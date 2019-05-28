import files;
import io;
import launch;
import stats;
import string;
import sys;

import common;

(boolean vld) lvi_chk_params(int params[])
{

	int ppn = 36;	// bebop
	int wpn = string2int(getenv("PPN"));
	int ppw = ppn %/ wpn - 1;
	int workers;
	if (string2int(getenv("PROCS")) - 2 < 32) {
		workers = string2int(getenv("PROCS")) - 2;
	} else  {
		workers = 32;
	}

	// 0) Lammps: the num of runs for the phase from liquid to solid
	// 1) Lammps: the num of runs for the solid phase
	// 2) Lammps: total num of processes
	// 3) Lammps: num of processes per worker
	// 4) Lammps: num of threads per process
	// 5) Lammps: IO interval in steps
	// 6) Voro: total num of processes
	// 7) Voro: num of processes per worker
	// 8) Voro: num of threads per process

	if ((params[3] <= ppw) && (params[7] <= ppw) && (params[2] >= params[3]) && (params[6] >= params[7]))
	{
		int nwork;
		if (params[2] %% params[3] == 0 && params[6] %% params[7] == 0) {
			nwork = params[2] %/ params[3] + params[6] %/ params[7];
		} else {
			if (params[2] %% params[3] == 0 || params[6] %% params[7] == 0) {
				nwork = params[2] %/ params[3] + params[6] %/ params[7] + 1;
			} else {
				nwork = params[2] %/ params[3] + params[6] %/ params[7] + 2;
			}
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

(float exectime) lvi_launch_wrapper(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		int lmp_l2s = params[0];	// Lammps: the num of runs for the phase from liquid to solid
		int lmp_sld = params[1];	// Lammps: the num of runs for the solid phase
		int lmp_proc = params[2];	// Lammps: total num of processes
		int lmp_ppw = params[3];	// Lammps: num of processes per worker
		int lmp_thrd = params[4];	// Lammps: num of threads per process
		int lmp_frqIO = params[5];	// Lammps: IO interval in steps
		int voro_proc = params[6];	// Voro: total num of processes
		int voro_ppw = params[7];	// Voro: num of processes per worker
		int voro_thrd = params[8];	// Voro: num of threads per process

		string workflow_root = getenv("WORKFLOW_ROOT");
		string turbine_output = getenv("TURBINE_OUTPUT");
		string dir = "%s/run/%s" % (turbine_output, run_id);
		string infile1 = "%s/in.quench" % turbine_output;
		string infile2 = "%s/restart.liquid" % turbine_output;
		string infile3 = "%s/CuZr.fs" % turbine_output;

		string cmd0[] = [ workflow_root/"lmp.sh", int2string(lmp_frqIO), "FLEXPATH", int2string(lmp_l2s), int2string(lmp_sld), dir/"in.quench" ];
		setup_run_lmp(dir, infile1, infile2, infile3) =>
			(output0, exit_code0) = system(cmd0);

		if (exit_code0 != 0)
		{
			printf("swift: %s failed with exit code %d for the parameters (%d, %d, %d, %d, %d, %d, %d, %d, %d).", 
					cmd0[0]+" "+cmd0[1]+" "+cmd0[2]+" "+cmd0[3], exit_code0, 
					params[0], params[1], params[2], params[3], params[4], 
					params[5], params[6], params[7], params[8]);
			sleep(1) =>
				exectime = lvi_launch_wrapper(run_id, params, count + 1);
		}
		else
		{
			// Worker counts
			int nworks[];
			if (lmp_proc %% lmp_ppw == 0) {
				nworks[0] = lmp_proc %/ lmp_ppw;
			} else {
				nworks[0] = lmp_proc %/ lmp_ppw + 1;
			}
			if (voro_proc %% voro_ppw == 0) {
				nworks[1] = voro_proc %/ voro_ppw;
			} else {
				nworks[1] = voro_proc %/ voro_ppw + 1;
			}
			int timeout;
			if (lmp_proc <= 16) {
				timeout = 1600 * float2int(2 ** count);
			} else {
				if (lmp_proc <= 32) {
					timeout = 600 * float2int(2 ** count);
				} else {
					if (lmp_proc <= 256) {
						timeout = 300 * float2int(2 ** count);
					} else {
						timeout = 150 * float2int(2 ** count);
					}
				}
			}

			// Commands
			string cmds[];
			cmds[0] = "../../../../../../Example-LAMMPS/swift-all/lmp_mpi";
			cmds[1] = "../../../../../../Example-LAMMPS/swift-all/voro_adios_omp_staging";

			// Command line arguments
			string args[][];

			// mpiexec -n 8 ./lmp_mpi -i in.quench
			args[0] = split("-i in.quench", " ");

			// mpiexec -n 4 ./voro_adios_omp_staging dump.bp adios_atom_voro.bp FLEXPATH
			args[1] = split("dump.bp adios_atom_voro.bp FLEXPATH", " ");

			// Environment variables
			string envs[][];
			envs[0] = [ "OMP_NUM_THREADS="+int2string(lmp_thrd), 
				"swift_chdir="+dir, 
				"swift_output="+dir/"output_lmp_mpi.txt", 
				"swift_exectime="+dir/"time_lmp_mpi.txt",
				"swift_timeout=%i" % timeout, 
				"swift_numproc=%i" % lmp_proc, 
				"swift_ppw=%i" % lmp_ppw ];
			envs[1] = [ "OMP_NUM_THREADS="+int2string(voro_thrd), 
				"swift_chdir="+dir, 
				"swift_output="+dir/"output_voro_adios_omp_staging.txt", 
				"swift_exectime="+dir/"time_voro_adios_omp_staging.txt", 
				"swift_timeout=%i" % timeout, 
				"swift_numproc=%i" % voro_proc, 
				"swift_ppw=%i" % voro_ppw ];

			printf("swift: multiple launching: %s, %s", cmds[0], cmds[1]);
			sleep(1) =>
				exit_code = @par=sum_integer(nworks) launch_multi(nworks, cmds, args, envs);

			if (exit_code == 124)
			{
				sleep(1) =>
					exectime = lvi_launch_wrapper(run_id, params, count + 1);
			}
			else
			{
				if (exit_code != 0)
				{
					exectime = -1.0;
					lvi_failure(run_id, params);
					printf("swift: The multi-launched application with parameters (%d, %d, %d, %d, %d, %d, %d, %d, %d) did not succeed with exit code: %d.", 
							params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], exit_code);
				}
				else
				{
					exectime = lvi_get_exectime(run_id, params);
				}
			}
		}
	}
	else
	{
		exectime = -1.0;
		lvi_failure(run_id, params);
		printf("swift: The launched application with parameters (%d, %d, %d, %d, %d, %d, %d, %d, %d) did not succeed %d times.",
				params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], time_limit);
	}
}

