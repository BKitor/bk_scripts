#!/usr/bin/bash

# fetch a set of files form a CC cluster
# coppies `fetch.txt` from the home directory of 
# $cluster. `fetch.txt` is a list of files to be coppied over
# the files in fetch are then coppies into a local `./fetch` dir

if [ "0" == $# ]; then
	echo "pass in an argument for the cluster"
	echo "fetch <beluga|cedar|graham>"
	return
fi

mkdir ./fetch
pushd fetch

if [ "mist" == $1 -o "niagara" == $1 ];then
	CLUSTER_HOME="/gpfs/fs1/home/q/queenspp/bkitor"
else
	CLUSTER_HOME="/home/bkitor"
fi

scp $1.computecanada.ca:$CLUSTER_HOME/fetch.txt .

if [ $? -ne 0 ]; then
	echo "ERROR, coulding get fetch.txt"
	echo "scp $cluster.computecanada.ca:/home/bkitor/fetch.txt ."
	popd 
	exit
fi

for f in $(cat fetch.txt); do
	echo "fetching $f"
	scp -r $1.computecanada.ca:$f . &
done

wait

rm fetch.txt
popd
echo "SUCCESS"
