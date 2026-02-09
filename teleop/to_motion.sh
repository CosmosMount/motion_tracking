#!/bin/bash

script_dir=$(dirname $(realpath $0))
# motion_file="${script_dir}/assets/example_motions/0807_yanjie_walk_005.pkl"
motion_file="${script_dir}/recordings/xrobot_retargeting_20260209_201456.pkl"

# by default we use our own laptop as the redis server
redis_ip="localhost"
# this is my unitree g1's ip in wifi
# redis_ip="192.168.110.24"

# Run the motion server
python g1_motion.py \
    --motion_file ${motion_file} \
    --robot unitree_g1_with_hands \
    --vis \
    --redis_ip ${redis_ip}
    # --send_start_frame_as_end_frame \
    # --use_remote_control \
