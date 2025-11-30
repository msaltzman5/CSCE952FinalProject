#!/usr/bin/env python3
"""
Parse iperf3 JSON logs (client.json) under results/* and
convert them into CSV files (client.csv) for analysis.
"""

import json
import pandas as pd
import os


def parse_iperf_json(json_path: str):
    """Return a DataFrame with per-interval throughput/retransmissions, or None."""
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"[SKIP] Corrupt JSON: {json_path}")
        return None

    # If iperf reported an error, skip this run
    if "error" in data and data["error"]:
        print(f"[SKIP] iperf error in {json_path}: {data['error']}")
        return None

    intervals = data.get("intervals", [])
    if not intervals:
        print(f"[SKIP] No intervals in {json_path}")
        return None

    rows = []
    for entry in intervals:
        # iperf3 JSON has either "sum" or "sum_sent"/"sum_received"
        if "sum" in entry:
            s = entry["sum"]
        elif "sum_sent" in entry:
            s = entry["sum_sent"]
        elif "sum_received" in entry:
            s = entry["sum_received"]
        else:
            continue

        rows.append({
            "start": s.get("start", 0.0),
            "end": s.get("end", 0.0),
            "throughput_mbps": s.get("bits_per_second", 0.0) / 1e6,
            "retransmissions": s.get("retransmits", 0),
        })

    if not rows:
        print(f"[SKIP] No usable intervals in {json_path}")
        return None

    return pd.DataFrame(rows)


def main():
    root = "results"
    if not os.path.isdir(root):
        print("[INFO] No results directory found.")
        return

    for dir_name in os.listdir(root):
        exp_dir = os.path.join(root, dir_name)
        if not os.path.isdir(exp_dir):
            continue

        json_path = os.path.join(exp_dir, "client.json")
        if not os.path.exists(json_path):
            print(f"[SKIP] Missing client.json in {exp_dir}")
            continue

        print(f"[Parsing] {json_path}")
        df = parse_iperf_json(json_path)
        if df is None or df.empty:
            print(f"[SKIP] No data for {dir_name}")
            continue

        csv_path = os.path.join(exp_dir, "client.csv")
        df.to_csv(csv_path, index=False)
        print(f"[OK] Wrote {csv_path}")


if __name__ == "__main__":
    main()
