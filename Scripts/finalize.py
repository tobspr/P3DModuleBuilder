from __future__ import print_function

# This script just copies the generated .pyd file to the current directory.

import sys
sys.dont_write_bytecode = True

import platform
from shutil import copyfile
from os.path import isfile, join, dirname, realpath, isdir

from panda3d.core import PandaSystem

from common import *

# Storage for the precompiled render pipeline binaries
# BINARY_STORAGE = "E:\Dropbox\Sonstiges\PrecompiledBuilds"
MODULE_NAME = "RSNative"

def find_binary():
    """ Returns the path to the generated binary and pdb file """

    # Stores where we find the generated binary
    source_file = None

    # Stores where we find the generated PDB
    pdb_file = None

    curr_dir = get_script_dir()
    possible_files = []
    possible_pdb_files = []
    target_pdb_file = MODULE_NAME + ".pdb"

    if is_windows():

        # Check the different Configurations
        configurations = ["Release", "RelWithDebInfo"]
        target_file = MODULE_NAME + ".pyd"

        for config in configurations:
            possible_files.append(join(get_output_dir(), config, MODULE_NAME + ".dll"))

    elif is_linux():
        target_file = MODULE_NAME + ".so"
        possible_files.append(join(get_output_dir(), target_file))

    for file in possible_files:
        if isfile(file):
            source_file = file

            pdb_name = file.replace(".so", ".pdb").replace(".dll", ".pdb")
            if isfile(pdb_name):
                pdb_file = pdb_name

    return source_file, pdb_file


if __name__ == "__main__":

    source_file, pdb_file = 

    if source_file:

        dest_folder = join(curr_dir, "../../Code/Native")

        # Copy the generated DLL
        copyfile(source_file, join(dest_folder, target_file))

        # Copy the generated PDB (if it was generated)
        if pdb_file:
            copyfile(pdb_file, join(dest_folder, target_pdb_file))


        if isdir(BINARY_STORAGE):

            # Copy DLL to the precompiled binary dir
            target_filename = "RSNative_" + PandaSystem.getPlatform() + ".pyd"
            target_filename = join(BINARY_STORAGE, target_filename)

            copyfile(source_file, target_filename)

    else:
        print("Failed to find source file at", ' or '.join(possible_files), "!", file=sys.stderr)
