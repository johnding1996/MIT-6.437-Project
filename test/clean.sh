#!/bin/bash

source test.inc

if [ -z "$@" ];
then
  rm -rf ./$logdir/*
  rm -rf ./$resultdir/*
  rm -rf ./$rundir/*
  rm -rf ./$outputdir/*
  rm -rf ./$lockdir/*
fi

for NAME in "$@"; do
  rm -rf ./$rundir/$NAME
  rm -rf ./$outputdir/$NAME
  rm -f ./$logdir/.temp_${NAME}_time_output
done
