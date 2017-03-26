#!/usr/bin/env python3

from distutils.command.build import build
from distutils.core import setup

import os
import shutil
import subprocess


class CMakeCommand(build):
    """A custom command to compile liblambdaoj2.so."""

    def run(self):
        cwd = os.getcwd()
        c_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        build_dir = os.path.join(c_path, "build")
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        os.mkdir(build_dir)
        os.chdir(build_dir)

        cmake_install_prefix = os.getenv("VIRTUAL_ENV")
        proc = subprocess.Popen(["cmake",
                                 "-DCMAKE_INSTALL_PREFIX=%s" % cmake_install_prefix,
                                 ".."])
        proc.wait()

        proc = subprocess.Popen(["make"])
        proc.wait()

        proc = subprocess.Popen(["make", "install"])
        proc.wait()

        os.chdir(cwd)
        super().run()


setup(name='oj',
      version='1.0',
      description='Python Interface for liblambdaOJ2',
      author='Zhenghua Lyu',
      author_email='kainwen@gmail.com',
      url='https://github.com/kainwen/liblambdaOJ2',
      cmdclass={'build': CMakeCommand},
      packages=['oj']
)
