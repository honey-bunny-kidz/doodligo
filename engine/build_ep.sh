#!/bin/bash
# build_ep.sh epfile code
set -e
cd /home/claude/doodligo/engine
PYTHONPATH=../episodes python3 compose.py ../episodes/$1.py /home/claude/work/$2/clips /home/claude/work/$2/voices ../videos/$2.mp4 > /home/claude/work/$2/build.log 2>&1
tail -2 /home/claude/work/$2/build.log
