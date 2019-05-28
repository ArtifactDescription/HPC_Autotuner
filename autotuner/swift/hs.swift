import files;
import io;
import launch;
import stats;
import string;
import sys;

import common;

(boolean vld) hs_chk_params(int params[])
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

	// 0) HeatTransfer: total number of processes in X dimension
	// 1) HeatTransfer: total number of processes in Y dimension
	// 2) HeatTransfer: number of processes per worker
	// 3) HeatTransfer: the total number of steps to output
	// 4) HeatTransfer: the maximum size of I/O buffer
	// 5) StageWrite: total number of processes
	// 6) StageWrite: number of processes per worker

	if ((params[2] <= ppw) && (params[6] <= ppw) && (params[0] * params[1] >= params[2]) && (params[5] >= params[6]))
	{
		int nwork;
		if (params[0] * params[1] %% params[2] == 0 && params[5] %% params[6] == 0) {
			nwork = params[0] * params[1] %/ params[2] + params[5] %/ params[6];
		} else {
			if (params[0] * params[1] %% params[2] == 0 || params[5] %% params[6] == 0) {
				nwork = params[0] * params[1] %/ params[2] + params[5] %/ params[6] + 1;
			} else {
				nwork = params[0] * params[1] %/ params[2] + params[5] %/ params[6] + 2;
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

(float exectime) hs_launch_wrapper(string run_id, int params[], int count = 0) 
{
	int time_limit = 2;
	if (count < time_limit)
	{
		int ht_proc_x = params[0];	// HeatTransfer: total number of processes in X dimension
		int ht_proc_y = params[1];	// HeatTransfer: total number of processes in Y dimension
		int ht_ppw = params[2];		// HeatTransfer: number of processes per worker
		int ht_step = params[3];	// HeatTransfer: the total number of steps to output
		int ht_buff = params[4];	// HeatTransfer: the maximum size of I/O buffer
		int sw_proc = params[5];	// StageWrite: total number of processes
		int sw_ppw = params[6];		// StageWrite: number of processes per worker

		string workflow_root = getenv("WORKFLOW_ROOT");
		string turbine_output = getenv("TURBINE_OUTPUT");
		string dir = "%s/run/%s" % (turbine_output, run_id);
		string infile = "%s/heat_transfer.xml" % turbine_output;

		string cmd0[] = [ workflow_root/"ht.sh", "FLEXPATH", int2string(ht_buff), dir/"heat_transfer.xml" ];
		setup_run_ht(dir, infile) =>
			(output0, exit_code0) = system(cmd0);

		if (exit_code0 != 0)
		{
			printf("swift: %s failed with exit code %d for the parameters (%d, %d, %d, %d, %d, %d, %d).", 
					cmd0[0]+" "+cmd0[1]+" "+cmd0[2]+" "+cmd0[3], exit_code0, 
					params[0], params[1], params[2], params[3], params[4], params[5], params[6]);
			sleep(1) =>
				exectime = hs_launch_wrapper(run_id, params, count + 1);
		}
		else
		{
			// Worker counts
			int nworks[];
			ht_proc = ht_proc_x * ht_proc_y;
			if (ht_proc %% ht_ppw == 0) {
				nworks[0] = ht_proc %/ ht_ppw;
			} else {
				nworks[0] = ht_proc %/ ht_ppw + 1;
			}
			if (sw_proc %% sw_ppw == 0) {
				nworks[1] = sw_proc %/ sw_ppw;
			} else {
				nworks[1] = sw_proc %/ sw_ppw + 1;
			}
			int timeout = 1200 * float2int(2 ** count);

			// Commands
			string cmds[];
			cmds[0] = "../../../../../../Example-Heat_Transfer/heat_transfer_adios2";
			cmds[1] = "../../../../../../Example-Heat_Transfer/stage_write/stage_write";

			// Command line arguments
			string args[][];

			// Problem Size of HeatTransfer
			int ht_x = 2048;
			int ht_y = 2048;
			int ht_iter = 1024;
			int ht_las_x = ht_x %/ ht_proc_x;
			int ht_las_y = ht_y %/ ht_proc_y;
			int ht_ips = ht_iter %/ ht_step;
			// mpiexec -n 12 ./heat_transfer_adios2 heat 4 3 40 50 6 5
			args[0] = split("heat %i %i %i %i %i %i" 
					% (ht_proc_x, ht_proc_y, ht_las_x, ht_las_y, ht_step, ht_ips), " ");

			// mpiexec -n 3 stage_write/stage_write heat.bp staged.bp FLEXPATH "" MPI ""
			string method = "FLEXPATH";
			args[1] = split("heat.bp staged.bp %s \"\" MPI \"\"" % method , " ");

			// Environment variables
			string envs[][];
			envs[0] = [ "swift_chdir="+dir, 
				"swift_output="+dir/"output_heat_transfer_adios2.txt", 
				"swift_exectime="+dir/"time_heat_transfer_adios2.txt", 
				"swift_timeout=%i" % timeout, 
				"swift_numproc=%i" % ht_proc, 
				"swift_ppw=%i" % ht_ppw ];
			envs[1] = [ "swift_chdir="+dir, 
				"swift_output="+dir/"output_stage_write.txt", 
				"swift_exectime="+dir/"time_stage_write.txt", 
				"swift_timeout=%i" % timeout, 
				"swift_numproc=%i" % sw_proc, 
				"swift_ppw=%i" % sw_ppw ];

			printf("swift: multiple launching: %s, %s", cmds[0], cmds[1]);
			sleep(1) =>
				exit_code = @par=sum_integer(nworks) launch_multi(nworks, cmds, args, envs);

			if (exit_code == 124)
			{
				sleep(1) =>
					exectime = hs_launch_wrapper(run_id, params, count + 1);
			}
			else
			{
				if (exit_code != 0)
				{
					exectime = -1.0;
					hs_failure(run_id, params);
					printf("swift: The multi-launched application with parameters (%d, %d, %d, %d, %d, %d, %d) did not succeed with exit code: %d.", 
							params[0], params[1], params[2], params[3], params[4], params[5], params[6], exit_code);
				}
				else
				{
					exectime = hs_get_exectime(run_id, params);
				}
			}
		}
	}
	else
	{
		exectime = -1.0;
		hs_failure(run_id, params);
		printf("swift: The launched application with parameters (%d, %d, %d, %d, %d, %d, %d) did not succeed %d times.",
				params[0], params[1], params[2], params[3], params[4], params[5], params[6], time_limit);
	}
}

(void v) hs_failure(string run_id, int params[])
{
	string turbine_output = getenv("TURBINE_OUTPUT");
	string dir = "%s/run/%s" % (turbine_output, run_id);
	string output = "%0.2i\t%0.2i\t%0.2i\t%0.2i\t%0.2i\t%0.4i\t%0.2i\t%s"
		% (params[0], params[1], params[2], params[3], params[4], params[5], params[6], "inf");
	file out <dir/"time.txt"> = write(output);
	v = propagate();
}

(float exectime) hs_get_exectime(string run_id, int params[], int count = 0)
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
				exectime = hs_get_exectime(run_id, params, count + 1);
		}
		else
		{
			exectime = string2float(time_output);
			if (exectime >= 0.0)
			{
				printf("exectime(%i, %i, %i, %i, %i, %i, %i): %f",
						params[0], params[1], params[2], params[3], params[4], params[5], params[6], exectime);
				string output = "%0.2i\t%0.2i\t%0.2i\t%0.2i\t%0.2i\t%0.4i\t%0.2i\t%f"
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

