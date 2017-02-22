#!/bin/bash

compile_c_code () {
    mkdir build; cd build;
    cmake -DCMAKE_INSTALL_PREFIX=../local ..;
    make;
	make install;
    cd ..;
}

install_python () {
	pip install git+https://github.com/kainwen/lambdaOJ2@master\#egg=lambdaOJ2\&subdirectory=python_package
}

compile_c_code;
install_python;
