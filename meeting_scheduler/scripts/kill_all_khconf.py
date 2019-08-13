#! /usr/bin/env python

import psutil
from subprocess import call

for p in psutil.process_iter():
    cmdline = p.cmdline()
    if len(cmdline) > 1 and cmdline[1] == '/var/lib/khconf/sipcall.py':
        call(['/var/lib/khconf/stop', cmdline[2], cmdline[3]])
