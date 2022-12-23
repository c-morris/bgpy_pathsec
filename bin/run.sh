#!/bin/bash 

# Symlink the Caida Collector cache into a common directory
# This prevents it from running once per container
ln -s /data/caida_collector_cache /tmp/caida_collector_cache

# Run the simulation
pypy3 /python_sim/bgp-simulator-policies/bin/2023_aggregated.py
