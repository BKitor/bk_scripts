import argparse
import re
import logging

GPD = {
    "hvd_cpu": re.compile(r"^Number of CPUs: (?P<ncpu>\w+)$"),
    "hvd_gpu": re.compile(r"^Number of GPUs: (?P<ngpu>\w+)$"),
    "hcoll_en_sharp": re.compile(r"^HCOLL_ENABLE_SHARP=(?P<sharp>\d)$"),
    "ompi_hcoll_en": re.compile(r"^OMPI_MCA_coll_hcoll_enable=(?P<hcoll>\d)$"),
    "bkpap_prio": re.compile(r"^bkpap_prio: (?P<bkpap_prio>\d+)$"),
    "bkpap_alg": re.compile(r"^bkpap_alg: (?P<bkpap_alg>\d+)$"),
    "tuned_alg": re.compile(r"^tuned_alg: (?P<tuned_alg>\d+)$"),
    "allreduce_alg": re.compile(r"^allreduce_alg: (?P<allreduce_alg>\d+)$"),
    "n_and_npernode": re.compile(r"^-n (?P<wsize>\d+) --npernode (?P<ppn>\d+)$"),
    "n_and_ppn": re.compile(r"^-n (?P<wsize>\d+) -ppn (?P<ppn>\d+)$"),
    "omb_pattern_run": re.compile(r"^(?P<msize>\d+)\s+(?P<time>\d+\.\d+)$"),
    "mif": re.compile(r"# BK OSU Allreduce MIF (?P<mif>\d+\.\d+)?"),
    "ucc_prio": re.compile(r"^ucc_prio: (?P<ucc_prio>\d+)$"),
    "ucc_en": re.compile(r"^ucc_enable: (?P<ucc_en>\d)$"),
    "ompi_pml": re.compile(r"^OMPI_pml (?P<pml>\w+)$"),
    "hvd_cycle_time": re.compile(r"^HOROVOD_CYCLE_TIME: (?P<hvd_cycle_time>\d+)$"),
    "osu_p2p_memloc": re.compile(
        r"^# Send Buffer on \w+ \((?P<sloc>\w+)\) and Receive Buffer on \w+ \((?P<rloc>\w+)\)$"),
    # misses 'Bi-Directinoal Bandwithd'
    "osu_p2p_type": re.compile(r"^# OSU MPI-CUDA (?P<type>[\w]+) Test v5\.\d+$"),
}
hvd_pattern_cpu = GPD["hvd_cpu"]
hvd_pattern_gpu = GPD["hvd_gpu"]

pattern_sharp_en = GPD["hcoll_en_sharp"]
pattern_hcoll_en = GPD["ompi_hcoll_en"]
pattern_wsize_ppn = GPD["n_and_npernode"]

omb_pattern_run = GPD["omb_pattern_run"]
omb_pap_pattern_mif = GPD["mif"]

hvd_pattern_base = [
    re.compile(r"^Model: (?P<model>\w+)$"),
    re.compile(r"^Batch size: (?P<bsize>\d+)$"),
    re.compile(
        r"^Total img/sec.* (?P<avg_perf>\d+\.\d) \+-(?P<avg_perf_err>\d+\.\d)$"),
]


def get_patterns_from_str(pat_str):
    ret_arr = []
    pattern_arr = pat_str.split(",")
    for p in pattern_arr:
        if p not in GPD:
            logging.error(f"pattern {p} not found, exiting")
            exit()
        ret_arr.append(GPD[p])

    # logging.info(ret_arr)
    return ret_arr


# 
def gen_match_help_str(pattern_dict):
    ret_str = "Available patterns:\n"
    max_len_str = max(map(lambda x: len(x), pattern_dict.keys()))
    for k, v in pattern_dict.items():
        ret_str += f'"{k:{max_len_str}}" : {v.pattern:s}\n'

    return ret_str


def parse_inputs():
    parser = argparse.ArgumentParser(epilog=gen_match_help_str(
        GPD), formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("FILE")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable DEBUG level logging")
    parser.add_argument("-n", "--num-folds", type=int, default=1,
                        help="How many experiments to fold into the output")
    parser.add_argument("-g", "--fold-by", type=str,
                        help="Group tables by specified regex-group")
    parser.add_argument("-p", "--pattern-lst", type=str,
                        help="Comma sepperated list of features to match (eg: mif,ucc_prio,ppn,wsize)")

    parser.add_argument("--cpu", action="store_true",
                        help="Parse horovod cpu runs")
    parser.add_argument("--gpu", action="store_true",
                        help="Parse horovod gpu runs")
    args = parser.parse_args()

    if args.num_folds < 1:
        logging.error(
            f"-n/--num-folds must be greater than 1, value given was {args.num_folds}")
        exit()

    if args.num_folds != 1 and args.fold_by:
        logging.error(
            "-n/--num-folds and -g/--group-by are incompatible, set one or the other")
        exit()

    return args
