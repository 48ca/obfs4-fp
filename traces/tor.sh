#!/bin/bash

pushd $(dirname ${BASH_SOURCE[0]}) > /dev/null

tor -f torrc

popd > /dev/null
