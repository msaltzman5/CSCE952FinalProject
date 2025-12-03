import subprocess
import itertools

cc_algos = ["reno", "cubic", "bbr"] 

# Extremes for each parameter
bws = [10, 50]            # Mbps (low/high)
delays = ["20ms", "50ms"] # low/high
queues = [100, 200]       # small/large
losses = [0.0, 0.1, 1.0]       # none/a tad/high

def run_cmd(cc, bw, delay, queue, loss, repeat=1):
    """Run topo_cc.py with given parameters, repeat if requested."""
    for i in range(repeat):
        cmd = [
            "sudo", "python3", "topo_cc.py",
            "--cc", cc,
            "--bw", str(bw),
            "--delay", delay,
            "--queue", str(queue),
            "--loss", str(loss),
            "--time", "20",
            "--round", str(i)
        ]
        print(f"\n[RUN {i+1}/{repeat}] {' '.join(cmd)}")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"[WARN] Experiment FAILED for {cc}, bw={bw}, delay={delay}, queue={queue}, loss={loss}")

def run_all():
    for cc, bw, delay, queue, loss in itertools.product(cc_algos, bws, delays, queues, losses):
        run_cmd(cc, bw, delay, queue, loss, repeat=5)

if __name__ == "__main__":
    run_all()