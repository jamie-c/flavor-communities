#! /bin/bash

source $WORKON_HOME/exaptive/bin/activate

cd $WORKON_HOME/exaptive/exaptive/flavor-community-detection/src/_py

python "neo4j_gds_community_detection.py"

deactivate