import files;
import io;
import launch;
import stats;
import string;
import sys;

(void v) setup_run(string dir, string infile1, string infile2, string infile3) "turbine" "0.0"
[
"""
	file delete -force -- <<dir>>
	file mkdir <<dir>>
	cd <<dir>>
	file copy -force -- <<infile1>> in.quench
	file copy -force -- <<infile2>> restart.liquid
	file copy -force -- <<infile3>> CuZr.fs
"""
];

(float exectime) launch_wrapper(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		int lmp_proc = params[0];	// Lammps: total num of processes
		int lmp_ppw = params[1];	// Lammps: num of processes per worker
		int lmp_thrd = params[2];	// Lammps: num of threads per process
		int voro_proc = params[3];	// Voro: total num of processes
		int voro_ppw = params[4];	// Voro: num of processes per worker
		int voro_thrd = params[5];	// Voro: num of threads per process
		int lmp_spo = params[6];	// Lammps: num of steps per output interval

		string workflow_root = getenv("WORKFLOW_ROOT");
		string turbine_output = getenv("TURBINE_OUTPUT");
		string dir = "%s/run/%s" % (turbine_output, run_id);
		string infile1 = "%s/in.quench" % turbine_output;
		string infile2 = "%s/restart.liquid" % turbine_output;
		string infile3 = "%s/CuZr.fs" % turbine_output;

		string cmd0[] = [ workflow_root/"lmp.sh", int2string(lmp_spo), "FLEXPATH", "16000", "20000", dir/"in.quench" ];
		setup_run(dir, infile1, infile2, infile3) =>
			(output0, exit_code0) = system(cmd0);

		if (exit_code0 != 0)
		{
			printf("swift: %s failed with exit code %d for the parameters (%d, %d, %d, %d, %d, %d, %d).", 
					cmd0[0]+" "+cmd0[1]+" "+cmd0[2]+" "+cmd0[3], exit_code0, 
					params[0], params[1], params[2], params[3], params[4], params[5], params[6]);
			sleep(1) =>
				exectime = launch_wrapper(run_id, params, count + 1);
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
				timeout = 1200 * float2int(2 ** count);
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
			cmds[0] = "../../../../../adios1-coupled/Example-LAMMPS/swift-all/lmp_mpi";
			cmds[1] = "../../../../../adios1-coupled/Example-LAMMPS/swift-all/voro_adios_omp_staging";

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
					exectime = launch_wrapper(run_id, params, count + 1);
			}
			else
			{
				if (exit_code != 0)
				{
					exectime = -1.0;
					failure(run_id, params);
					printf("swift: The multi-launched application with parameters (%d, %d, %d, %d, %d, %d, %d) did not succeed with exit code: %d.", 
							params[0], params[1], params[2], params[3], params[4], params[5], params[6], exit_code);
				}
				else
				{
					exectime = get_exectime(run_id, params);
				}
			}
		}
	}
	else
	{
		exectime = -1.0;
		failure(run_id, params);
		printf("swift: The launched application with parameters (%d, %d, %d, %d, %d, %d, %d) did not succeed %d times.",
				params[0], params[1], params[2], params[3], params[4], params[5], params[6], time_limit);
	}
}

(void v) failure(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);
	string output = "%0.4i\t%0.2i\t%0.1i\t%0.4i\t%0.2i\t%0.1i\t%0.3i\t%s"
		% (params[0], params[1], params[2], params[3], params[4], params[5], params[6], "inf");
	file out <dir/"time.txt"> = write(output);
	v = propagate();
}

(float exectime) get_exectime(string run_id, int params[], int count = 0)
{
	int time_limit = 3;
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
				exectime = get_exectime(run_id, params, count + 1);
		}
		else
		{
			exectime = string2float(time_output);
			if (exectime >= 0.0) {
				printf("exectime(%i, %i, %i, %i, %i, %i, %i): %f",
						params[0], params[1], params[2], params[3], params[4], params[5], params[6], exectime);
				string output = "%0.4i\t%0.2i\t%0.1i\t%0.4i\t%0.2i\t%0.1i\t%0.3i\t%f"
					% (params[0], params[1], params[2], params[3], params[4], params[5], params[6], exectime);
				file out <dir/"time.txt"> = write(output);
			}
			else
			{
				printf("swift: The execution time (%f seconds) of the multi-launched application with parameters (%d, %d, %d, %d, %d, %d, %d) is negative.",
						exectime, params[0], params[1], params[2], params[3], params[4], params[5], params[6]);
			}
		}
	}
	else
	{
		exectime = -1.0;
		printf("swift: Failed to get the execution time of the multi-launched application of parameters (%d, %d, %d, %d, %d, %d, %d) %d times.\n%s",
				params[0], params[1], params[2], params[3], params[4], params[5], params[6], time_limit);
	}
}

main()
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

	// 0) Lammps: total num of processes
	// 1) Lammps: num of processes per worker
	// 2) Lammps: num of threads per process
	// 3) Voro: total num of processes
	// 4) Voro: num of processes per worker
	// 5) Voro: num of threads per process
	// 6) Lammps: num of steps per output interval
	int sample_num = string2int(read(input("num_smpl.txt")));
	conf_samples = file_lines(input("smpl_lv.csv"));

	float exectime[];
	int codes[];
	foreach i in [0 : sample_num - 1 : 1]
	{
		params_str = split(conf_samples[i], "\t");
		int params[];
		foreach j in [0 : 6 : 1]
		{
			params[j] = string2int(params_str[j]);
		}
		if ((params[1] <= ppw) && (params[4] <= ppw))
		{
			int nwork;
			if (params[0] %% params[1] == 0 && params[3] %% params[4] == 0) {
				nwork = params[0] %/ params[1] + params[3] %/ params[4];
			} else {
				if (params[0] %% params[1] == 0 || params[3] %% params[4] == 0) {
					nwork = params[0] %/ params[1] + params[3] %/ params[4] + 1;
				} else {
					nwork = params[0] %/ params[1] + params[3] %/ params[4] + 2;
				}
			}
			if (nwork <= workers)
			{
				exectime[i] = launch_wrapper("%0.4i_%0.2i_%0.1i_%0.4i_%0.2i_%0.1i_%0.3i" 
						% (params[0], params[1], params[2], params[3], params[4], params[5], params[6]), 
						params);

				if (exectime[i] >= 0.0) {
					codes[i] = 0;
				} else {
					codes[i] = 1;
				}
			}
		}
	}
	int failure_num = sum_integer(codes);
	if (failure_num == 0) {
		printf("swift: all the multi-launched applications succeed.");
	} else {
		printf("swift: %d of %d launched applications did not succeed.", failure_num, sample_num);
	}
}

