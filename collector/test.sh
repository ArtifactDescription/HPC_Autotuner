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

export EXPID=$3
export PROCS=$(($2 + 2))		# The number of nodes
echo $PROCS
