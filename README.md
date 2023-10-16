![Tests](https://github.com/c-morris/bgp-simulator-pathsec-policies/actions/workflows/tests.yml/badge.svg)

# bgp_simulator_pathsec_policies

This package is for simulating defenses against BGP Path Manipulation attacks
and Route Leaks. Additional documentation can be found in the docs directory.

BGP propagation according to valley-free routing rules is provided by
[https://github.com/jfuruness/bgpy](https://github.com/jfuruness/bgpy).

## Installation

This package requires Python >= 3.7.

To install for development
```sh
git clone https://github.com/c-morris/bgp-simulator-policies.git
cd bgp_simulator_pathsec_policies
pip install -e .
```

1. Download pypy 3.10: wget https://downloads.python.org/pypy/pypy3.10-v7.3.12-linux64.tar.bz2
2. `/path/to/pypy3 -m venv env`
3. `source env/bin/activate`

1. `git clone git@github.com:jfuruness/caida_collector_pkg.git`
2. `cd caida_collector_pkg`, edit setup.cfg to change PyYAML version to 5.3.1 (in both places!)
3. `pip install -e .`

1. `git clone git@github.com:jfuruness/bgpy.git`
2. `git checkout f1d388afd9460de2d15ec8a6189bf4a66a26ae8a`
3. `cd bgpy`, edit setup.cfg to change PyYAML version to 5.3.1 (in both places!) and comment out caida_collector dependency
4. `pip install -e .`

1.` git clone git@github.com:c-morris/bgp-simulator-pathsec-policies.git`
2. `pypy3 setup.py develop`

## Usage

Runnable scripts are located in the `run` directory. Run them with either Python
```sh
python3 run/2023_aggregated.py
```
or PyPy (Recommended)
```sh
pypy3 run/2023_aggregated.py
```

## Running Tests

To run all tests, including unit and system integration tests, use

```sh
pytest
```

Human-readable results of the system integration tests can be found in
tests/engine_tests/engine_test_outputs/aggregated_diagrams.pdf. More detailed
test results are stored as YAML in each subdirectory of the engine_test_outputs
directory. 

When the tests run, the running simulator output is saved in a \*-guess.yml
file and compared to a known-good ground truth (\*-gt.yml) file. Any difference
between the two files will be reported as a test failure. This is important to
keep in mind when modifying data structures, especially the announcement class,
because these modifications will change the yaml without necessarily making the
simulator behave incorrectly. In cases like this where a large number of false
failures are created, the \*-gt.yml files can be deleted and the next run of
`pytest` will re-generate them.   
