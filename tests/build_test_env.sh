#!/bin/bash

install_python () {
    cd python_package;
    python setup.py install;
    rm build -rf;
    cd ..
}

install_python;
