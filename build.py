#!/usr/bin/python

# Important: import panda3d as the very first library - otherwise it crashes
import panda3d.core  # noqa

import sys
import os
import argparse
from os.path import join, realpath, dirname

# Configure Logging Module
import logging

# Custom logging formatter
VERBOSE = logging.INFO - 1 # INFO== for verbose logging

class CustomLogFormatter(logging.Formatter):
    err_fmt  = "ERROR: %(message)s"
    dbg_fmt  = "DEBUG: %(module)s: %(lineno)d: %(message)s"
    info_fmt = "%(message)s"

    def __init__(self, fmt="%(msg)s"):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        format_orig = self._fmt
        if record.levelno == logging.DEBUG:
            self._fmt = CustomLogFormatter.dbg_fmt
#         elif record.levelno in (logging.INFO, VERBOSE):
#             self._fmt = CustomLogFormatter.info_fmt
        elif record.levelno == logging.ERROR:
            self._fmt = CustomLogFormatter.err_fmt
        result = super().format(record)
        self._fmt = format_orig
        return result

logging.addLevelName(VERBOSE, 'VERBOSE')
# -logger - add custom loglevel
def verbose(self, message, *args, **kwargs):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kwargs) 
#add method for verbose logging
logging.Logger.verbose = verbose
custom_log_format = CustomLogFormatter()
handler_hook = logging.StreamHandler()
handler_hook.setFormatter(custom_log_format)
logging.basicConfig(level=logging.DEBUG,
        format='%(message)s',
        handlers=[handler_hook])
logger = logging.getLogger(__name__)

# Change into the current directory
os.chdir(dirname(realpath(__file__)))

from scripts.common import get_ini_conf, write_ini_conf  # noqa
from scripts.setup import make_output_dir, run_cmake, run_cmake_build

if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(description="P3DModuleBuilder")
    parser.add_argument(
        '--optimize', type=int, default=None,
        help="Optimize level, should match the one used for the Panda3D build",)
    parser.add_argument(
        "--clean", action="store_true", help="Forces a clean rebuild")
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.verbose:
        logger.setLevel(VERBOSE)

    # Python 2 compatibility
    if sys.version_info.major > 2:
        raw_input = input

    config_file = join(dirname(realpath(__file__)), "config.ini")
    config = get_ini_conf(config_file)

    # Find cached module name
    if "module_name" not in config or not config["module_name"]:
        module_name = str(raw_input("Enter a module name: "))
        config["module_name"] = module_name.strip()

    # Check for outdated parameters
    for outdated_param in ["vc_version", "use_lib_eigen", "use_lib_bullet", "use_lib_freetype"]:
        if outdated_param in config:
            logger.warn("Removing obsolete parameter '" + outdated_param + "', is now auto-detected.")
            del config[outdated_param]

    # Write back config
    write_ini_conf(config, config_file)

    # Just execute the build script
    make_output_dir(clean=args.clean)
    run_cmake(config, args)
    run_cmake_build(config, args)

    logger.info("Success!")
