import files;
import io;
import launch;
import stats;
import string;
import sys;

import common;

(boolean vld) lmp_chk_params(int params[])
{
	int ppn = 36;   // bebop
	int wpn = string2int(getenv("PPN"));
	int ppw = ppn %/ wpn - 1;
	int workers;
	if (string2int(getenv("PROCS")) - 2 < 31) {
		workers = string2int(getenv("PROCS")) - 2;
	} else {
		workers = 31;
	}

	// 0) Lammps: total num of processes
	// 1) Lammps: num of processes per worker
	// 2) Lammps: num of threads per process
	// 3) Lammps: IO interval in steps

	if ((params[1] <= ppw) && (params[0] >= params[1]))
	{
		int nwork;
		if (params[0] %% params[1] == 0) {
			nwork = params[0] %/ params[1];
		} else {
			nwork = params[0] %/ params[1] + 1;
		}
		if (nwork <= workers) {
			vld = true;
		} else {
			vld = false;
		}
	}
	else
	{
		vld = false;
	}
}

(float exectime) lmp_launch_wrapper(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		int lmp_proc = params[0];	// Lammps: total num of processes
		int lmp_ppw = params[1];	// Lammps: num of processes per worker
		int lmp_thrd = params[2];	// Lammps: num of threads per process
		int lmp_frqIO = params[3];	// Lammps: IO interval in steps

		string workflow_root = getenv("WORKFLOW_ROOT");
		string turbine_output = getenv("TURBINE_OUTPUT");
		string dir = "%s/run/%s" % (turbine_output, run_id);
		string infile1 = "%s/in.quench" % turbine_output;
		string infile2 = "%s/restart.liquid" % turbine_output;
		string infile3 = "%s/CuZr.fs" % turbine_output;

		string cmd0[] = [ workflow_root/"lmp.sh", int2string(lmp_frqIO), "POSIX", "16000", "20000", dir/"in.quench" ];
		setup_run_lmp(dir, infile1, infile2, infile3) =>
			(output0, exit_code0) = system(cmd0);

		if (exit_code0 != 0)
		{
			printf("swift: %s failed with exit code %d for the parameters (%d, %d, %d, %d).", 
					cmd0[0]+" "+cmd0[1]+" "+cmd0[2]+" "+cmd0[3], exit_code0, 
					params[0], params[1], params[2], params[3]);
			sleep(1) =>
				exectime = lmp_launch_wrapper(run_id, params, count + 1);
		}
		else
		{
			int nwork1;
			if (lmp_proc %% lmp_ppw == 0) {
				nwork1 = lmp_proc %/ lmp_ppw;
			} else {
				nwork1 = lmp_proc %/ lmp_ppw + 1;
			}
			int timeout;
			if (lmp_proc <= 16) {
				timeout = 1200 * float2int(2 ** count);
			} else {
				if (lmp_proc <= 32) {
					timeout = 600 * float2int(2 ** count);
				} else {
					if (lmp_proc <= 64) {
						timeout = 300 * float2int(2 ** count);
					} else {
						if (lmp_proc <= 128) {
							timeout = 150 * float2int(2 ** count);
						} else {
							timeout = 75 * float2int(2 ** count);
						}
					}
				}
			}

			string cmd1 = "../../../../../../Example-LAMMPS/swift-all/lmp_mpi"; 

			string args1[] = split("-i in.quench", " ");	// mpiexec -n 8 ./lmp_mpi -i in.quench

			string envs1[] = [ "OMP_NUM_THREADS="+int2string(lmp_thrd), 
			       "swift_chdir="+dir, 
			       "swift_output="+dir/"output_lmp_mpi.txt", 
			       "swift_exectime="+dir/"time_lmp_mpi.txt",
			       "swift_timeout=%i" % timeout,
			       "swift_numproc=%i" % lmp_proc,
			       "swift_ppw=%i" % lmp_ppw ];

			printf("swift: launching with environment variables: %s", cmd1);
			sleep(1) =>
				exit_code1 = @par=nwork1 launch_envs(cmd1, args1, envs1);

			if (exit_code1 == 124)
			{
				sleep(1) =>
					exectime = lmp_launch_wrapper(run_id, params, count + 1);
			}
			else
			{
				if (exit_code1 != 0)
				{
					exectime = -1.0;
					lmp_failure(run_id, params);
					printf("swift: The launched application %s with parameters (%d, %d, %d, %d) did not succeed with exit code: %d.", 
							cmd1, params[0], params[1], params[2], params[3], exit_code1);
				}
				else
				{
					exectime = lmp_get_exectime(run_id, params);
				}
			}
		}
	}
	else
	{
		exectime = -1.0;
		lmp_failure(run_id, params);
		printf("swift: The launched application with parameters (%d, %d, %d, %d) did not succeed %d times.",
				params[0], params[1], params[2], params[3], time_limit);
	}
}

(void v) lmp_failure(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);
	string output = "%0.4i\t%0.2i\t%0.1i\t%0.4i\t%s"
		% (params[0], params[1], params[2], params[3], "inf");
	file out <dir/"time.txt"> = write(output);
	v = propagate();
}

(float exectime) lmp_get_exectime(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		string turbine_output = getenv("TURBINE_OUTPUT");
		string dir = "%s/run/%s" % (turbine_output, run_id);

		string cmd[] = [ turbine_output/"get_maxtime.sh", dir/"time_lmp_mpi.txt" ];
		sleep(1) =>
			(time_output, time_exit_code) = system(cmd);

		if (time_exit_code != 0)
		{
			sleep(1) =>
				exectime = lmp_get_exectime(run_id, params, count + 1);
		}                       
		else                    
		{
			exectime = string2float(time_output);
			if (exectime >= 0.0)
			{
				printf("exectime(%i, %i, %i, %i): %f", params[0], params[1], params[2], params[3], exectime);
				string output = "%0.4i\t%0.2i\t%0.1i\t%0.4i\t%f" 
					% (params[0], params[1], params[2], params[3], exectime);
				file out <dir/"time.txt"> = write(output);
			}
			else
			{
				printf("swift: The execution time (%f seconds) of the launched application with parameters (%d, %d, %d, %d) is negative.", 
						exectime, params[0], params[1], params[2], params[3]);                    
			}
		}
	}
	else
	{
		exectime = -1.0;
		printf("swift: Failed to get the execution time of the launched application of parameters (%d, %d, %d, %d) %d times.\n%s",
				params[0], params[1], params[2], params[3], time_limit);
	}
}

