# bgp_simulator_pathsec_policies

This package is for simulating defenses against BGP Path Manipulation attacks
and Route Leaks. 

## Usage

Runnable scripts are located in the `bin` directory. Run them with either Python
```sh
python3 bin/2023_aggregated.py
```
or PyPy
```sh
pypy3 bin/2023_aggregated.py
```

## Installation

This package requires Python >= 3.7.

To install for development
```sh
git clone https://github.com/c-morris/bgp-simulator-policies.git
cd bgp_simulator_pathsec_policies
pip install -e .
```

## Testing

```sh
pytest
```
