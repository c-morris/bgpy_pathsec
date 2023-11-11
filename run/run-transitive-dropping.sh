#!/bin/bash 

# Source Virtual Environment
source ~/env/bin/activate

# Set Job Completion Index
export JOB_COMPLETION_INDEX=$SLURM_ARRAY_TASK_ID

# Run the simulation
python ~/bgp-simulator-pathsec-policies/run/transitive_dropping.py
