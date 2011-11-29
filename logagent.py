#!/usr/bin/env python 
# Start our program as a daemon

from  daemon import daemon 
from reader import __worker

print "aaaaa"
with daemon.DaemonContext(pidfile="agent.pid"):
	print "starting logging agent....."
	__worker() 

