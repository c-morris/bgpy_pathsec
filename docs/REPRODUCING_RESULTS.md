# How to Reproduce the Results from the Paper

Reproducibility is a key part of scientific integrity; the intent of this
document is to make that possible for someone with reasonable familiarity with
the tools and techniques used here, including grad students like myself.

## Computing Environment

The simulations that generated the results for the paper were run on UConn's
High Performance Computing (HPC) cluster. The UConn HPC uses the Slurm workload
manager as its job scheduler. If your institution makes a similar service
available, you may be able to re-use parts of the sbatch script I used.

```sh
#!/bin/bash
#SBATCH --partition=general
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1    # Job only requires 1 CPU core
#SBATCH --mem-per-cpu=3G
#SBATCH --mail-type=END
#SBATCH --mail-user=your.email@institution.edu
#SBATCH --account=youraccount
#SBATCH --job-name=bgpy-pathsec
#SBATCH --output=out/array_%A_%a.out
#SBATCH --error=err/array_%A_%a.err
#SBATCH --array=0-1000%100
~/bgpy_pathsec/run/run.sh
```

Before running this, you'll need to manually crate the out and err directories
or the job will fail without a descriptive error message. The `%100` at the end
of the last SBATCH line specifies the number of concurrent tasks that are
allowed to run out of the total (1000). Your institution may have different
restrictions on the number of tasks you can run in parallel. 

Alternatively, if a Slurm environment is not readily available, it is possible
to run these simulations on a Kubernetes cluster using the Jobs API. Before
learning about the university's HPC this is how I ran simulations, so while I
haven't run the latest version of the code like this, I have high confidence it
would work with few modifications. 

Below is a Dockerfile that *should* work based on the old one I used, but it is
untested on the latest version.

```
# syntax=docker/dockerfile:1

FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y \
    curl \
    python3 \
    python3-pip \
    graphviz \
    git \
    texlive-xetex \
  && rm -rf /var/lib/apt/lists/*
RUN curl -L "https://downloads.python.org/pypy/pypy3.10-v7.3.13-linux64.tar.bz2" \
    | tar -xjC / \
    && ln -s /pypy3.10-v7.3.13-linux64/bin/pypy3 /usr/local/bin/pypy3 \
    && /usr/local/bin/pypy3 -m ensurepip
COPY . /bgpy_pathsec/
RUN pypy3 -m pip install -e /bgpy_pathsec/
```

For the job spec, something like this should work. I was running this on a
local Kubernetes cluster, so I used glusterfs as a shared file system. If
running in the cloud, using s3 or an equivalent managed storage service would
be much simpler.

```
apiVersion: batch/v1
kind: Job
metadata:
  name: bgpy-pathsec-job
spec:
  backoffLimit: 10
  completions: 1000
  completionMode: "Indexed"
  parallelism: 100
  template:
    spec:
      volumes:
      - name: gluster1
        glusterfs:
          path: gluster1
          endpoints: glusterfs-cluster
          readOnly: false
      containers:
      - name: bgpy-container
        image: <local-registry-ip-redacted>:5000/bgpy-pathsec
        command: ["bash", "/bgpy_pathsec/run/run.sh"]
        volumeMounts:
        - name: gluster1
          mountPath: /data
        resources:
          requests:
            cpu: "1"
      restartPolicy: Never
```

There are two other changes needed to run on Kubernetes. One is to delete these
lines in run.sh. Kubernetes will set the JOB_COMPLETION_INDEX environment
variable directly and no virtual environment is needed with the container. 

```sh
# Source Virtual Environment
source ~/env/bin/activate

# Set Job Completion Index
export JOB_COMPLETION_INDEX=$SLURM_ARRAY_TASK_ID
```

The other is to change over all the directories in run.sh and the python file
you're running (e.g. 2023_aggregated.py) to point to a shared filesystem. On
the HPC, home directories are shared with all of the compute nodes, so the
scripts assume this. In the example job spec, I mount the volume to /data, so
the caida cache_dir parameter and the Simulation output_path parameter would
need to be changed to point to /data. 

Regardless of how the simulations are run, it's important that the caida cache
directory is shared. The simulator automatically downloads the graph from CAIDA
on first run and caches it for future runs. Sharing the cache directory means
it only downloads the graph once as opposed to 1000 times. 

While there are no technical limitations that preclude setting the number of
trials in 2023_aggregated.py to 7000 and running it on a desktop PC, my
back-of-the-napkin calculation says it would take around 27 days to run on a
12-core machine, so I do not recommend it.

## Graphs

All of the graphs for the paper were generated using matplotlib and a Jupyter
notebook. The code quality of the graphing code is unfortunately much lower
than the rest of the code in this repo, mostly due to the speed at which
changes needed to be made in the graphs. I've included a cleaned up version of
the Jupyter notebook in the run folder, though, it's full of hard-coded file
paths that need to be edited before it will run.
