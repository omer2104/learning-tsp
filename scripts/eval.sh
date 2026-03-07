#!/bin/bash

# DEVICES="0"
# NUM_WORKERS=0
# EVAL_DATASET="data/tsp/tsp10-200_concorde.txt"
# VAL_SIZE=25600
# MODELS=("outputs/tsp_20-50/rl-ar-var-20pnn-gnn-max_20200313T002243")
# BATCH_SIZE=16

# DEVICES="0"
# NUM_WORKERS=0
# EVAL_DATASET="data/tsp/cp_lt_0.75_or_gt_0.77_tsp10-200_concorde.txt"
# VAL_SIZE=18704
# BATCH_SIZE=16
# MODELS=(
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-max_20200308T172931"
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-max-bntrack_20200310T095509"
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-mean_20200310T094833"
# )

# DEVICES="0"
# NUM_WORKERS=0
# EVAL_DATASET="data/tsp/tsp10-200_cnocorde_with_a_100.2.txt"
# VAL_SIZE=25600
# BATCH_SIZE=8
# MODELS=(
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-sum_20200310T094801"
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-max_20200308T172931"
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-max-bntrack_20200310T095509"
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-mean_20200310T094833"
# )

# DEVICES="0"
# NUM_WORKERS=0
# EVAL_DATASET="data/tsp/tsp10-200_concorde_with_side_100_solved_2.txt"
# VAL_SIZE=25600
# BATCH_SIZE=8
# MODELS=(
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-sum_20200310T094801"
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-max_20200308T172931"
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-max-bntrack_20200310T095509"
#     "outputs/tspsl_20-50/sl-ar-var-20pnn-gnn-mean_20200310T094833"
# )

DEVICES="0"
NUM_WORKERS=0
EVAL_DATASET="data/tsp/tsp10-200_concorde.txt"
VAL_SIZE=25600
MODELS=(
    "outputs/tspsl_20-50/sl-ar-var-20pnn-64edim-gnn-max_20250808T010107"
    "outputs/tspsl_20-50/sl-ar-var-20pnn-32edim-gnn-max_20250808T104211"
    "outputs/tspsl_20-50/sl-ar-var-20pnn-16edim-gnn-max_20250808T151845"
    "outputs/tspsl_20-50/sl-ar-var-20pnn-8edim-gnn-max_20250808T220639"
)
BATCH_SIZE=16


for MODEL in ${MODELS[*]}; do
    echo $MODEL
    CUDA_VISIBLE_DEVICES="$DEVICES" python eval.py  \
        "$EVAL_DATASET" \
        --val_size "$VAL_SIZE" --batch_size "$BATCH_SIZE" \
        --model "$MODEL" \
        --decode_strategies "greedy" "bs" \
        --widths 0 128 \
        --num_workers "$NUM_WORKERS"
done

# For insertion baselines:
# python eval_baseline.py random_insertion data/tsp/tsp10-200_concorde.txt -n 25600 --cpus 32 -f
