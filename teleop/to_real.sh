SCRIPT_DIR=$(dirname $(realpath $0))
ckpt_path=${SCRIPT_DIR}/assets/ckpts/twist2_1017_20k.onnx

# change the network interface name to your own that connects to the robot
# net=enp0s31f6
net=enp108s0

cd deploy_real

python g1_sim.py \
    --policy ${ckpt_path} \
    --net ${net} \
    --device cuda \
    --use_hand \
    # --smooth_body 0.5
    # --record_proprio \
