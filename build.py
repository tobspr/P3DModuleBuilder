#!/usr/bin/python

import sys
import os

if __name__ == "__main__":

    # Find cached module name
    module_name = ""
    module_cfg_file = "module_name.cfg"
    if os.path.isfile(module_cfg_file):
        with open(module_cfg_file, "r") as handle:
            module_name = handle.read().strip()
    else:
        if sys.version_info.major > 2:
            raw_input = input
        module_name = str(raw_input("Enter a module name: "))
        with open(module_cfg_file, "w") as handle:
            handle.write(module_name)

    # Just execute the build script
    from Scripts.setup import make_output_dir, run_cmake, run_cmake_build
    make_output_dir()
    run_cmake(module_name)
    run_cmake_build()

    print("Success!")
    sys.exit(0)
