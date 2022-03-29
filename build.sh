#!/usr/bin/env bash

set -ex

DOCKER=haproxy_packaging:centos7
CURPATH="$( cd $(dirname $0) ; pwd -P )"

rm   -rf ${CURPATH}/output
mkdir -p ${CURPATH}/output

docker build -t ${DOCKER} .


docker run --rm -t -h haproxy -v ${CURPATH}/output:/root/rpmbuild:Z ${DOCKER}
