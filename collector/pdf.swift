import files;
import io;
import launch;
import stats;
import string;
import sys;

(void v) setup_run(string parDir, string srcDir, string dir, string confile) "turbine" "0.0"
[
"""
	file mkdir <<parDir>>
	file delete -force -- <<dir>>
	file copy -force -- <<srcDir>> <<dir>>
	cd <<dir>>
	file copy -force -- <<confile>> adios2.xml
"""
];

(void v) clearup_run(string dir1, string dir2) "turbine" "0.0"
[
"""
	file delete -force -- <<dir1>>
	file delete -force -- <<dir2>>
"""
];

(float exectime) launch_wrapper(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		int gs_cs = params[0];		// gray-scott: the cube size of global array (L x L x L)
		int gs_step = params[1];	// gray-scott: the total number of steps to simulate
		int pdf_proc = params[2];	// pdf_calc: the total number of processes
		int pdf_ppw = params[3];	// pdf_calc: the number of processes per worker

		string workflow_root = getenv("WORKFLOW_ROOT");
		string srcDir = "%s/bp4/gs-%0.4i-%0.3i" % (workflow_root, gs_cs, gs_step);
		string turbine_output = getenv("TURBINE_OUTPUT");
		string parDir = "%s/run" % turbine_output;
		string dir = "%s/%s" % (parDir, run_id);
		string confile = "%s/adios2.xml" % turbine_output;

		int nwork1;
		if (pdf_proc %% pdf_ppw == 0) {
			nwork1 = pdf_proc %/ pdf_ppw;
		} else {
			nwork1 = pdf_proc %/ pdf_ppw + 1;
		}
		int timeout = 900 * float2int(2 ** count);

		string cmd1 = "../../../../../adios2-coupled/gray-scott/build/pdf_calc";

		// mpiexec -n 8 build/pdf_calc gs.bp pdf.bp 200
		string args1[] = split("gs.bp pdf.bp 200", " ");

		string envs1[] = [ "swift_chdir="+dir,
		       "swift_output="+dir/"output_pdf_calc.txt",
		       "swift_exectime="+dir/"time_pdf_calc.txt",
		       "swift_timeout=%i" % timeout,
		       "swift_numproc=%i" % pdf_proc,
		       "swift_ppw=%i" % pdf_ppw ];

		printf("swift: launching with environment variables: %s (%s, %s)", cmd1, envs1[4], envs1[5]);
		setup_run(parDir, srcDir, dir, confile) =>
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
				printf("swift: The launched application %s with parameters (%d, %d, %d, %d) did not succeed with exit code: %d.", 
						cmd1, params[0], params[1], params[2], params[3], exit_code1);
			}
			else
			{
				string simu_dir = "%s/gs.bp" % dir;
				string anal_dir = "%s/pdf.bp" % dir;
				sleep(1) =>
					clearup_run(simu_dir, anal_dir);
				exectime = get_exectime(run_id, params);
			}
		}
	}
	else
	{
		exectime = -1.0;
		failure(run_id, params);
		printf("swift: The launched application with parameters (%d, %d, %d, %d) did not succeed %d times.",
				params[0], params[1], params[2], params[3], time_limit);
	}
}

(void v) failure(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);
	string output = "%0.4i\t%0.3i\t%0.4i\t%0.2i\t%s"
		% (params[0], params[1], params[2], params[3], "inf");
	file out <dir/"time.txt"> = write(output);
	v = propagate();
}

(float exectime) get_exectime(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);

	string cmd[] = [ turbine_output/"get_maxtime.sh", dir/"time_pdf_calc.txt" ];
	sleep(1) =>
		(time_output, time_exit_code) = system(cmd);

	if (time_exit_code != 0)
	{
		exectime = -1.0;
		printf("swift: Failed to get the execution time of the launched application of parameters (%d, %d, %d, %d) with exit code: %d.\n%s",
				params[0], params[1], params[2], params[3], time_exit_code, time_output);
	}
	else
	{
		exectime = string2float(time_output);
		if (exectime >= 0.0)
		{
			printf("exectime(%i, %i, %i, %i): %f", params[0], params[1], params[2], params[3], exectime);
			string output = "%0.4i\t%0.3i\t%0.4i\t%0.2i\t%f"
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

main()
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

	// 0) gray-scott: the cube size of global array (L x L x L)
	// 1) gray-scott: the total number of steps to simulate
	// 2) pdf_calc: the total number of processes
	// 3) pdf_calc: the number of processes per worker
	int sample_num = 500;
	conf_samples = file_lines(input("smpl_pdf.csv"));

	float exectime[];
	int codes[];
	for (int i = 0, int flag0 = 0; i < sample_num; i = i + 1, flag0 = flag1)
	{
		int flag1;
		params_str = split(conf_samples[i], "\t");
		int params[];
		foreach j in [0 : 3 : 1]
		{
			params[j] = string2int(params_str[j]);
		}
		if (params[3] <= ppw)
		{
			int nwork;
			if (params[2] %% params[3] == 0) {
				nwork = params[2] %/ params[3];
			} else {
				nwork = params[2] %/ params[3] + 1;
			}
			if (nwork <= workers)
			{
				flag0 =>
					exectime[i] = launch_wrapper("%0.4i_%0.3i_%0.4i_%0.2i"
						% (params[0], params[1], params[2], params[3]),
						params);

				if (exectime[i] >= 0.0) {
					codes[i] = 0;
				} else {
					codes[i] = 1;
				}
				flag1 = codes[i];
			} else {
				flag1 = flag0;
			}
		} else {
			flag1 = flag0;
		}
	}
	int failure_num = sum_integer(codes);
	if (failure_num == 0) {
		printf("swift: all the launched applications succeed.");
	} else {
		printf("swift: %d of %d launched applications did not succeed.", failure_num, sample_num);
	}
}

