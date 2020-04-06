#!/bin/bash -xe

git submodule update --init --recursive --remote

# If that doesn't work:
#
# rmdir obfs4
# git clone git@github.com:jamesthoughton/obfs4
# cd fpgen/crawl
# rmdir oniontree
# git clone git@github.com:onionltd/oniontree
