#!/bin/bash

install_python () {
    cd python_package;
    python setup.py install;
    rm build -rf;
    cd ..
}

export INSTALL_PREFIX=/tmp
mkdir /tmp/bin
install_python;
