import files;
import io;
import launch;
import stats;
import string;
import sys;

import common;

(boolean vld) sw_chk_params(int params[])
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

	// 0) StageWrite: total number of processes
	// 1) StageWrite: number of processes per worker
	// 2) HeatTransfer: the total number of steps to output

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

(float exectime) sw_launch_wrapper(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		int sw_proc = params[0];	// StageWrite: total number of processes
		int sw_ppw = params[1];		// StageWrite: number of processes per worker
		int ht_step = params[2];	// HeatTransfer: the total number of steps to output

		string workflow_root = getenv("WORKFLOW_ROOT");
		string srcDir = "%s/experiment/wf-ht-bp%0.2i" % (workflow_root, ht_step);
		string turbine_output = getenv("TURBINE_OUTPUT");
		string parDir = "%s/run" % turbine_output;
		string dir = "%s/%s" % (parDir, run_id);

		int nwork1;
		if (sw_proc %% sw_ppw == 0) {
			nwork1 = sw_proc %/ sw_ppw;
		} else {
			nwork1 = sw_proc %/ sw_ppw + 1;
		}
		int timeout = 360 * float2int(2 ** count);

		string cmd1 = "../../../../../../Example-Heat_Transfer/stage_write/stage_write";

		// mpiexec -n 70 stage_write/stage_write heat.bp staged.bp MPI "" MPI ""
		string args1[] = split("heat.bp staged.bp MPI \"\" MPI \"\"", " ");

		string envs1[] = [ "swift_chdir="+dir, 
		       "swift_output="+dir/"output_stage_write.txt", 
		       "swift_exectime="+dir/"time_stage_write.txt",
		       "swift_timeout=%i" % timeout, 
		       "swift_numproc=%i" % sw_proc, 
		       "swift_ppw=%i" % sw_ppw ];

		printf("swift: launching with environment variables: %s", cmd1);
		setup_run2(parDir, srcDir, dir) =>
			sleep(1) =>
			exit_code1 = @par=nwork1 launch_envs(cmd1, args1, envs1);

		if (exit_code1 == 124)
		{
			sleep(1) =>
				exectime = sw_launch_wrapper(run_id, params, count + 1);
		}
		else
		{
			if (exit_code1 != 0)
			{
				exectime = -1.0;
				sw_failure(run_id, params);
				printf("swift: The launched application %s with parameters (%d, %d, %d) did not succeed with exit code: %d.", 
						cmd1, params[0], params[1], params[2], exit_code1);
			}
			else
			{
				exectime = sw_get_exectime(run_id, params);
			}
		}
	}
	else
	{
		exectime = -1.0;
		sw_failure(run_id, params);
		printf("swift: The launched application with parameters (%d, %d, %d) did not succeed %d times.",
				params[0], params[1], params[2], time_limit);

	}
}

(void v) sw_failure(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);
	string output = "%0.4i\t%0.2i\t%0.2i\t%s"
		% (params[0], params[1], params[2], "inf");
	file out <dir/"time.txt"> = write(output);
	v = propagate();
}

(float exectime) sw_get_exectime(string run_id, int params[], int count = 0)
{
	int time_limit = 2;
	if (count < time_limit)
	{
		string turbine_output = getenv("TURBINE_OUTPUT");
		string dir = "%s/run/%s" % (turbine_output, run_id);
	
		string cmd[] = [ turbine_output/"get_maxtime.sh", dir/"time_stage_write.txt" ];
		sleep(1) =>
			(time_output, time_exit_code) = system(cmd);
	
		if (time_exit_code != 0)
		{
			sleep(1) =>
				exectime = sw_get_exectime(run_id, params, count + 1);
		}
		else
		{
			exectime = string2float(time_output);
			if (exectime >= 0.0)
			{
				printf("exectime(%i, %i, %i): %f", 
					params[0], params[1], params[2], exectime);
				string output = "%0.4i\t%0.2i\t%0.2i\t%f" 
					% (params[0], params[1], params[2], exectime);
				file out <dir/"time.txt"> = write(output);
			}
			else
			{
				printf("swift: The execution time (%f seconds) of the launched application with parameters (%d, %d, %d) is negative.",
						exectime, params[0], params[1], params[2]);
			}
		}
	}
	else
	{
		exectime = -1.0;
		printf("swift: Failed to get the execution time of the launched application of parameters (%d, %d, %d) %d times.\n%s",
				params[0], params[1], params[2], time_limit);
	}
}

