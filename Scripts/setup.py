
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


def run_cmake(config):
    """ Runs cmake in the output dir """
    cmake_args = ["-DCMAKE_BUILD_TYPE=Release"]
    cmake_args += ["-DPYTHON_EXECUTABLE:STRING=" + sys.executable]
    cmake_args += ["-DPROJECT_NAME:STRING=" + config["module_name"]]

    lib_prefix = "lib" if is_windows() else ""

    # Check for the right interrogate lib
    if PandaSystem.get_major_version() > 1 or PandaSystem.get_minor_version() > 9:
        cmake_args += ["-DINTERROGATE_LIB:STRING=" + lib_prefix + "p3interrogatedb"]
    else:

        # Buildbot versions do not have the core lib, instead try using libpanda
        if not isfile(join_abs(get_panda_lib_path(), "core.lib")):
            cmake_args += ["-DINTERROGATE_LIB:STRING=" + lib_prefix + "panda"]
        else:
            cmake_args += ["-DINTERROGATE_LIB:STRING=core"]

    if is_windows():
        # Specify 64-bit compiler when using a 64 bit panda sdk build
        bit_suffix = " Win64" if is_64_bit() else ""
        cmake_args += ["-G" + config["vc_version"] + bit_suffix]


    # Specify python version
    pyver = "{}{}".format(sys.version_info.major, sys.version_info.minor)
    pyver_dot = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    cmake_args += ["-DPYTHONVER:STRING=" + pyver]
    cmake_args += ["-DPYTHONVERDOT:STRING=" + pyver_dot]

    # Libraries
    for lib in ["freetype", "bullet", "eigen"]:
        if "use_lib_" + lib in config and config["use_lib_" + lib] in ["1", "yes", "y"]:
            cmake_args += ["-DUSE_LIB_" + lib.upper() + "=TRUE"]

    try_execute("cmake", join_abs(get_script_dir(), ".."), *cmake_args)


def run_cmake_build(config):
    """ Runs the cmake build which builds the final output """

    configuration = "Release"
    if config["generate_pdb"].lower() in ["1", "true", "yes", "y"]:
        configuration = "RelWithDebInfo"

    try_execute("cmake", "--build", ".", "--config", configuration)

