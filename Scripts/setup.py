
import sys
from os import chdir
from os.path import join, isdir
from panda3d.core import PandaSystem

from common import *

def make_output_dir():
    """ Creates the output directory and sets the CWD into that directory """
    output_dir = get_output_dir()
    try_makedir(output_dir)
    if not isdir(output_dir):
        fatal_error("Could not create output directory at:", output_dir)
    chdir(output_dir)


def run_cmake(module_name):
    """ Runs cmake in the output dir """
    cmake_args = ['-DCMAKE_BUILD_TYPE=Release']
    cmake_args += ['-DPYTHON_EXECUTABLE:STRING=' + sys.executable]
    cmake_args += ['-DPROJECT_NAME:STRING=' + module_name]

    # Check for the right interrogate lib
    if PandaSystem.get_major_version() > 1 or PandaSystem.get_minor_version() > 9:
        cmake_args += ['-DINTERROGATE_LIB:STRING=interrogatedb']
    else:
        cmake_args += ['-DINTERROGATE_LIB:STRING=p3core']


    if is_windows():
        # Specify 64-bit compiler when using a 64 bit panda sdk build
        bit_suffix = " Win64" if is_64_bit() else ""
        # cmake_args += ['-GVisual Studio 10 2010' + bit_suffix]

    # if sys.version_info.major == 3:
    pyver = "{}{}".format(sys.version_info.major, sys.version_info.minor)
    cmake_args += ['-DPYTHONVER:STRING=' + pyver]

    try_execute("cmake", join_abs(get_script_dir(), ".."), *cmake_args)


def run_cmake_build():
    """ Runs the cmake build which builds the final output """
    try_execute("cmake", "--build", ".", "--config", "RelWithDebInfo")


# if __name__ == "__main__":

    # make_output_dir()
    # run_cmake()

    # if not "--cmake-only" in sys.argv:
        # run_cmake_build()

    # print("Success!")
    # sys.exit(0)
