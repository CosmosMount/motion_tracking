# sudo ufw disable
# this is my unitree g1's ip in wifi
# redis_ip="192.168.110.24"
# localhost if you are using laptop to verify sim2sim or sim2real
redis_ip="localhost"

# the height (empirically) should be smaller than the actual human height, due to inaccuracy of the PICO estimation.
actual_human_height=1.6
python xrobot.py --robot unitree_g1 \
             --actual_human_height $actual_human_height \
             --redis_ip $redis_ip \
             --target_fps 100 \
             --measure_fps 0 \
             --smooth \
             --record_pkl \
            #  --pinch_mode
