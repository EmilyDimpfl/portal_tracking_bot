#!/bin/sh

docker build -t portalbot .
docker run --rm -d -v ${PWD}/data.json:/opt/portalbot/data.json \
    -e MOD_ROLE_ID=1074134286652936202 \
    --name tkdimensions portalbot
