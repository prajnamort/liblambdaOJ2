#!/bin/bash

export JUDGE_DIR=`pwd`/local/bin;
export LD_LIBRARY_PATH=`pwd`/local/lib;
python tests/test.py;
