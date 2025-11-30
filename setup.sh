#!/bin/bash

echo "[+] Updating packages..."
sudo apt update -y
sudo apt upgrade -y

echo "[+] Installing Mininet and dependencies..."
sudo apt install -y mininet iperf3 openvswitch-switch openvswitch-testcontroller

echo "[+] Installing Python scientific libraries (apt-based)..."
sudo apt install -y python3-matplotlib python3-pandas python3-numpy

echo "[+] Creating project directories..."
mkdir -p results figures

echo "[+] Setup complete!"
