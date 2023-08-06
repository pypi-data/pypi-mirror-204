#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2023 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor                                              #
#                                                           #
#      Version: 8.0.1 -                                     #
#                                                           #
#############################################################
#
#
#  @File: pyarmor/core/cli/fixup.py
#
#  @Author: Jondy Zhao (pyarmor@163.com)
#
#  @Create Date: Fri Apr 14 17:43:59 CST 2023
#
import os
import sys

from subprocess import check_output, Popen, PIPE


def _shell_cmd(cmdlist):
    p = Popen(cmdlist, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return p.returncode, stderr


def _fixup_darwin_rpath(path, pyver):
    output = check_output(['otool', '-L', sys.executable])
    for line in output.splitlines():
        if line.find(b'Frameworks/Python.framework/Versions') > 0:
            pydll = line.split()[0].decode()
            break

        if line.find(('libpython' + pyver).encode('utf-8')) > 0:
            pydll = line.split()[0].decode()
            break
    else:
        return 'no found CPython shared library'

    # old = '@rpath/Frameworks/Python.framework/Versions/%s/Python' % pyver
    old = '@rpath/lib/libpython%s.dylib' % pyver
    cmdlist = ['install_name_tool', '-change', old, pydll, path]
    rc, err = _shell_cmd(cmdlist)
    if rc:
        raise 'install_name_tool failed (%d): %s' % (rc, err)

    identity = '-'
    cmdlist = ['codesign', '-s', identity, '--force',
               '--all-architectures', '--timestamp', path]
    rc, err = _shell_cmd(cmdlist)
    if rc:
        return 'codesign failed (%d): %s' % (rc, err)

    return rc


def _fixup_library_not_load(path):
    if not (path and os.path.exists(path)):
        return

    pyver = '%s.%s' % sys.version_info[:2]
    platform = sys.platform
    if platform == 'darwin':
        return

    elif platform.startswith('linux'):
        return 'try to install package "libpython%s" to fix it' % pyver

    elif platform.startswith('win'):
        return
