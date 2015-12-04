

import sys
import os

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python build.py <module-name>")
        sys.exit(1)

    # Just execute the build script
    from Scripts.setup import make_output_dir, run_cmake, run_cmake_build
    make_output_dir()
    run_cmake(sys.argv[1])
    run_cmake_build()

    print("Success!")
    sys.exit(0)
