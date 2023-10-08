#!/bin/bash 

# Symlink the Caida Collector cache into a common directory
# This prevents it from running once per container
#ln -s /data/caida_collector_cache /tmp/caida_collector_cache

# Source Virtual Environment
source ~/env/bin/activate

# Set Job Completion Index
export JOB_COMPLETION_INDEX=$SLURM_ARRAY_TASK_ID

# Run the simulation
python ~/bgp-simulator-pathsec-policies/run/kapk.py
