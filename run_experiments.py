#!/usr/bin/env python3
"""
Run a batch of experiments over multiple congestion control algorithms
and link configurations by calling topo_cc.py with sudo.
"""

import subprocess
import itertools

# Congestion control algorithms to test
cc_algos = ["reno", "cubic", "bbr"]  # add "bbr2" or "tahoe" if available

# Link parameter grid
bws = [10, 50]           # Mbps
delays = ["20ms", "50ms"]
queues = [100, 200]      # packets
losses = [0.0, 1.0]      # percent

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
            "--loss", str(loss),
            "--time", "20",
        ]
        print("\n[RUN]", " ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"[WARN] Experiment FAILED for {cc}, bw={bw}, delay={delay}, queue={queue}, loss={loss}")


if __name__ == "__main__":
    run_all()
