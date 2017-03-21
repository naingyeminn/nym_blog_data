#!/bin/bash

curl -L -o splitpgs.zip https://github.com/naingyeminn/splitpgs/archive/master.zip
unzip splitpgs.zip
cp splitpgs-master/splitpgs /usr/local/bin
rm -rf splitpgs-master
