#!/bin/bash -l

echo
echo "Setup and rebuild Swift/T with Python..."
echo

if (( ${#ROOT} == 0  ))
then
	echo "Set ROOT as the parent installation directory!"
	exit 1
fi

set -eu

# Setup Swift/T
cd swift-t
PYTHON_EXE=$( which python )
sed -i 's/^ENABLE_PYTHON=0/ENABLE_PYTHON=1/' dev/build/swift-t-settings.sh
sed -i 's@^PYTHON_EXE=.*$@PYTHON_EXE='"$PYTHON_EXE"'@' dev/build/swift-t-settings.sh

# Rebuild Swift/T
dev/build/build-swift-t.sh
cd ..

echo
echo "Swift/T with Python is done!"
echo

