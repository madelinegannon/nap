#!/usr/bin/env python3
import argparse
import os
from platform import machine
from subprocess import call
from sys import platform
import sys

LINUX_BUILD_DIR = 'build'
MACOS_BUILD_DIR = 'Xcode'
MSVC_BUILD_DIR = 'msvc64'
CODEBLOCKS_BUILD_DIR = 'codeblocks'
DEFAULT_LINUX_BUILD_TYPE = 'Release'

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'common'))
from nap_shared import get_cmake_path, get_nap_root

def generate(forced_path, enable_python, additional_dirs, linux_build_type):
    nap_root = get_nap_root()
    cmake = get_cmake_path()

    if platform.startswith('linux'):
        build_dir = forced_path if forced_path else os.path.join(nap_root, LINUX_BUILD_DIR)
        build_type = linux_build_type.lower().capitalize()
        call(['%s -H%s -B%s -DCMAKE_BUILD_TYPE=%s -DNAP_ENABLE_PYTHON=%s -DADDITIONAL_SUB_DIRECTORIES=%s' % (cmake, nap_root, build_dir, build_type, enable_python, additional_dirs)], shell=True)
    elif platform == 'darwin':
        build_dir = forced_path if forced_path else os.path.join(nap_root, MACOS_BUILD_DIR)
        call(['%s -H%s -B%s -G Xcode -DNAP_ENABLE_PYTHON=%s -DADDITIONAL_SUB_DIRECTORIES=%s' % (cmake, nap_root, build_dir, enable_python, additional_dirs)], shell=True)
    else:
        build_dir = forced_path if forced_path else os.path.join(nap_root, MSVC_BUILD_DIR)
        cmd = '%s -H%s -B%s -G "Visual Studio 16 2019" -DNAP_ENABLE_PYTHON=%s -DADDITIONAL_SUB_DIRECTORIES=%s' % (cmake, nap_root, build_dir, enable_python, additional_dirs)
        call(cmd, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build-path',
        type=str,
        default=None,
        action='store',
        help="Force custom build path")

    if platform.startswith('linux'):
        parser.add_argument('-t', '--linux-build-type',
            type=str,
            default=DEFAULT_LINUX_BUILD_TYPE,
            action='store', nargs='?',
            choices=['release', 'debug'],
            help="Linux build type (default: %s)" % DEFAULT_LINUX_BUILD_TYPE.lower())

    parser.add_argument('-p', '--enable-python', action="store_true",
        help="Enable python integration using pybind (deprecated)")

    parser.add_argument('-d', '--additional-dirs',
        nargs='+',
        type=str,
        default=[],
        help="List of additional sub directories to add to the build")

    args = parser.parse_args()

    # Convert additional sub directories to CMake list type
    additional_dirs = ';'.join(args.additional_dirs)

    # Get linux build type
    linux_build_type = args.linux_build_type if platform.startswith('linux') else None

    # Generate solution
    generate(args.build_path, int(args.enable_python), additional_dirs, linux_build_type)
