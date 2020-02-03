# Recherche Babac2

A Python3 module to parse experimental information from a Bruker NMR dataset.

## Installation

1. Clone the repository

```bash
git clone https://github.com/normcyr/parse_NMR_dataset
```

2. Create a Python virtual environment using `virtualenv`

```bash
cd parse_NMR_dataset
virtualenv -p python3 venv
source venv/bin/activate
```

3. Install the module

```bash
pip install -e .
```

4. Run the program

```bash
parse_data -h
```
```
usage: parse_dataset [options]

positional arguments:
  dataset_path   indicate the path to dataset you want to be parsed

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

For example:

```bash
parse_data /home/norm/data/NMR/NormandCyr/nc001neo7
```
