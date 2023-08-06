#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Setup this SWIG library."""
import os
import re
import shutil
import subprocess

from setuptools import Extension, setup
from setuptools.command.build_py import build_py
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

STD_EXT = Extension(
    name='_dfiibridge_core',
    swig_opts=['-c++', '-Iswig/include', '-threads', '-py3'],
    sources=[
        'swig/src/DfiiBridgeServer.cpp',
        'swig/src/Channel.cpp',
        'swig/src/ChannelClient.cpp',
        'swig/src/ChannelServer.cpp',
        'swig/src/CoreSessionManager.cpp',
        'swig/src/DfiiBridgeClient.cpp',
        'swig/src/DfiiBridgeCore.cpp',
        'swig/src/Session.cpp',
        'swig/src/DfiiBridge.i'
    ],
    include_dirs=[
        'swig/include',
    ],
    extra_compile_args=['-std=c++17'],
    libraries = ['stdc++fs', 'rt', 'pthread']
)



"""
Build extensions before python modules, or the generated SWIG python files will be missing.
"""
class BuildPy(build_py):

    def setup_libzmq(self):
        """
        Add libzmq to the list of needed link libraries
        """

        libs_stdout = subprocess.run(["gcc", "-lzmq"], stderr=subprocess.PIPE).stderr

        if "cannot find -lzmq" in libs_stdout.decode():
            raise Exception("Libzmq is not present on your system. Please install it.")

        print("Libzmq is already installed. I'll link to it.")
        STD_EXT.libraries += ["zmq"]

    def verify_swig_version(self):
        """
        Verify that the required SSIG version 4 is available.
        """
        stdout_swig_version = subprocess.check_output(["swig", "-version"])
        swig_version = re.findall(r"(\d+)\.(\d+)\.(\d+)", stdout_swig_version.decode())
        if swig_version:
            if swig_version[0][0]!="4":
                raise Exception(f"The swig version {swig_version} that is installed is too old")
                # we need a new version of swig!


    def run(self):
        self.setup_libzmq()
        self.verify_swig_version()
        self.run_command('build_ext')
        super(build_py, self).run()


class PostInstallCommand(install):
    """
    We need to copy the SWIG generated python file DfiiBridgeCore.py in the installation directory.
    This file copy isn't done by the framework. Without this python script, none of our python classes
    are available.
    """

    def run(self):
        print(f"Copy the SWIG generated python file to {self.install_libbase}")
        install.run(self)
        shutil.copyfile("swig/src/dfiibridge_core.py", os.path.join(self.install_libbase, "dfiibridge_core.py"))

class egg_info_ex(egg_info):
    """
    Includes license file into `.egg-info` folder.
    SRC: https://stackoverflow.com/questions/9977889/how-to-include-license-file-in-setup-py-script
    """

    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get('install', True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file('LICENSE', self.egg_info)

        egg_info.run(self)

setup(
    ext_modules=[STD_EXT],
    cmdclass={'build_py': BuildPy , 'install': PostInstallCommand, 'egg_info': egg_info_ex},
    license_files = ('LICENSE',),
    license = 'GPL3',
)
