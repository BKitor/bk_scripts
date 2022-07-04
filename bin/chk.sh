#!/usr/bin/bash

print_help(){
	echo "chk [-a/--salloc] [-q/--squeue] [-w/--watch] CLUSTER_1 CLUSTER_2..."
	echo "-a for idle nodes"
	echo "-q for jobs in the queue (set by default)"
	echo "-w to watch output (only works for -q)"
	echo "CLUSTER is a list of clusters <CLUSTER>.computecanada.ca"
	exit
}

while getopts "aqwh" BK_OPT; do
	case $BK_OPT in
	a)
		_flag_a=1
		;;
	q)
		_flag_q=1
		;;
	w)
		_flag_w=1
		;;
	h | : | \?)
		print_help
		;;
	*) print_help;;
	esac
done

PARAMS="${@:$OPTIND}"

if [ "" == "$_flag_a" -a "" == "$_flag_q" ]; then
	# _flag_a=1
	_flag_q=1
fi

PARAMS_ARRAY=($PARAMS)

if [ "" != "$_flag_w" ]; then
	watch -n 240 -c chk $PARAMS
	exit
fi

for CLUSTER in ${PARAMS_ARRAY[@]}; do
	echo "CHECKING CLUSTER : $CLUSTER"

	if [ "" != "$_flag_a" ]; then
		ssh $CLUSTER.computecanada.ca sinfo | grep idle
	fi

	if [ "" != "$_flag_q" ]; then
		CUR_FILE="$HOME/.chk_bak/chk_$CLUSTER-$(date +%s).txt"
		OLD_FILE="$(ls $HOME/.chk_bak/chk_$CLUSTER* | sort -n | tail -1)"
		ssh $CLUSTER.computecanada.ca squeue -u $USER -o '"%A %j %D %.9L %.20S %N"' | tee $CUR_FILE

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
