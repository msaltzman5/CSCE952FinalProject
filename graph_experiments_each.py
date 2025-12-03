#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS = "results/"
FIGURES_EACH = "figures/each/"

for folder in os.listdir(RESULTS):
    path = f"{RESULTS}{folder}/client.csv"
    if not os.path.exists(path):
        continue

    # Parse experiment parameters from folder name
    parts = folder.split("_")
    cc = parts[0]
    bw = parts[1].replace("bw", "")
    delay = parts[2].replace("d", "")
    queue = parts[3].replace("q", "")
    loss = parts[4].replace("l", "")
    round = parts[5].replace("r", "")

    # Load CSV
    df = pd.read_csv(path)

    # Plot throughput and retransmissions
    fig, ax1 = plt.subplots(figsize=(10,6))

    # Throughput
    ax1.plot(df['end'], df['throughput_mbps'], color='blue', label='Throughput (Mbps)')
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Throughput (Mbps)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Retransmissions on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(df['end'], df['retransmissions'], color='red', alpha=0.6, label='Retransmissions')
    ax2.set_ylabel("Retransmissions", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Title
    title = (f"{cc.upper()} Bandwidth={bw}Mbps | Delay={delay} | Max Queue={queue} | Loss Rate={loss} | Round={round}")
    plt.title(title)

    # Legends
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Ensure output directory exists
    EXPERIMENT = f"bw{bw}_d{delay}_q{queue}_l{loss}/"
    os.makedirs(f"{FIGURES_EACH}{EXPERIMENT}", exist_ok=True)

    # Save figure
    fig.tight_layout()
    outpath = f"{FIGURES_EACH}{EXPERIMENT}{cc}_throughput_retrans.png"
    plt.savefig(outpath)
    plt.close(fig)

    print(f"[SAVED] {outpath}")