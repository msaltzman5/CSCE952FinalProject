#!/usr/bin/env python3

import json
import pandas as pd
import os

def parse_json(path):
    with open(path) as f:
        data = json.load(f)

    rows = []
    for entry in data.get("intervals", []):
        s = entry["sum"]
        rows.append({
            "start": s["start"],
            "end": s["end"],
            "throughput_mbps": s["bits_per_second"] / 1e6,
            "retransmissions": s.get("retransmits", 0)
        })
    return pd.DataFrame(rows)

def main():
    for dir_name in os.listdir("results"):
        json_path = f"results/{dir_name}/client.json"
        if not os.path.exists(json_path):
            continue

        print(f"[Parsing] {json_path}")
        df = parse_json(json_path)
        df.to_csv(f"results/{dir_name}/client.csv", index=False)

if __name__ == "__main__":
    main()
