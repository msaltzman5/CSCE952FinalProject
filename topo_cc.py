#!/usr/bin/env python3
import argparse
import os
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.log import setLogLevel, info

class CCTopo(Topo):
    def build(self, bw, delay, queue, loss):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")

        # high-bandwidth access links
        self.addLink(h1, s1, cls=TCLink, bw=1000, delay="1ms")
        self.addLink(h2, s2, cls=TCLink, bw=1000, delay="1ms")

        # bottleneck
        self.addLink(
            s1, s2,
            cls=TCLink,
            bw=bw,
            delay=delay,
            max_queue_size=queue,
            loss=loss
        )

def run_experiment(args):
    outdir = f"results/{args.cc}_bw{args.bw}_d{args.delay}_q{args.queue}_l{args.loss}"
    os.makedirs(outdir, exist_ok=True)

    topo = CCTopo(args.bw, args.delay, args.queue, args.loss)
    net = Mininet(topo=topo, controller=OVSController, link=TCLink)
    net.start()

    h1, h2 = net.get("h1", "h2")

    # Set CC algorithm
    for h in (h1, h2):
        h.cmd(f"sysctl -w net.ipv4.tcp_congestion_control={args.cc}")

    # Start iperf3 server
    server_log = f"{outdir}/server.json"
    h2.cmd(f"iperf3 -s -J > {server_log} &")
    time.sleep(1)

    # Run client
    client_log = f"{outdir}/client.json"
    info(f"*** Running iperf3 using {args.cc}\n")
    h1.cmd(f"iperf3 -c {h2.IP()} -t {args.time} -J > {client_log}")

    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    p = argparse.ArgumentParser()
    p.add_argument("--cc", required=True)
    p.add_argument("--bw", type=int, required=True)
    p.add_argument("--delay", required=True)
    p.add_argument("--queue", type=int, required=True)
    p.add_argument("--loss", type=float, required=True)
    p.add_argument("--time", type=int, default=20)
    run_experiment(p.parse_args())
