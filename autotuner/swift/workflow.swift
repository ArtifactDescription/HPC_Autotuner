import assert;
import files;
import io;
import location;
import launch;
import python;
import stats;
import string;
import sys;

import EQPy;
import common;
import lv;
import lvi;
import lmp;
import vr;
import hs;
import hsi;
import ht;
import sw;

location ML = locationFromRank(turbine_workers() - 1);

(void v) handshake(string settings_filename)
{
	message = EQPy_get(ML) =>
		v = EQPy_put(ML, settings_filename);
	assert(message == "Settings", "Error in handshake.");
}

(void v) loop()
{
	for (boolean b = true;
			b;
			b=c)
	{
		message = EQPy_get(ML);
		boolean c;
		if (message == "FINAL")
		{
			printf("Swift: FINAL") =>
				v = make_void() =>
				c = false;
			finals = EQPy_get(ML);
			printf("Swift: finals: %s", finals);
		}
		else if (message == "EQPY_ABORT")
		{
			printf("Swift: EQ/Py aborted!") =>
			v = make_void() =>
			c = false;
		}
		else
		{
			printf("Swift: message: %s", message);
			if (message == "lv" || message == "lvi" || message == "lmp" || message == "vr"
				|| message == "hs" || message == "hsi" || message == "ht" || message == "sw")
			{
				samples = EQPy_get(ML);
				printf("Swift: samples: %s", samples);
				string confs[] = split(samples, ";");
				string results[];
				foreach conf, i in confs
				{
					int params[] = strarr2intarr(split(conf, ","));
					boolean vld_params;
					if (message == "lv") {
						vld_params = lv_chk_params(params);
					} else if (message == "lvi") {
						vld_params = lvi_chk_params(params);
					} else if (message == "lmp") {
						vld_params = lmp_chk_params(params);
					} else if (message == "vr") {
						vld_params = vr_chk_params(params);
					} else if (message == "hs") {
						vld_params = hs_chk_params(params);
					} else if (message == "hsi") {
						vld_params = hsi_chk_params(params);
					} else if (message == "ht") {
						vld_params = ht_chk_params(params);
					} else {  // message == "sw"
						vld_params = sw_chk_params(params);
					}
					if (vld_params) {
						float exectime[];
						if (message == "lv") {
							exectime[i] = lv_launch_wrapper("%0.4i_%0.2i_%0.1i_%0.3i_%0.4i_%0.2i_%0.1i" 
								% (params[0], params[1], params[2], params[3], params[4], params[5], params[6]), 
								params);
						} else if (message == "lvi") {
							exectime[i] = lvi_launch_wrapper("%0.5i_%0.5i_%0.4i_%0.2i_%0.1i_%0.3i_%0.4i_%0.2i_%0.1i" 
								% (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8]), 
								params);
						} else if (message == "lmp") {
							exectime[i] = lmp_launch_wrapper("%0.4i_%0.2i_%0.1i_%0.4i" 
								% (params[0], params[1], params[2], params[3]),
								params);
						} else if (message == "vr") {
							exectime[i] = vr_launch_wrapper("%0.4i_%0.2i_%0.1i_%0.4i"
								% (params[0], params[1], params[2], params[3]),
								params);
						} else if (message == "hs") {
							exectime[i] = hs_launch_wrapper("%0.2i_%0.2i_%0.2i_%0.2i_%0.2i_%0.4i_%0.2i"
								% (params[0], params[1], params[2], params[3], params[4], params[5], params[6]),
								params);
						} else if (message == "hsi") {
							exectime[i] = hsi_launch_wrapper("%0.4i_%0.4i_%0.4i_%0.2i_%0.2i_%0.2i_%0.2i_%0.2i_%0.4i_%0.2i"
								% (params[0], params[1], params[2], params[3], params[4],
								params[5], params[6], params[7], params[8], params[9]),
								params);
						} else if (message == "ht") {
							exectime[i] = ht_launch_wrapper("%0.2i_%0.2i_%0.2i_%0.2i_%0.2i"
								% (params[0], params[1], params[2], params[3], params[4]),
								params);
						} else {  // message == "sw"
							exectime[i] = sw_launch_wrapper("%0.4i_%0.2i_%0.2i"
								% (params[0], params[1], params[2]),
								params);
						}
						if (exectime[i] >= 0.0) {
							results[i] = float2string(exectime[i]);
						} else {
							results[i] = "inf";
						}
					} else {
						results[i] = "inf"; 
					}
				}
				result = join(results, ";");
				printf("Swift: result: %s", result);
				EQPy_put(ML, result) => c = true;
			}
		}
	}
}

main()
{
	algorithm = argv("algorithm");
	settings_filename = argv("settings");

	EQPy_init_package(ML, algorithm) =>
	handshake(settings_filename) =>
	loop() =>
	EQPy_stop();
}

