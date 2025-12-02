run:
	sudo python3 run_experiments.py

analyze:
	sudo python3 parse_iperf.py
	sudo python3 graph_experiments_each.py
	sudo python3 graph_experiments_summary.py

clean:
	rm -rf results/*
	rm -rf figures/*
