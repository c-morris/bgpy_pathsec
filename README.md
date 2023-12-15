![Tests](https://github.com/c-morris/bgp-simulator-pathsec-policies/actions/workflows/tests.yml/badge.svg)

# bgpy_pathsec

This package is for simulating defenses against BGP Path Manipulation attacks
and Route Leaks. It was developed to support the evaluation of the defenses
proposed in [this paper](https://www.researchgate.net/publication/375553362_BGP-iSec_Improved_Security_of_Internet_Routing_Against_Post-ROV_Attacks).
Additional documentation can be found in the docs directory.

BGP propagation according to valley-free routing rules is provided by
[https://github.com/jfuruness/bgpy](https://github.com/jfuruness/bgpy).

## Installation

This package requires Python or PyPy (Recommended) >= 3.10.

To install for development
```sh
git clone https://github.com/c-morris/bgpy_pathsec.git
cd bgpy_pathsec
pip install -e .
```

## Usage

See [docs/REPRODUCING_RESULTS.md](docs/REPRODUCING_RESULTS.md) for detailed instructions on how to run the simulations.

For small runs on a single machine, runnable scripts are located in the `run`
directory. Run them with either Python
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

## Misc

Development is supported by NSF grant No. 2247810. Any opinions, findings, and
conclusions or recommendations expressed in this material are those of the
author(s) and do not necessarily reflect the views of the National Science
Foundation.

