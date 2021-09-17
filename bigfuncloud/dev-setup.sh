#!/bin/bash

set -ex

eval "$(direnv export bash)"
pip3 install -r ./requirements.txt
