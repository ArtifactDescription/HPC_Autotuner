import files;
import io;
import launch;
import stats;
import string;
import sys;

(void v) setup_run(string parDir, string srcDir, string dir) "turbine" "0.0"
[
"""
	file mkdir <<parDir>>
	file delete -force -- <<dir>>
	file copy -force -- <<srcDir>> <<dir>>
	cd <<dir>>
"""
];

(float exectime) launch_wrapper(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		int voro_proc = params[0];	// Voro: total num of processes
		int voro_ppw = params[1];	// Voro: num of processes per worker
		int voro_thrd = params[2];	// Voro: num of threads per process
		int lmp_spo = params[3];	// Lammps: num of steps per output interval, which decides the input size of Voro
		int lmp_l2s = params[4];	// Lammps: num of runs for the phase from liquid to solid
		int lmp_sld = params[5];	// Lammps: num of runs for the solid phase

		string workflow_root = getenv("WORKFLOW_ROOT");
		string srcDir = "%s/exp_lv/lmp-%0.4i-%0.5i-%0.5i" % (workflow_root, lmp_spo, lmp_l2s, lmp_sld);
		string turbine_output = getenv("TURBINE_OUTPUT");
		string parDir = "%s/run" % turbine_output;
		string dir = "%s/%s" % (parDir, run_id);

		int nwork1;
		if (voro_proc %% voro_ppw == 0) {
			nwork1 = voro_proc %/ voro_ppw;
		} else {
			nwork1 = voro_proc %/ voro_ppw + 1;
		}
		int timeout = 300 * float2int(2 ** count);

		string cmd1 = "../../../../../adios1-coupled/Example-LAMMPS/swift-all/voro_adios_omp_staging";

		// mpiexec -n 4 ./voro_adios_omp_staging dump.bp adios_atom_voro.bp BP
		string args1[] = split("dump.bp adios_atom_voro.bp BP", " ");

		string envs1[] = [ "OMP_NUM_THREADS="+int2string(voro_thrd),
		       "swift_chdir="+dir,
		       "swift_output="+dir/"output_voro_adios_omp_staging.txt",
		       "swift_exectime="+dir/"time_voro_adios_omp_staging.txt",
		       "swift_timeout=%i" % timeout,
		       "swift_numproc=%i" % voro_proc,
		       "swift_ppw=%i" % voro_ppw ];

		printf("swift: launching with environment variables: %s (%s, %s, %s)", cmd1, envs1[0], envs1[4], envs1[5]);
		setup_run(parDir, srcDir, dir) =>
			sleep(1) =>
			exit_code1 = @par=nwork1 launch_envs(cmd1, args1, envs1);

		if (exit_code1 == 124)
		{
			sleep(1) =>
				exectime = launch_wrapper(run_id, params, count + 1);
		}
		else
		{
			if (exit_code1 != 0)
			{
				exectime = -1.0;
				failure(run_id, params);
				printf("swift: The launched application %s with parameters (%d, %d, %d, %d, %d, %d) did not succeed with exit code: %d.", 
						cmd1, params[0], params[1], params[2], params[3], params[4], params[5], exit_code1);
			}
			else
			{
				exectime = get_exectime(run_id, params);
			}
		}
	}
	else
	{
		exectime = -1.0;
		failure(run_id, params);
		printf("swift: The launched application with parameters (%d, %d, %d, %d, %d, %d) did not succeed %d times.",
				params[0], params[1], params[2], params[3], params[4], params[5], time_limit);
	}
}

(void v) failure(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);
	string output = "%0.4i\t%0.2i\t%0.1i\t%0.3i\t%0.5i\t%0.5i\t%s"
		% (params[0], params[1], params[2], params[3], params[4], params[5], "inf");
	file out <dir/"time.txt"> = write(output);
	v = propagate();
}

(float exectime) get_exectime(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);

	string cmd[] = [ turbine_output/"get_maxtime.sh", dir/"time_voro_adios_omp_staging.txt" ];
	sleep(1) =>
		(time_output, time_exit_code) = system(cmd);

	if (time_exit_code != 0)
	{
		exectime = -1.0;
		printf("swift: Failed to get the execution time of the launched application of parameters (%d, %d, %d, %d, %d, %d) with exit code: %d.\n%s",
				params[0], params[1], params[2], params[3], params[4], params[5], time_exit_code, time_output);
	}
	else
	{
		exectime = string2float(time_output);
		if (exectime >= 0.0)
		{
			printf("exectime(%i, %i, %i, %i, %i, %i): %f", params[0], params[1], params[2], params[3], params[4], params[5], exectime);
			string output = "%0.4i\t%0.2i\t%0.1i\t%0.3i\t%0.5i\t%0.5i\t%f"
				% (params[0], params[1], params[2], params[3], params[4], params[5], exectime);
			file out <dir/"time.txt"> = write(output);
		}
		else
		{
			printf("swift: The execution time (%f seconds) of the launched application with parameters (%d, %d, %d, %d, %d, %d) is negative.",
					exectime, params[0], params[1], params[2], params[3], params[4], params[5]);
		}
	}
}

main()
{
	int ppn = 36;   // bebop
	int wpn = string2int(getenv("PPN"));
	int ppw = ppn %/ wpn - 1;
	int workers;
	if (string2int(getenv("PROCS")) - 2 < 32) {
		workers = string2int(getenv("PROCS")) - 2;
	} else {
		workers = 32;
	}

	// 0) Voro: total num of processes
	// 1) Voro: num of processes per worker
	// 2) Voro: num of threads per process
	// 3) Lammps: num of steps per output interval, which decides the input size of Voro
	// 4) Lammps: num of runs for the phase from liquid to solid
	// 5) Lammps: num of runs for the solid phase
	int sample_num = string2int(read(input("num_smpl.txt")));
	conf_samples = file_lines(input("smpl_vr.csv"));

	float exectime[];
	int codes[];
	foreach i in [0 : sample_num - 1 : 1]
	{
		params_str = split(conf_samples[i], "\t");
		int params[];
		foreach j in [0 : 5 : 1]
		{
			params[j] = string2int(params_str[j]);
		}
		if (params[1] <= ppw)
		{
			int nwork;
			if (params[0] %% params[1] == 0) {
				nwork = params[0] %/ params[1];
			} else {
				nwork = params[0] %/ params[1] + 1;
			}
			if (nwork <= workers)
			{
				exectime[i] = launch_wrapper("%0.4i_%0.2i_%0.1i_%0.3i_%0.5i_%0.5i"
						% (params[0], params[1], params[2], params[3], params[4], params[5]),
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
		printf("swift: all the launched applications succeed.");
	} else {
		printf("swift: %d of %d launched applications did not succeed.", failure_num, sample_num);
	}
}

