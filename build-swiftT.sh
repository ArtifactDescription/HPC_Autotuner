#!/bin/bash -l

echo
echo "Swift/T starts ..."
echo

if (( ${#ROOT} == 0  ))
then
	echo "Set ROOT as the parent installation directory!"
	exit 1
fi

if [ -d $ROOT ]
then
	mkdir -pv $ROOT/swift-t-install
else 
	echo "There does not exist $ROOT!"
	exit 1
fi

# echo "Loading Modules ..."
# module load intel/17.0.4-74uvhji
# module load jdk/8u141-b15-mopj6qr
# module load tcl/8.6.6-x4wnbsg
# echo "Modules are loaded!"

set -eu

# Download Java
# wget --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u192-b12/750e1c8617c5452694857ad95c3ee230/jdk-8u192-linux-x64.tar.gz
# if [ -d $ROOT/jdk1.8.0_192 ]
# then
#	rm -rv $ROOT/jdk1.8.0_192
# fi
# tar -zxvf jdk-8u192-linux-x64.tar.gz -C $ROOT
# export JAVA_HOME=$ROOT/jdk1.8.0_192
# export PATH=$JAVA_HOME/bin:$PATH
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$JAVA_HOME/lib

# Download Ant
if [ -f apache-ant-1.10.5-bin.tar.gz ]
then
	rm -fv apache-ant-1.10.5-bin.tar.gz
fi
if wget -q https://www.apache.org/dist/ant/binaries/apache-ant-1.10.5-bin.tar.gz
then
	echo WARNING: wget exited with: $?
fi
if [ -d $ROOT/apache-ant-1.10.5 ]
then
        rm -rf $ROOT/apache-ant-1.10.5
fi
tar -zxvf apache-ant-1.10.5-bin.tar.gz -C $ROOT
source ./env_ant.sh
# export ANT_HOME=$ROOT/apache-ant-1.10.5
# export PATH=$ANT_HOME/bin:$PATH
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ANT_HOME/lib

echo
echo "Delete and then download Swift/T ..."
if [ -d swift-t ]
then
        rm -rf swift-t
fi
git clone https://github.com/swift-lang/swift-t.git

# Setup swift-t
cd swift-t
dev/build/init-settings.sh
sed -i 's/^export SWIFT_T_PREFIX=\/tmp\/swift-t-install$/export SWIFT_T_PREFIX='"${ROOT//\//\\/}"'\/swift-t-install/' dev/build/swift-t-settings.sh

echo
echo "Build Swift/T ..."
dev/build/build-swift-t.sh

cd ..

source ./env_swiftT.sh
# export SWIFT_T_HOME=$ROOT/swift-t-install
# export PATH=$SWIFT_T_HOME/turbine/bin:$SWIFT_T_HOME/stc/bin:$PATH

echo
echo "Swift/T is done!"
echo

