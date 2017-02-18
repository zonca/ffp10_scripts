import sys
import subprocess

def make_chtags(first_horn, last_horn):
    return ["LFI{}{}".format(horn, side) for horn in range(first_horn, last_horn+1) for side in "MS"]

all_chtags = {
    30 : make_chtags(27, 28), 
    44 : make_chtags(24, 26), 
    70 : make_chtags(18, 23) 
}

nodes = {
    30 : 64,
    44 : 128,
    70 : 256
}

for freq in sorted(all_chtags.keys()):
    #freq = int(sys.argv[1])
    chtags = all_chtags[freq]
    for mc in [10]:
    #for mc in [0]:

        with open("ringsets_sim_mcnoise_dx12_template.par") as f:
            par = f.read()

        par = par.format(chtags=','.join(chtags), freq=freq, mc=mc)

        tag = "{}_{}".format(freq, mc)

        with open("temp/ringsets_dx12_{}.par".format(tag), 'w') as f:
            f.write(par)

        with open("slurm_template.sh") as f:
            slurm = f.read()

        with open("temp/slurm_{}.sh".format(tag), 'w') as f:
            f.write(slurm.format(nodes=nodes[freq], tag=tag))

        subprocess.run(["sbatch", "temp/slurm_{}.sh".format(tag)], check=True)
