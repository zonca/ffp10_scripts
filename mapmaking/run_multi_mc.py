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
    30 : 128,
    44 : 128,
    70 : 512
}

folder = os.environ["SCRATCH"] + "/ringsets/"

freqs = [30]

MAPS_TEMPLATE = "multi_mc_maps_template.par"

for freq in freqs:

        chtags = all_chtags[freq]
        cal = "FFP10MC_{0:04}"
        tag = "{}".format(freq)

        with open(MAPS_TEMPLATE) as f:
            par = f.read()
        par = par.format(
                chtags=",".join(chtags), freq=freq,
                cal=cal,
        )

        with open("temp/maps_{}.par".format(tag), 'w') as f:
            f.write(par)

        with open("slurm_template.sh") as f:
            slurm = f.read()

        slurm_filename = "temp/slurm_{}.sh".format(tag)

        if nodes[freq] <= 256:
            partition = "regular"
            qos = "special_planck"
        else:
            partition = "regular"
            qos = "premium"
        partition_qos = """#SBATCH --partition={p}
#SBATCH --qos={q}""".format(p=partition, q=qos)

        with open(slurm_filename, 'w') as f:
            f.write(slurm.format(nodes=nodes[freq], tag=tag, partition_qos=partition_qos))

        subprocess.run(["sbatch", slurm_filename], check=True)
