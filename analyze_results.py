#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS = "results/"
FIGURES = "figures/"

os.makedirs(FIGURES, exist_ok=True)

dfs = []

for folder in os.listdir(RESULTS):
    path = f"{RESULTS}{folder}/client.csv"
    if not os.path.exists(path):
        continue

    parts = folder.split("_")
    cc = parts[0]
    bw = parts[1].replace("bw", "")
    delay = parts[2].replace("d", "")
    queue = parts[3].replace("q", "")
    loss = parts[4].replace("l", "")

    df = pd.read_csv(path)
    df["cc"] = cc
    df["bw"] = int(bw)
    df["delay"] = delay
    df["queue"] = int(queue)
    df["loss"] = float(loss)

    dfs.append(df)

df = pd.concat(dfs)

# ---------------------------
# Average Throughput
# ---------------------------
avg = df.groupby("cc")["throughput_mbps"].mean()
plt.figure(figsize=(8,5))
avg.plot(kind="bar", title="Average Throughput by Algorithm")
plt.ylabel("Mbps")
plt.grid(axis="y")
plt.savefig(FIGURES + "avg_throughput.png")
plt.close()

# ---------------------------
# Retransmissions
# ---------------------------
re = df.groupby("cc")["retransmissions"].sum()
plt.figure(figsize=(8,5))
re.plot(kind="bar", color="orange", title="Total Retransmissions")
plt.ylabel("Count")
plt.grid(axis="y")
plt.savefig(FIGURES + "retransmissions.png")
plt.close()

# ---------------------------
# Time Series Per Algorithm
# ---------------------------
for cc in df["cc"].unique():
    subset = df[df["cc"] == cc]
    plt.figure(figsize=(8,5))
    plt.plot(subset["end"], subset["throughput_mbps"])
    plt.title(f"Throughput over Time ({cc})")
    plt.xlabel("Seconds")
    plt.ylabel("Mbps")
    plt.grid()
    plt.savefig(FIGURES + f"throughput_{cc}.png")
    plt.close()
