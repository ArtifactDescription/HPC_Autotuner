#!/bin/bash
set -eu

# WORKFLOW SH
# Main user entry point

if [[ ${#} != 3 ]]
then
	echo "Usage: ./workflow.sh workflow_name num_nodes experiment_id"
	exit 1
fi

WORKFLOW_SWIFT=$1.swift
WORKFLOW_TIC=${WORKFLOW_SWIFT%.swift}.tic

export EXPID=$3

# Turn off Swift/T debugging
export TURBINE_LOG=0 TURBINE_DEBUG=0 ADLB_DEBUG=0

# Find the directory of ./workflow.sh
export WORKFLOW_ROOT=$( cd $( dirname $0 ) ; /bin/pwd )
cd $WORKFLOW_ROOT

if [[ $1 = "lmp" ]]
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_lv/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_lmp.csv smpl_lmp.csv
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/in.quench in.quench
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/restart.liquid restart.liquid
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/CuZr.fs CuZr.fs
	cd -
fi

if [[ $1 = "vr" ]]
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_lv/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_vr.csv smpl_vr.csv
	cd -
fi

if [[ $1 = "lv" ]]
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_lv/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_lv.csv smpl_lv.csv
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/in.quench in.quench
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/restart.liquid restart.liquid
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/CuZr.fs CuZr.fs
	cd -
fi

if [[ $1 = "lvi" ]]
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_lv/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_lv.csv smpl_lv.csv
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/in.quench in.quench
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/restart.liquid restart.liquid
	cp -f ../../../adios1-coupled/Example-LAMMPS/swift-all/CuZr.fs CuZr.fs
	cd -
fi

if [[ $1 = "ht" ]]
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_hs/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_ht.csv smpl_ht.csv
	cp -f ../../../adios1-coupled/Example-Heat_Transfer/heat_transfer.xml heat_transfer.xml
	cd -
fi

if [[ $1 = "sw" ]]
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_hs/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_sw.csv smpl_sw.csv
	cd -
fi

if [[ $1 = "hs" ]]
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_hs/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_hs.csv smpl_hs.csv
	cp -f ../../../adios1-coupled/Example-Heat_Transfer/heat_transfer.xml heat_transfer.xml
	cd -
fi

if [[ $1 = "hsi" ]]
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_hs/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_hs.csv smpl_hs.csv
	cp -f ../../../adios1-coupled/Example-Heat_Transfer/heat_transfer.xml heat_transfer.xml
	cd -
fi

if [[ $1 = "gs" ]]	# Gray-Scott
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_bp4/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_gs.csv smpl_gs.csv
	cp -f ../settings-files.json settings-files.json
	cp -f ../adios2.xml adios2.xml
	cd -
fi

if [[ $1 = "pdf" ]]	# PDF Calculator
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_bp4/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_pdf.csv smpl_pdf.csv
	cp -f ../adios2.xml adios2.xml
	cd -
fi

if [[ $1 = "pplot" ]] || [[ $1 = "gplot" ]]	# PDF Plot or Gray Plot
then
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_bp4/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_plot.csv smpl_plot.csv
	cp -f ../adios2.xml adios2.xml
	cd -
fi

if [[ $1 = "gp" ]]	# Gray-Scott and PDF Calculator coupled
then
	# Set the output directory
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_sst/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_gp.csv smpl_gp.csv
	cp -f ../settings-staging.json settings-staging.json
	cp -f ../adios2-gp.xml adios2.xml
	cd -
fi

if [[ $1 = "gv" ]]	# Gray-Scott and Gray Plot coupled
then
	# Set the output directory
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_sst/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_gv.csv smpl_gs.csv
	cp -f ../settings-staging.json settings-staging.json
	cp -f ../adios2-gp.xml adios2.xml
	cd -
fi

if [[ $1 = "gpv" ]]	# Gray-Scott, PDF Calculator, and PDF Plot coupled
then
	# Set the output directory
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_sst/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_gp.csv smpl_gp.csv
	cp -f ../settings-staging.json settings-staging.json
	cp -f ../adios2-gpv.xml adios2.xml
	cd -
fi

if [[ $1 = "wf" ]]	# Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot coupled
then
	# Set the output directory
	export TURBINE_OUTPUT=$WORKFLOW_ROOT/exp_sst/$EXPID
	mkdir -pv $TURBINE_OUTPUT
	cd $TURBINE_OUTPUT
	cp -f ../num_smpl.txt num_smpl.txt
	cp -f ../smpl_gp.csv smpl_gp.csv
	cp -f ../settings-staging.json settings-staging.json
	cp -f ../adios2.xml adios2.xml
	cd -
fi

if (( ${#TURBINE_OUTPUT} == 0  ))
then
	echo "Set TURBINE_OUTPUT as the output directory!"
	exit 1
fi

cp -f $WORKFLOW_ROOT/get_maxtime.sh $TURBINE_OUTPUT/get_maxtime.sh

# Total number of processes available to Swift/T
# Of these, 2 are reserved for the system
export PROCS=$(($2 + 2))	# The number of nodes
export PPN=1			# fixed as 1
export WALLTIME=01:00:00
export PROJECT=PACC
export QUEUE=bdw
MACHINE="-m slurm" # -m (machine) option that accepts pbs, cobalt, cray, lsf, theta, or slurm. The empty string means the local machine.

ENVS="" # "-e <key>=<value>" Set an environment variable in the job environment.

set -x
stc -p -O0 $WORKFLOW_ROOT/$WORKFLOW_SWIFT
# -p: Disable the C preprocessor
# -u: Only compile if target is not up-to-date

turbine -l $MACHINE -n $PROCS $ENVS $WORKFLOW_ROOT/$WORKFLOW_TIC
# -l: Enable mpiexec -l ranked output formatting
# -n <procs>: The total number of Turbine MPI processes

#swift-t -l $MACHINE -p -n $PROCS $ENVS $WORKFLOW_ROOT/workflow.swift

echo WORKFLOW COMPLETE.

