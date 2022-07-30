#!/bin/bash

# activate the python virtual environment

source ~/slt/venv/slt-python3.7/bin/activate

echo "get the token"

token=`python3 finicity_engine.py "create_token"`

echo "$token"
