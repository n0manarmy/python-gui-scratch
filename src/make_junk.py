import subprocess
import random
import sys

dst = sys.argv[2]

for x in range(1,101):
    comm = subprocess.Popen(
        ["dd", "if=/dev/urandom", 
         "of=" + dst + "/{}.junk".format(x), 
         "bs=1M", 
         "count={}".format(random.randrange(10,100))])