(void v) lvi_failure(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);
	string output = "%0.5i\t%0.5i\t%0.4i\t%0.2i\t%0.1i\t%0.3i\t%0.4i\t%0.2i\t%0.1i\t%s"
		% (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], "inf");
	file out <dir/"time.txt"> = write(output);
	v = propagate();
}

(float exectime) lvi_get_exectime(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		string turbine_output = getenv("TURBINE_OUTPUT");
		string dir = "%s/run/%s" % (turbine_output, run_id);

		string cmd[] = [ turbine_output/"get_maxtime.sh", dir/"time_*.txt" ];
		sleep(1) =>
			(time_output, time_exit_code) = system(cmd);

		if (time_exit_code != 0)
		{
			sleep(1) =>
				exectime = lvi_get_exectime(run_id, params, count + 1);
		}
		else
		{
			exectime = string2float(time_output);
			if (exectime >= 0.0) {
				printf("exectime(%i, %i, %i, %i, %i, %i, %i, %i, %i): %f",
						params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], exectime);
				string output = "%0.5i\t%0.5i\t%0.4i\t%0.2i\t%0.1i\t%0.3i\t%0.4i\t%0.2i\t%0.1i\t%f"
					% (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], exectime);
				file out <dir/"time.txt"> = write(output);
			}
			else
			{
				printf("swift: The execution time (%f seconds) of the multi-launched application with parameters (%d, %d, %d, %d, %d, %d, %d, %d, %d) is negative.",
						exectime, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8]);
			}
		}
	}
	else
	{
		exectime = -1.0;
		printf("swift: Failed to get the execution time of the multi-launched application of parameters (%d, %d, %d, %d, %d, %d, %d, %d, %d) %d times.\n%s",
				params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], time_limit);
	}
}

