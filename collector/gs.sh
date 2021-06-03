#!/bin/bash

CS=$1
STP=$2
FILE=$3

export PWD=$( cd $( dirname $0 ) ; /bin/pwd )
sed -i 's/^    "L": .*,$/    "L": '"$CS"',/' $FILE
sed -i 's/^    "steps": .*,$/    "steps": '"$STP"',/' $FILE

