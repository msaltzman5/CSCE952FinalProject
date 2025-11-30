#!/usr/bin/env python3

import subprocess
import itertools

cc_algos = ["reno", "cubic", "bbr"]  # Add 'tahoe' if your kernel supports it
bws = [10, 50]
delays = ["20ms", "50ms"]
queues = [100, 200]
losses = [0, 1]

def run_all():
    for cc, bw, delay, queue, loss in itertools.product(
        cc_algos, bws, delays, queues, losses
    ):
        cmd = [
            "sudo", "python3", "topo_cc.py",
            "--cc", cc,
            "--bw", str(bw),
            "--delay", delay,
            "--queue", str(queue),
            "--loss", str(loss)
        ]
        print("\n[RUN]", " ".join(cmd))
        subprocess.run(cmd)

if __name__ == "__main__":
    run_all()
