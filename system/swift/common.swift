
(void v) setup_run_lmp(string dir, string infile1, string infile2, string infile3) "turbine" "0.0"
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

(void v) setup_run_ht(string dir, string infile) "turbine" "0.0"
[
"""
	file delete -force -- <<dir>>
	file mkdir <<dir>>
	cd <<dir>>
	file link -symbolic heat_transfer.xml <<infile>>
"""
];

(void v) setup_run2(string parDir, string srcDir, string dir) "turbine" "0.0"
[
"""
	file mkdir <<parDir>>
	file delete -force -- <<dir>>
	file copy -force -- <<srcDir>> <<dir>>
	cd <<dir>>
"""
];

(int int_params[]) strarr2intarr(string str_params[])
{
	foreach str_param, i in str_params
	{
		int_params[i] = string2int(str_params[i]);
	}
}
 
