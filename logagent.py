#!/usr/bin/env python 
# Start our program as a daemon

from daemon import daemon
from reader import __worker

with daemon.DaemonContext():
    worker()

