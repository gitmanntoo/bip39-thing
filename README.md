# BIP39 Thing

- Run from Docker: `docker run -it --rm dockmann/bip39-thing`
- Run from repo: `sh run-it.sh`

## Description

This utility generates three hashes:

- SHA256
- BIP39 mnemonic
- Truncated BIP39 mnemonic

When run, it will prompt for an input string which is one of the following:

- A valid hexadecimal hash with length [16, 20, 24, 28, 32] bytes
- A valid BIP39 mnemonic phrase with [12, 15, 18, 21, 24] words
- Some other string

Input can span multiple lines. Leading and trailing whitespace is trimmed.

For the given input, the output consists of hashes and mnemonic phrases for all valid lengths of the input hash.

## Setup

Built with Pythyon 3.11 using Poetry.

- `requirements.txt` generated from `poetry export -f requirements.txt --output requirements.txt`


Requires `docker` to be installed to build and run from image.

- [Install Docker Engine](https://docs.docker.com/engine/install/)
- multi-platform build requires containerd (https://docs.docker.com/build/building/multi-platform/)
