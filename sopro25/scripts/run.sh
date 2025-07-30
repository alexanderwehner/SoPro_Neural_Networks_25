#!/usr/bin/env bash

# run setup
source /nethome/awehner/projects/sopro25/scripts/setup.sh

# run misc. stuff
nvidia-smi
echo $CUDA_VISIBLE_DEVICES
echo $HOSTNAME
which python
python -m pip list

# run code
python $PROJECT_DIR/src/mnist_train.py
