#!/usr/bin/env python3
"""
Run a single Mininet TCP experiment using OVSKernelSwitch in standalone mode.
"""

import os
os.system("mn -c >/dev/null 2>&1")

import argparse
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSKernelSwitch
from mininet.log import setLogLevel, info


class CCTopo(Topo):
    """Simple 2-host dumbbell topology."""
    def build(self, bw, delay, queue, loss):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")

        # high-capacity access links
        self.addLink(h1, s1, cls=TCLink, bw=1000, delay="1ms")
        self.addLink(h2, s2, cls=TCLink, bw=1000, delay="1ms")

        # bottleneck link
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

    # NO controller; switches run in normal Ethernet mode
    net = Mininet(
        topo=topo,
        controller=None,
        switch=OVSKernelSwitch,
        link=TCLink,
        autoSetMacs=True,
        autoStaticArp=True
    )

    net.start()

    # Force each switch to standalone (L2 switching) mode
    for sw in net.switches:
        sw.cmd(f"ovs-vsctl set-fail-mode {sw.name} standalone")

    h1, h2 = net.get("h1", "h2")

    # Connectivity sanity check
    info("*** Testing connectivity\n")
    print(h1.cmd(f"ping -c 1 {h2.IP()}"))

    # Set congestion control algorithm
    for h in (h1, h2):
        h.cmd(f"sysctl -w net.ipv4.tcp_congestion_control={args.cc}")

    # Start iperf3 server
    server_log = f"{outdir}/server.json"
    h2.cmd(f"iperf3 -s -1 -J > {server_log} 2>&1 &")
    time.sleep(1)

    # Start iperf3 client
    client_log = f"{outdir}/client.json"
    info(f"*** Running iperf3 ({args.cc})\n")
    h1.cmd(f"iperf3 -c {h2.IP()} -t {args.time} -J > {client_log} 2>&1")

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
