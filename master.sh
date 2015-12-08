#!/bin/bash

WORKER_NUM=${1}
WORKER_PIDS=""

for WORKER_ID in `seq 1 ${WORKER_NUM}`; do
   # ./worker.sh ${WORKER_ID} ${2} & # bash worker
   ./worker.py & # first python worker (thread pool)
   #./worker2.py & # second python worker (separate threads)
   WORKER_PIDS="${WORKER_PIDS} $!"
done

wait ${WORKER_PIDS}
