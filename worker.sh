#!/bin/bash

#ENDPOINT="149.156.9.143:8888/image/v0/api/bbic?fname=/srv/data"
ENDPOINT="dcache-dot12.desy.de:8888/image/v0/api/bbic?fname=/srv/data/HBP"
DIR=/tmp
WORKER_ID=${1}
WORKER_DIR=${DIR}/${WORKER_ID}
WGET_OPTS=${2}
STACKS=`seq 0 0`
LEVELS=`seq 0 0`
SLICES=`seq 3699 3699`
XS=`seq 1 8`
YS=`seq 1 1`

mkdir -p ${WORKER_DIR}
rm -rf ${WORKER_DIR}/*

for STACK in ${STACKS}; do
  for LEVEL in ${LEVELS}; do
    for SLICE in ${SLICES}; do
      for X in ${XS}; do
        for Y in ${YS}; do
          FILE=${WORKER_DIR}/${STACK}_${LEVEL}_${SLICE}_${X}_${Y}.png
          URL="http://${ENDPOINT}/BigBrain_jpeg.h5&mode=ims&prog=TILE%200%20${STACK}%20${LEVEL}%20${SLICE}%20${X}%20${Y}%20none%2010%201"
          echo ${URL}
          wget ${WGET_OPTS} -O ${FILE} ${URL}
        done
      done
    done
  done
done
