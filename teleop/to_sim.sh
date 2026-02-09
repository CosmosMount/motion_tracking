SCRIPT_DIR=$(dirname $(realpath $0))
ckpt_path=${SCRIPT_DIR}/assets/ckpts/twist2_1017_20k.onnx

python g1_sim.py \
    --xml ./assets/g1/g1_sim2sim_29dof.xml \
    --policy ${ckpt_path} \
    --device cuda \
    --measure_fps 0 \
    --policy_frequency 80 \
    --limit_fps 1 \
    --record_proprio \
