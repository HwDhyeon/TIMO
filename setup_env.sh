#!/bin/sh -i

echo "export PYTHONPATH=$(pwd)/timo;${PYTHONPATH}" >> "~/.bashrc"
source "~/.bashrc"
