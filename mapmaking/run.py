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
#skyfile = {
#    30 : folder + "commander_tot_030_full_map_TQU_beta5.4_temp_alm.fits",
#    44 : folder + "commander_tot_044_full_map_TQU_beta5.4_temp_alm.fits",
#    70 : folder + "foregrounds_70_synchrotron_spindust_thermaldust_freefree_radiops_kineticsz_thermalsz_firb_irps_alm.fits"
#}

#cals = ["DX12_OSGN"] + ["M{}_FFP10SKY".format(i) for i in [0,1,3,4]] 
freqs = [30,44,70]
freqs = [30,44]
freqs = [70]
mcs = [1]
mcs=[0]
mcs = list(range(1, 10))

MAPS_TEMPLATE = "mc_maps_template.par"

for freq in freqs:
    for mc in mcs:
        #freq = int(sys.argv[1])

        mc = "{:04}".format(mc)
        chtags = all_chtags[freq]
        cal = "FFP10MC_{}".format(mc)
        #cal = "FFP10"
        tag = "{}_{}".format(freq, cal)
        maps_available = glob("ffp10_maps/{}/*/*{}*_map.fits".format(cal, freq))
        if len(maps_available) > 0:
            print("Skip", tag, freq)
        else:

            with open(MAPS_TEMPLATE) as f:
                par = f.read()
            par = par.format(
                    chtags=",".join(chtags), freq=freq,
                    cal=cal,
                    mc=mc
            )

            with open("temp/maps_{}.par".format(tag), 'w') as f:
                f.write(par)

            with open("slurm_template.sh") as f:
                slurm = f.read()

            slurm_filename = "temp/slurm_{}.sh".format(tag)

            with open(slurm_filename, 'w') as f:
                f.write(slurm.format(nodes=nodes[freq], tag=tag))

            subprocess.run(["sbatch", slurm_filename], check=True)
