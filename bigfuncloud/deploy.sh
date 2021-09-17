#!/bin/sh

set -ex

export IMAGE=registry.$BFC_DOMAIN/$BFC_USER/$BFC_APP:latest
docker build -t "$IMAGE" .
docker push "$IMAGE"
