# dpy2-migration-helper

Helper for d.py 1.x -> 2.x migrations.
Searches for and reports (potentially) required changes.

This is only slightly smarter than a simple regex search
and mostly aims to speed up the manual part of those searches.

## Installation

1. Create a venv if you don't already have one:
```
python -m venv .venv
```
1. Install this package:
```
python -m pip install dpy2-migration-helper
```

## Usage

```
usage: dpy2-migration-helper [-h] src [src ...]

positional arguments:
  src         Path to cog's module file or package directory.

optional arguments:
  -h, --help  show this help message and exit
```

## License

Distributed under the Apache License 2.0. See ``LICENSE`` for more information.

---

> Jakub Kuczys &nbsp;&middot;&nbsp;
> GitHub [@Jackenmen](https://github.com/Jackenmen)
