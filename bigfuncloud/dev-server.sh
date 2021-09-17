#!/bin/bash

export FLASK_APP=main
eval "$(direnv export bash)"

watchexec -r -- "invalidate-devserver; flask run --port=80"
