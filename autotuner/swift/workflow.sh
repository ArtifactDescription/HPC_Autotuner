#!/bin/bash
set -eu

# WORKFLOW SH
# Main user entry point

if [[ ${#} != 3 ]]
then
	echo "Usage: ./workflow.sh workflow_name algorithm experiment_id"
	exit 1
fi

WORKFLOW_SWIFT=$1.swift
WORKFLOW_TIC=${WORKFLOW_SWIFT%.swift}.tic

export EXPID=$3

# Turn off Swift/T debugging
export TURBINE_LOG=1 TURBINE_DEBUG=0 ADLB_DEBUG=0

# Find the directory of ./workflow.sh
export WORKFLOW_ROOT=$( cd $( dirname $0 ) ; /bin/pwd )
export T_PROJECT_ROOT=$( cd $WORKFLOW_ROOT/.. ; /bin/pwd )
cd $WORKFLOW_ROOT

# Set the output directory
export TURBINE_OUTPUT=$WORKFLOW_ROOT/experiment/$EXPID
mkdir -pv $TURBINE_OUTPUT
cp -f $WORKFLOW_ROOT/get_maxtime.sh $TURBINE_OUTPUT/get_maxtime.sh

cd $TURBINE_OUTPUT
cp -f ../lv_time.csv lv_time.csv
cp -f ../lvi_time.csv lvi_time.csv
cp -f ../lmp_time.csv lmp_time.csv
cp -f ../vr_time.csv vr_time.csv
cp -f ../in.quench in.quench
cp -f ../restart.liquid restart.liquid
cp -f ../CuZr.fs CuZr.fs
cp -f ../hs_time.csv hs_time.csv
cp -f ../hsi_time.csv hsi_time.csv
cp -f ../ht_time.csv ht_time.csv
cp -f ../sw_time.csv sw_time.csv
cp -f ../heat_transfer.xml heat_transfer.xml
cd -

# Total number of processes available to Swift/T
# Of these, 2 are reserved for the system
export PROCS=${PROCS:-18}
export PPN=1
export WALLTIME=10:00:00
export PROJECT=PACC
export QUEUE=bdw

EQP=$T_PROJECT_ROOT/ext/EQ-Py

export PYTHONPATH=$T_PROJECT_ROOT/python:$EQP
# Python packages can be installed and accessed from Swift/T as expected. You can also set the environment variable PYTHONPATH as desired, this will be picked up by the Swift/T features.

export TURBINE_RESIDENT_WORK_WORKERS=1
# Number of workers of this type

algorithm=$2
settings_file=$WORKFLOW_ROOT/settings.json

# Construct the command line given to Swift/T
CMD_LINE_ARGS=(	--algorithm=$algorithm
		--settings=$settings_file
	)

MACHINE="-m slurm" # -m (machine) option that accepts pbs, cobalt, cray, lsf, theta, or slurm. The empty string means the local machine.

ENVS="-e TURBINE_STDOUT=out-%r.txt" # "-e <key>=<value>" Set an environment variable in the job environment.

set -x
stc -p -O0 -I $EQP -r $EQP $WORKFLOW_ROOT/$WORKFLOW_SWIFT
# -p: Disable the C preprocessor
# -u: Only compile if target is not up-to-date

turbine -l $MACHINE -n $PROCS $ENVS $WORKFLOW_ROOT/$WORKFLOW_TIC ${CMD_LINE_ARGS[@]}

# -l: Enable mpiexec -l ranked output formatting
# -n <procs>: The total number of Turbine MPI processes

# swift-t -p -I $EQP -r $EQP -l $MACHINE -n $PROCS $ENVS $WORKFLOW_ROOT/$WORKFLOW_SWIFT ${CMD_LINE_ARGS[@]}
# -I <DIRECTORY>: Add an include path. TURBINE_HOME/export is always included to get standard library
# -r <DIRECTORY>: Add an RPATH for a Swift/T extension

echo WORKFLOW COMPLETE.

