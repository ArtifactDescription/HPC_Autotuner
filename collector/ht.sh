#!/bin/bash

METHOD=$1
BUFFER=$2
FILE=$3

export PWD=$( cd $( dirname $0 ) ; /bin/pwd )

if [[ $METHOD = "FLEXPATH" ]]
then
	sed -i 's@^<!-- <method group="heat" method="FLEXPATH">QUEUE_SIZE=4;verbose=3</method> -->$@  <method group="heat" method="FLEXPATH">QUEUE_SIZE=4;verbose=3</method>@' $FILE
	sed -i 's@^  <method group="heat" method="MPI"/>$@<!-- <method group="heat" method="MPI"/> -->@' $FILE
	sed -i 's@^  <method group="heat" method="MPI_AGGREGATE">num_aggregators=4;num_ost=2;have_metadata_file=1;verbose=3</method>$@<!-- <method group="heat" method="MPI_AGGREGATE">num_aggregators=4;num_ost=2;have_metadata_file=1;verbose=3</method> -->@' $FILE
	sed -i 's@^  <method group="heat" method="DATASPACES"/>$@<!-- <method group="heat" method="DATASPACES"/> -->@' $FILE
fi

if [[ $METHOD = "MPI" ]]
then
	sed -i 's@^<!-- <method group="heat" method="MPI"/> -->$@  <method group="heat" method="MPI"/>@' $FILE
	sed -i 's@^  <method group="heat" method="FLEXPATH">QUEUE_SIZE=4;verbose=3</method>$@<!-- <method group="heat" method="FLEXPATH">QUEUE_SIZE=4;verbose=3</method> -->@' $FILE
	sed -i 's@^  <method group="heat" method="MPI_AGGREGATE">num_aggregators=4;num_ost=2;have_metadata_file=1;verbose=3</method>$@<!-- <method group="heat" method="MPI_AGGREGATE">num_aggregators=4;num_ost=2;have_metadata_file=1;verbose=3</method> -->@' $FILE
	sed -i 's@^  <method group="heat" method="DATASPACES"/>$@<!-- <method group="heat" method="DATASPACES"/> -->@' $FILE
fi

if [[ $METHOD = "MPI_AGGREGATE" ]]
then
	sed -i 's@^<!-- <method group="heat" method="MPI_AGGREGATE">num_aggregators=4;num_ost=2;have_metadata_file=1;verbose=3</method> -->$@  <method group="heat" method="MPI_AGGREGATE">num_aggregators=4;num_ost=2;have_metadata_file=1;verbose=3</method>@' $FILE
	sed -i 's@^  <method group="heat" method="FLEXPATH">QUEUE_SIZE=4;verbose=3</method>$@<!-- <method group="heat" method="FLEXPATH">QUEUE_SIZE=4;verbose=3</method> -->@' $FILE
	sed -i 's@^  <method group="heat" method="MPI"/>$@<!-- <method group="heat" method="MPI"/> -->@' $FILE
	sed -i 's@^  <method group="heat" method="DATASPACES"/>$@<!-- <method group="heat" method="DATASPACES"/> -->@' $FILE
fi

if [[ $METHOD = "DATASPACES" ]]
then
	sed -i 's@^<!-- <method group="heat" method="DATASPACES"/> -->$@  <method group="heat" method="DATASPACES"/>@' $FILE
	sed -i 's@^  <method group="heat" method="FLEXPATH">QUEUE_SIZE=4;verbose=3</method>$@<!-- <method group="heat" method="FLEXPATH">QUEUE_SIZE=4;verbose=3</method> -->@' $FILE
	sed -i 's@^  <method group="heat" method="MPI"/>$@<!-- <method group="heat" method="MPI"/> -->@' $FILE
	sed -i 's@^  <method group="heat" method="MPI_AGGREGATE">num_aggregators=4;num_ost=2;have_metadata_file=1;verbose=3</method>$@<!-- <method group="heat" method="MPI_AGGREGATE">num_aggregators=4;num_ost=2;have_metadata_file=1;verbose=3</method> -->@' $FILE
fi

sed -i 's@^  <buffer max-size-MB=".*"/>$@  <buffer max-size-MB="'"$BUFFER"'"/>@' $FILE

