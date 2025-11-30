# CSCE952FinalProject

## Steps to run:
### 1. Set up ubuntu virtual machine
a. https://ubuntu.com/download/desktop  
b. Download VirtualBox  
c. Create new vm with iso you downloaded  
d. Start up virtual machine  
e. run:  
    i. sudo apt install git  
f. Clone this repo  
### 2. Run:
chmod +x setup.sh  
./setup.sh  
make run  
make analyze  
### 3. View results:
Access results/ and figures/ directories

## Project Structure:
cc-project/
│
├── setup.sh
├── Makefile
│
├── topo_cc.py
├── run_experiments.py
├── parse_iperf.py
├── analyze_results.py
│
├── results/      ← auto-generated
└── figures/      ← auto-generated
