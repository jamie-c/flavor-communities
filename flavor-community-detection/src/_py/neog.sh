#! /bin/bash

# check if the virtual environment exists
if [ ! -d "$WORKON_HOME/exaptive" ]; then
    # if it doesn't exist, exit with error
    echo "virtual environment doesn't exist"
    exit 1
fi

# activate the virtual environment
source $WORKON_HOME/exaptive/bin/activate

# get the directory of this file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# change to the directory of this file then src/_py
cd $DIR

# run python script
python neo4j_gds_community_detection.py

# deactivate the virtual environment
deactivate

# exit the script
exit 0