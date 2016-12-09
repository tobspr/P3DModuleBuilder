
import shutil
import sys
import multiprocessing
from os import chdir, _exit
from os.path import isdir, isfile
from panda3d.core import PandaSystem

from .common import get_output_dir, try_makedir, fatal_error, is_windows
from .common import is_linux, join_abs, get_panda_lib_path, is_64_bit
from .common import try_execute, get_script_dir, get_panda_mscv_version
from .common import have_eigen, have_bullet, have_freetype, print_error


def make_output_dir(clean=False):
    """ Creates the output directory and sets the CWD into that directory. If
    clean is True, the output dir will be cleaned up. """
    output_dir = get_output_dir()

    # Cleanup output directory in case clean is specified
    if isdir(output_dir) and clean:
        print("Cleaning up output directory ..")
        shutil.rmtree(output_dir)

    try_makedir(output_dir)
    if not isdir(output_dir):
        fatal_error("Could not create output directory at:", output_dir)
    chdir(output_dir)


def handle_cmake_error(output):
    """ Improves the cmake output messages """
    print_error("\n\n\n")
    print_error("-" * 60)
    print_error("\nCMake Error:")

    if "Re-run cmake with a different source directory." in output:
        print_error("You moved the project folder, please add ' --clean' to the command line.")

    elif "No CMAKE_CXX_COMPILER could be found." in output or "No CMAKE_C_COMPILER could be found." in output:
        print_error("Could not find the required compiler!")
        if is_windows():
            print_error("\nPlease make sure you installed the following compiler:")
            bitness = "64 bit" if is_64_bit() else ""
            print_error(get_panda_mscv_version().cmake_str, bitness)
        else:
            print_error("The required compiler is:", PandaSystem.get_compiler())


    print_error("\n")
    print_error("-" * 60)
    print_error("\n\n\n")
    exit(-1)


def run_cmake(config, args):
    """ Runs cmake in the output dir """

    configuration = "Release"
    if config["generate_pdb"].lower() in ["1", "true", "yes", "y"]:
        configuration = "RelWithDebInfo"

    cmake_args = ["-DCMAKE_BUILD_TYPE=" + configuration]
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
        cmake_args += ["-G" + get_panda_mscv_version().cmake_str + bit_suffix]

    # Specify python version, once as integer, once seperated by a dot
    pyver = "{}{}".format(sys.version_info.major, sys.version_info.minor)
    pyver_dot = "{}.{}".format(sys.version_info.major, sys.version_info.minor)

    if is_windows():
        cmake_args += ["-DPYTHONVER:STRING=" + pyver]

    if is_linux():
        cmake_args += ["-DPYTHONVERDOT:STRING=" + pyver_dot]

    # Libraries
    def is_required(lib):
        if "require_lib_" + lib in config and config["require_lib_" + lib] in ["1", "yes", "y"]:
            return True
        return False

    if is_required("eigen") and not have_eigen():
        fatal_error("Your Panda3D build was not compiled with eigen support, but it is required!")
        
    if is_required("bullet") and not have_bullet():
        fatal_error("Your Panda3D build was not compiled with bullet support, but it is required!")

    if is_required("freetype") and not have_freetype():
        fatal_error("Your Panda3D build was not compiled with freetype support, but it is required!")

    if have_eigen():
        cmake_args += ["-DHAVE_LIB_EIGEN=TRUE"]
    if have_bullet():
        cmake_args += ["-DHAVE_LIB_BULLET=TRUE"]
    if have_freetype():
        cmake_args += ["-DHAVE_LIB_FREETYPE=TRUE"]

    # Optimization level
    optimize = 3

    if args.optimize is None:
        # No optimization level set. Try to find it in the config
        if "optimize" in config:
            optimize = config["optimize"]
    else:
        optimize = args.optimize

    # Verbose level
    if "verbose_igate" in config:
        cmake_args += ["-DIGATE_VERBOSE=" + str(config["verbose_igate"])]
    else:
        cmake_args += ["-DIGATE_VERBOSE=0"]

    cmake_args += ["-DOPTIMIZE=" + str(optimize)]

    output = try_execute("cmake", join_abs(get_script_dir(), ".."), *cmake_args, error_formatter=handle_cmake_error)


def run_cmake_build(config, args):
    """ Runs the cmake build which builds the final output """

    configuration = "Release"
    if config["generate_pdb"].lower() in ["1", "true", "yes", "y"]:
        configuration = "RelWithDebInfo"

    # get number of cores, leave one for the system though
    num_cores = max(1, multiprocessing.cpu_count() - 1)

    core_option = ""
    if is_linux():
        # On linux, use all available cores
        core_option = "-j" + str(num_cores)
    if is_windows():
        # Specifying no cpu count makes MSBuild use all available ones
        core_option = "/m"

    try_execute("cmake", "--build", ".", "--config", configuration, "--", core_option)
