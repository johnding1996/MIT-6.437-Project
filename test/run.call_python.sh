#!/bin/bash

# This file is used in run.sh, basically ${1} is replaces with the directory for a
# student's submission, so that python run_submitted_code.py ${1} is called, and
# the output is stored in $logdir/run.call_python.${1}.out 2>&1 ($logdir is defined
# in test.inc.

source test.inc

echo | python run_submitted_code.py ${1} > $logdir/run.call_python.${1}.out 2>&1
