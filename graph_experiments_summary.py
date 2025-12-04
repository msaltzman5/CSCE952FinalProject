#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

RESULTS = "results/"
FIGURES_SUMMARY = "figures/summary/"

# Collect data grouped by experiment parameters
experiments = defaultdict(lambda: defaultdict(list))

for folder in os.listdir(RESULTS):
    path = f"{RESULTS}{folder}/client.csv"
    if not os.path.exists(path):
        continue

    # Parse experiment parameters from folder name
    parts = folder.split("_")
    cc_raw = parts[0].lower()
    cc = cc_raw.upper()   # normalize to uppercase

    bw = parts[1].replace("bw", "")
    delay = parts[2].replace("d", "")
    queue = parts[3].replace("q", "")
    loss = parts[4].replace("l", "")
    round = parts[5].replace("r", "")

    key = (bw, delay, queue, loss)  # experiment condition
    df = pd.read_csv(path)
    experiments[key][cc].append(df)

# Colors for CCs
colors = {"RENO": "blue", "CUBIC": "green", "BBR": "red"}

# Plot summary for each experiment condition
for key, cc_runs in experiments.items():
    bw, delay, queue, loss = key

    EXPERIMENT = f"bw{bw}_d{delay}_q{queue}_l{loss}/"
    os.makedirs(f"{FIGURES_SUMMARY}{EXPERIMENT}", exist_ok=True)

    # --- Time-series plot WITHOUT retransmissions ---
    fig_no, ax_no = plt.subplots(figsize=(10, 6))
    for cc, runs in cc_runs.items():
        merged = pd.concat(runs)
        merged["end_bin"] = merged["end"].round(0)

        mean_t = merged.groupby("end_bin")["throughput_mbps"].mean().reset_index()
        std_t = merged.groupby("end_bin")["throughput_mbps"].std().reset_index()

        ax_no.plot(mean_t["end_bin"], mean_t["throughput_mbps"],
                   color=colors.get(cc, "black"), label=f"{cc} Throughput")
        ax_no.fill_between(mean_t["end_bin"],
                           mean_t["throughput_mbps"] - std_t["throughput_mbps"],
                           mean_t["throughput_mbps"] + std_t["throughput_mbps"],
                           color=colors.get(cc, "black"), alpha=0.2)

    ax_no.set_xlabel("Time (s)")
    ax_no.set_ylabel("Throughput (Mbps)")
    ax_no.set_title(f"Bandwidth={bw}Mbps | Delay={delay} | Max Queue={queue} | Loss Rate={loss}")
    ax_no.legend()

    outpath_no = f"{FIGURES_SUMMARY}{EXPERIMENT}throughput.png"
    fig_no.tight_layout()
    plt.savefig(outpath_no)
    plt.close(fig_no)
    print(f"[SAVED] {outpath_no}")

    # --- Time-series plot WITH retransmissions overlay ---
    fig_yes, ax_yes = plt.subplots(figsize=(10, 6))
    ax2 = ax_yes.twinx()
    ax_yes.set_xlabel("Time (s)")
    ax_yes.set_ylabel("Throughput (Mbps)")
    ax2.set_ylabel("Retransmissions per interval")

    for cc, runs in cc_runs.items():
        merged = pd.concat(runs)
        merged["end_bin"] = merged["end"].round(0)

        mean_t = merged.groupby("end_bin")["throughput_mbps"].mean().reset_index()
        std_t = merged.groupby("end_bin")["throughput_mbps"].std().reset_index()
        mean_r = merged.groupby("end_bin")["retransmissions"].mean().reset_index()

        ax_yes.plot(mean_t["end_bin"], mean_t["throughput_mbps"],
                    color=colors.get(cc, "black"), label=f"{cc} Throughput")
        ax_yes.fill_between(mean_t["end_bin"],
                            mean_t["throughput_mbps"] - std_t["throughput_mbps"],
                            mean_t["throughput_mbps"] + std_t["throughput_mbps"],
                            color=colors.get(cc, "black"), alpha=0.2)

        ax2.plot(mean_r["end_bin"], mean_r["retransmissions"],
                 color=colors.get(cc, "black"), linestyle="--", alpha=0.5,
                 label=f"{cc} Retrans")

    ax_yes.set_title(f"Bandwidth={bw}Mbps | Delay={delay} | Max Queue={queue} | Loss Rate={loss}")

    # Combine legends
    lines1, labels1 = ax_yes.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax_yes.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    outpath_yes = f"{FIGURES_SUMMARY}{EXPERIMENT}throughput_retrans.png"
    fig_yes.tight_layout()
    plt.savefig(outpath_yes)
    plt.close(fig_yes)
    print(f"[SAVED] {outpath_yes}")

    # --- Aggregated bar chart of retransmission rate ---
    fig_bar, ax_bar = plt.subplots(figsize=(8, 5))
    names, means, stds = [], [], []

    for cc, runs in cc_runs.items():
        totals = []
        for df in runs:
            total_retrans = df["retransmissions"].sum()
            total_bits = ((df["throughput_mbps"] * 1e6) * (df["end"] - df["start"])).sum()
            total_mb = total_bits / 8 / 1e6
            norm = total_retrans / total_mb if total_mb > 0 else np.nan
            totals.append(norm)
        names.append(cc)
        means.append(np.nanmean(totals))
        stds.append(np.nanstd(totals))

    x = np.arange(len(names))
    ax_bar.bar(x, means, yerr=stds,
               color=[colors.get(n, "black") for n in names],
               alpha=0.7, capsize=4)
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(names)
    ax_bar.set_ylabel("Retransmissions per MB")
    ax_bar.set_title(f"Retransmission rate - Bandwidth={bw}Mbps | Delay={delay} | Max Queue={queue} | Loss Rate={loss}")

    outpath_bar = f"{FIGURES_SUMMARY}{EXPERIMENT}retrans_bar.png"
    fig_bar.tight_layout()
    plt.savefig(outpath_bar)
    plt.close(fig_bar)
    print(f"[SAVED] {outpath_bar}")

    # --- Aggregated bar chart of average throughput ---
    fig_tbar, ax_tbar = plt.subplots(figsize=(8, 5))
    names, means, stds = [], [], []

    for cc, runs in cc_runs.items():
        avgs = []
        for df in runs:
            avg_tp = df["throughput_mbps"].mean()
            avgs.append(avg_tp)
        names.append(cc)
        means.append(np.nanmean(avgs))
        stds.append(np.nanstd(avgs))

    x = np.arange(len(names))
    ax_tbar.bar(x, means, yerr=stds,
                color=[colors.get(n, "black") for n in names],
                alpha=0.7, capsize=4)

    ax_tbar.set_xticks(x)
    ax_tbar.set_xticklabels(names)
    ax_tbar.set_ylabel("Average Throughput (Mbps)")
    ax_tbar.set_title(f"Average Throughput - Bandwidth={bw}Mbps | Delay={delay} | Max Queue={queue} | Loss Rate={loss}",fontsize=10)

    # Dotted line at bandwidth
    ax_tbar.axhline(y=float(bw), color="red", linestyle="--", linewidth=1.5, label=f"Bandwidth={bw} Mbps")
    ax_tbar.legend()

    outpath_tbar = f"{FIGURES_SUMMARY}{EXPERIMENT}throughput_bar.png"
    fig_tbar.tight_layout()
    plt.savefig(outpath_tbar)
    plt.close(fig_tbar)
    print(f"[SAVED] {outpath_tbar}")