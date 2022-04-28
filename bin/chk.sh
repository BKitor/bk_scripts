#!/usr/bin/bash

PARAMS=""
while (("$#")); do
	case "$1" in 
		-a|--salloc)
			_flag_a=1
			shift
			;;
		-q|--squeue)
			_flag_q=1
			shift
			;;
		-h|--help)
			_flag_h=1
			shift
			;;
		-w|--watch)
			_flag_w=1
			shift
			;;
		-*|--*)
			echo "ERROR: bad flag $1"
			echo
			_flag_h=1
			shift
			;;
		*)
			PARAMS="$PARAMS $1"
			shift
			;;
	esac
done


if [ "" != "$_flag_h" ]; then
 	echo "chk [-a/--salloc] [-q/--squeue] [-w/--watch] CLUSTER_1 CLUSTER_2..."
 	echo "$a_arg for avail gpu nodes"
 	echo "$q_arg for jobs in the queue"
 	echo "CLUSTER is a list of clusters <CLUSTER>.computecanada.ca"
 	exit
fi

if [ "" == "$_flag_a" -a "" == "$_flag_q" ]; then
			# _flag_a=1
			_flag_q=1
fi

PARAMS_ARRAY=($PARAMS)

if [ "" != "$_flag_w" ]; then
	watch -n 180 -c chk $PARAMS
	exit
fi

for CLUSTER in ${PARAMS_ARRAY[@]}; do
	echo "CHECKING CLUSTER : $CLUSTER"

	if [ "" != "$_flag_a" ]; then
 		ssh $CLUSTER.computecanada.ca sinfo | grep interac
	fi

	if [ "" != "$_flag_q" ]; then
 		CUR_FILE="$HOME/.chk_bak/chk_$CLUSTER-$(date +%s).txt"
 		OLD_FILE="$(ls $HOME/.chk_bak/chk_$CLUSTER* | sort -n | tail -1)"
 		ssh $CLUSTER.computecanada.ca squeue -u $USER -o '"%A %j %D %.9L %.20e %N"' | tee $CUR_FILE
 
 		if [ $? -ne 0 ]; then
 			echo "cluser $cluster failed"
 			continue
		fi
 
 		echo "***DIFFS****"
 		diff --color=always $OLD_FILE $CUR_FILE | tee "$HOME/.chk_bak/last_diff_$cluster.txt"
 		rm $OLD_FILE
 		echo "*******"
	fi
done	

