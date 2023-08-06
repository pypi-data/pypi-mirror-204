# lib-holdings

CLI tool for retrieving holding counts for a list of OCNs and libraries.
Uses the OCLC API: https://developer.api.oclc.org/

# Installation

```bash
$ pip install lib-holdings
```

# Usage

```bash
$ holdings [OPTIONS] INFILE_OCNS INFILE_SYMB OUT_FOLDER
```

ARGUMENTS:

    INFILE_OCNS:    text file containing OCNs (1 per line)
    INFILE_SYMB:    text file containing institute symbols (1 per line)
    OUT_FOLDER:     path to the output directory

OPTIONS:
```bash
--start INTEGER  Position of OCN to start with.
--key TEXT       OCLC API key.
--secret TEXT    OCLC API secret.
```