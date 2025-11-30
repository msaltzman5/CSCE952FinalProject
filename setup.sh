#!/bin/bash

echo "[+] Updating packages..."
sudo apt update

echo "[+] Installing Mininet, iperf3, and dependencies..."
sudo apt install -y mininet iperf3 python3-pip python3-venv

echo "[+] Installing Python packages..."
pip3 install matplotlib pandas numpy

echo "[+] Creating project directories..."
mkdir -p results figures

echo "[+] Setup complete!"
