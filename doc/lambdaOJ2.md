LambdaOJ2
=========

## Overview

LambdaOJ2 is a libaray for online judge system. It consists of two parts:

* kernel(written in pure C)
* python3 API(written in python, with the help of ctypes and subprocess)

An online judge system need to strictly control the resource(time and memory) of the program submitted by users. Security is also very important because we are going to run any code submitted by users.

LambdaOJ2 uses rlimit to control program resource(cputime, virtual memory, output file size) during runtime, and uses ptrace to trace each system call of the program to ensure security. Details can be understood from the code(`run_task.c`).

## Kernel

## Python3 API

## Usage
