# Compatible since ranger 1.7.0 (git commit c82a8a76989c)
#
# This plugin hides the directories "/boot", "/sbin", "/proc" and "/sys" unless
# the "show_hidden" option is activated.

# Save the original filter function

from __future__ import (absolute_import, division, print_function)

import ranger.container.directory
import os
from subprocess import getstatusoutput

ACCEPT_FILE_OLD = ranger.container.directory.accept_file

# Define a new one
def gitignore_filter(fobj, filters):
    sts = fobj.fm.settings
    if sts.vcs_aware and sts.vcs_backend_git == 'enabled' and not sts.show_hidden:
        dirname, filename = os.path.split(fobj.path)
        cmd = f'cd {dirname}; git ls-files -z --others --directory --ignored --exclude-standard'
        retcode, ignored_files = getstatusoutput(cmd)
        if retcode != 0:
            return ACCEPT_FILE_OLD(fobj, filters)
        ignored_files = [ os.path.normpath(f) for f in ignored_files.split('\0')[:-1] ]
        if filename in ignored_files:
            return False
    return ACCEPT_FILE_OLD(fobj, filters)


# Overwrite the old function
ranger.container.directory.accept_file = gitignore_filter
