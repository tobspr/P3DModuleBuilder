#!/usr/bin/python

import sys
import os
from os.path import join, realpath, dirname

from Scripts.common import get_ini_conf, write_ini_conf

if __name__ == "__main__":

    # Python 2 compatibility
    if sys.version_info.major > 2:
        raw_input = input

    config_file = join(dirname(realpath(__file__)), "config.ini")
    config = get_ini_conf(config_file)

    # Find cached module name
    if "module_name" not in config or not config["module_name"]:
        module_name = str(raw_input("Enter a module name: "))
        config["module_name"] = module_name.strip()

    # Write back config
    write_ini_conf(config, config_file)

    # Just execute the build script
    from Scripts.setup import make_output_dir, run_cmake, run_cmake_build
    make_output_dir()
    run_cmake(config)
    run_cmake_build(config)

    print("Success!")
    sys.exit(0)
