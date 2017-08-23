liblambdaOJ2 [![Build Status](https://travis-ci.org/kainwen/liblambdaOJ2.svg?branch=master)](https://travis-ci.org/kainwen/liblambdaOJ2)
=============================================

lambdaOJ2 is the platform for the course **Data Structure** in EE of Thu.


## INSTALL

### Compile

```bash
cd liblambdaOJ2
mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX=/your/path/to/install/ ..
make
make install
```

### Install Python3 API

Make sure:

* `judge` and `compile_code` is in `$PATH`

```bash
cd liblambdaOJ2/python_package
python3 setup.py install --prefix=/your/path/to/install/
```

Or use pip:

```bash
pip install "git+https://github.com/kainwen/liblambdaOJ2@master#egg=liblambdaOJ2&subdirectory=python_package"
```

### Docs

Docs can be found [here](doc/lambdaOJ2.md).
