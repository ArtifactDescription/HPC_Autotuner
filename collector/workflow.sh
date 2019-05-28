#!/bin/bash
set -eu

# WORKFLOW SH
# Main user entry point

if [[ ${#} != 2 ]]
then
	echo "Usage: ./workflow.sh workflow_name experiment_id"
	exit 1
fi

WORKFLOW_SWIFT=$1.swift
WORKFLOW_TIC=${WORKFLOW_SWIFT%.swift}.tic

export EXPID=$2

# Turn off Swift/T debugging
export TURBINE_LOG=0 TURBINE_DEBUG=0 ADLB_DEBUG=0

# Find the directory of ./workflow.sh
export WORKFLOW_ROOT=$( cd $( dirname $0 ) ; /bin/pwd )
cd $WORKFLOW_ROOT

# Set the output directory
export TURBINE_OUTPUT=$WORKFLOW_ROOT/experiment/$EXPID
mkdir -pv $TURBINE_OUTPUT
cp -f $WORKFLOW_ROOT/get_maxtime.sh $TURBINE_OUTPUT/get_maxtime.sh

if [[ $1 = "workflow-lv" ]]
then
	cd $TURBINE_OUTPUT
	cp -f ../conf_lv_smpls.csv conf_lv_smpls.csv
	cp -f ../../../autotuner/swift/experiment/in.quench in.quench
	cp -f ../../../autotuner/swift/experiment/restart.liquid restart.liquid
	cp -f ../../../autotuner/swift/experiment/CuZr.fs CuZr.fs
	cd -
fi

if [[ $1 = "workflow-lvi" ]]
then
	cd $TURBINE_OUTPUT
	cp -f ../conf_lvi_smpls.csv conf_lvi_smpls.csv
	cp -f ../../../autotuner/swift/experiment/in.quench in.quench
	cp -f ../../../autotuner/swift/experiment/restart.liquid restart.liquid
	cp -f ../../../autotuner/swift/experiment/CuZr.fs CuZr.fs
	cd -
fi

if [[ $1 = "workflow-lmp" ]]
then
	cd $TURBINE_OUTPUT
	cp -f ../conf_lmp_smpls.csv conf_lmp_smpls.csv
	cp -f ../conf_l_smpls.csv conf_l_smpls.csv
	cp -f ../../../autotuner/swift/experiment/in.quench in.quench
	cp -f ../../../autotuner/swift/experiment/restart.liquid restart.liquid
	cp -f ../../../autotuner/swift/experiment/CuZr.fs CuZr.fs
	cd -
fi

if [[ $1 = "workflow-vr" ]]
then
	cd $TURBINE_OUTPUT
	cp -f ../conf_vr_smpls.csv conf_vr_smpls.csv
	cp -f ../conf_v_smpls.csv conf_v_smpls.csv
	cd -
fi

if [[ $1 = "workflow-hs" ]]
then
	cd $TURBINE_OUTPUT
	cp -f ../conf_hs_smpls.csv conf_hs_smpls.csv
	cp -f ../../../autotuner/swift/experiment/heat_transfer.xml heat_transfer.xml
	cd -
fi

if [[ $1 = "workflow-hsi" ]]
then
	cd $TURBINE_OUTPUT
	cp -f ../conf_hsi_smpls.csv conf_hsi_smpls.csv
	cp -f ../../../autotuner/swift/experiment/heat_transfer.xml heat_transfer.xml
	cd -
fi

if [[ $1 = "workflow-ht" ]]
then
	cd $TURBINE_OUTPUT
	cp -f ../conf_ht_smpls.csv conf_ht_smpls.csv
	cp -f ../conf_h_smpls.csv conf_h_smpls.csv
	cp -f ../../../autotuner/swift/experiment/heat_transfer.xml heat_transfer.xml
	cd -
fi

if [[ $1 = "workflow-sw" ]]
then
	cd $TURBINE_OUTPUT
	cp -f ../conf_sw_smpls.csv conf_sw_smpls.csv
	cp -f ../conf_s_smpls.csv conf_s_smpls.csv
	cd -
fi

# Total number of processes available to Swift/T
# Of these, 2 are reserved for the system
export PROCS=34
export PPN=1
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

