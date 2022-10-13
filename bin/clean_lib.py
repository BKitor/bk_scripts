import argparse
import re
import logging

# Should only have 1 group per pattern, relied on in --omb_full
GPD = {
    "alg": re.compile(r"^alg: (?P<alg>\d+)$"),
    "ar_segsize": re.compile(r"^ar_segsize: (?P<ar_segsize>\d+)$"),
    "bc_segsize": re.compile(r"^bc_segsize: (?P<bc_segsize>\d+)$"),
    "bk_mapping": re.compile(r"^bk_mapping: (?P<bk_mapping>\w+)$"),
    "bkpap_alg": re.compile(r"^bkpap_alg: (?P<bkpap_alg>\d+)$"),
    "bkpap_dplane": re.compile(r"^bkpap_dplane: (?P<bkpap_dplane>\d+)$"),
    "bkpap_prio": re.compile(r"^bkpap_prio: (?P<bkpap_prio>\d+)$"),
    "bkpap_seg_size": re.compile(r"^bkpap_seg_size: (?P<bkpap_seg_size>\d+)$"),
    "bkpap_flat": re.compile(r"^bkpap_flat: (?P<bkpap_flat>\d+)$"),
    "hcoll_en_sharp": re.compile(r"^HCOLL_ENABLE_SHARP=(?P<sharp>\d)$"),
    "hvd_cpu": re.compile(r"^Number of CPUs: (?P<ncpu>\w+)$"),
    "hvd_cycle_time": re.compile(r"^HOROVOD_CYCLE_TIME: (?P<hvd_cycle_time>\d+)$"),
    "hvd_gpu": re.compile(r"^Number of GPUs: (?P<ngpu>\w+)$"),
    "mif": re.compile(r"# BK OSU Allreduce MIF (?P<mif>\d+\.\d+)?"),
    "n_and_npernode": re.compile(r"^-n (?P<wsize>\d+) --npernode (?P<ppn>\d+)$"),
    "n_and_ppn": re.compile(r"^-n (?P<wsize>\d+) -ppn (?P<ppn>\d+)$"),
    # "omb_pattern_run": re.compile(r"^(?P<msize>\d+)\s+(?P<time>\d+\.\d+)$"),
    "ompi_hcoll_en": re.compile(r"^OMPI_MCA_coll_hcoll_enable=(?P<hcoll>\d)$"),
    "ompi_pml": re.compile(r"^OMPI_pml (?P<pml>\w+)$"),
    # "osu_p2p_memloc": re.compile(r"^# Send Buffer on \w+ \((?P<sloc>\w+)\) and Receive Buffer on \w+ \((?P<rloc>\w+)\)$"),
    "osu_p2p_type": re.compile(r"^# OSU MPI-CUDA (?P<type>[\w\s-]+) Test v\d+\.\d+$"),
    "remap_alg": re.compile(r"^remap_alg: (?P<remap_alg>\d+)$"),
    "remap_disabled": re.compile(r"^remap_disabled: (?P<remap_disabled>\d+)$"),
    "scotch_en": re.compile(r"^scotch_en: (?P<scotch_en>\d+)$"),
    "tuned_alg": re.compile(r"^tuned_alg: (?P<tuned_alg>\d+)$"),
    "ucc_en": re.compile(r"^ucc_enable: (?P<ucc_en>\d)$"),
    "ucc_tls": re.compile(r"^ucc_tls: (?P<ucc_tls>\w+)$"),
    "ucc_prio": re.compile(r"^ucc_prio: (?P<ucc_prio>\d+)$"),
    "ucx_proto_en": re.compile(r"^ucx_proto_en: (?P<ucx_proto_en>\w+)$"),
    #     "allreduce_alg": re.compile(r"^allreduce_alg: (?P<allreduce_alg>\d+)$"),
    #     "tuned_alg": re.compile(r"^tuned_alg: (?P<tuned_alg>\d+)$"),
}
hvd_pattern_cpu = GPD["hvd_cpu"]
hvd_pattern_gpu = GPD["hvd_gpu"]

pattern_sharp_en = GPD["hcoll_en_sharp"]
pattern_hcoll_en = GPD["ompi_hcoll_en"]
pattern_wsize_ppn = GPD["n_and_npernode"]

# omb_pattern_run = GPD["omb_pattern_run"]
omb_patters = {
    "default": re.compile(r"^(?P<msize>\d+)\s+(?P<avg_lat>\d+\.\d+)$"),
    "full": re.compile(r"^(?P<msize>\d+)\s+(?P<avg_lat>\d+\.\d+)\s+(?P<min_lat>\d+\.\d+)\s+(?P<max_lat>\d+\.\d+)\s+(?P<iters>\d+)$"),
}

omb_pap_pattern_mif = GPD["mif"]
omb_reset_pattern = re.compile(r"^# OSU MPI.*$")

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
    parser.add_argument("-g", "--group-by", type=str,
                        help="Group tables by specified regex-group")
    parser.add_argument("-p", "--pattern-lst", type=str,
                        help="Comma sepperated list of features to match (eg: mif,ucc_prio,ppn,wsize)")

    parser.add_argument("--omb_full", action="store_true")

    parser.add_argument("--cpu", action="store_true",
                        help="Parse horovod cpu runs")
    parser.add_argument("--gpu", action="store_true",
                        help="Parse horovod gpu runs")
    args = parser.parse_args()

    if args.num_folds < 1:
        logging.error(
            f"-n/--num-folds must be greater than 1, value given was {args.num_folds}")
        exit()

    if args.num_folds != 1 and args.group_by:
        logging.error(
            "-n/--num-folds and -g/--group-by are incompatible, set one or the other")
        exit()

    return args
