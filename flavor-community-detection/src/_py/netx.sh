#! /bin/bash

source $WORKON_HOME/exaptive/bin/activate

cd $WORKON_HOME/exaptive/exaptive/flavor-community-detection/src/_py

python "networkx_community_detection.py"

deactivate