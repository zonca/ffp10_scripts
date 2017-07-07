import sys
from glob import glob
import subprocess
import os

def make_chtags(first_horn, last_horn):
    return ["LFI{}{}".format(horn, side) for horn in range(first_horn, last_horn+1) for side in "MS"]

all_chtags = {
    30 : make_chtags(27, 28), 
    44 : make_chtags(24, 26), 
    70 : make_chtags(18, 23) 
}

nodes = {
    30 : 96,
    44 : 160,
    70 : 512
}
nodes = {
    30 : 64,
    44 : 85,
    70 : 350
}

folder = os.environ["SCRATCH"] + "/ringsets/"

freqs = [30, 44, 70]
freqs = [int(sys.argv[1])]

MAPS_TEMPLATE = "multi_mc_maps_template.par"

split_rings = {
    "survey1": {"ringfirst":"0", "ringlast":"5472"},
    "survey2": {"ringfirst":"5473", "ringlast":"10942"},
    "survey3": {"ringfirst":"10943", "ringlast":"16434"},
    "survey4": {"ringfirst":"16435", "ringlast":"21460"},
    "survey5": {"ringfirst":"21461", "ringlast":"27360"},
    "survey6": {"ringfirst":"27361", "ringlast":"32704"},
    "survey7": {"ringfirst":"32705", "ringlast":"38507"},
    "survey8": {"ringfirst":"38508", "ringlast":"43931"},
    "survey9": {"ringfirst":"43932", "ringlast":"45777"},
    "year1": {"ringfirst":"0", "ringlast":"10942"},
    "year2": {"ringfirst":"10943", "ringlast":"21460"},
    "year3": {"ringfirst":"21461", "ringlast":"32704"},
    "year4": {"ringfirst":"32705", "ringlast":"43931"},
    "year12": {"ringfirst":"0", "ringlast":"21460"},
    "year34": {"ringfirst":"21461", "ringlast":"43931"},
    "year13": {"ringfirst":"0,21461", "ringlast":"10942,32704"},
    "year24": {"ringfirst":"10943,32705", "ringlast":"21460,43931"},
    "odd": {"ringfirst":"0,10943,21461,32705", "ringlast":"5472,16434,27360,38507"},
    "even": {"ringfirst":"5473,16435,27361,38508", "ringlast":"10942,21460,32704,43931"},
    "full": {"ringfirst":"0", "ringlast":"43931"}
}

selected_splits = ["full"]#, "year13", "year24"]


MC_start = int(sys.argv[2])
MC_count = int(sys.argv[3])


for freq in freqs:
    for split in selected_splits:

            chtags = all_chtags[freq]
            cal = "FFP10MCS_{0:04}"
            tag = "{}_{}_{}".format(split, freq, MC_start)

            with open(MAPS_TEMPLATE) as f:
                par = f.read()
            par = par.format(
                    chtags=",".join(chtags), freq=freq,
                    cal=cal,
                    ringfirst=split_rings[split]["ringfirst"],
                    ringlast=split_rings[split]["ringlast"],
                    madam_prefix="ffp10_{}".format(split),
                    MC_start=MC_start,
                    MC_count=MC_count
            )

            with open("temp/maps_{}.par".format(tag), 'w') as f:
                f.write(par)

            with open("slurm_template.sh") as f:
                slurm = f.read()

            slurm_filename = "temp/slurm_{}.sh".format(tag)

            if nodes[freq] <= 256:
                partition = "regular"
                qos = "special_planck"
                hours=12
                account = "planck"
            else:
                partition = "regular"
                qos = "normal"
                hours=int( (15+MC_count*6) / 60 + 1)
                account = "m2798"
            partition_qos = """#SBATCH --partition={p}
#SBATCH --qos={q}
#SBATCH --time={hours}:00:00
#SBATCH --account={account}""".format(p=partition, q=qos, hours=hours, account=account)

            with open(slurm_filename, 'w') as f:
                f.write(slurm.format(nodes=nodes[freq], tag=tag, partition_qos=partition_qos))

            subprocess.run(["sbatch", slurm_filename], check=True)
