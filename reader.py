#!/usr/bin/env python
# Logging agent
# HUNGNV 29/2011
import socket
import re
import sys
import os, time

class Reader(object):
	def __init__(self, logfile):
		self.logfile = logfile 
	
	def _readfirst(self):
		dbfile = self.logfile.split('/')[-1].strip()  
		if os.path.isfile(dbfile):
			f = open(self.logfile.strip()) 
			f.seek(-3, 2)
			p  = open(dbfile)
			cp = p.read()
			print "last possition: " + cp 
			print "current possition: " + str(f.tell())
			if f.tell() != cp:
				print "Read next!"
				lt = self._readnext(cp)
			f.close() 
			return lt
		else:
			print "Read log file 1st time!" 
			f = open(self.logfile.strip()) 
			lt = set() 
			for line in f:
				line = dbfile.split('.')[0] + ": "  + line
				lt.add(line) 
			current_possition = f.tell()
			with open(dbfile,'w') as db:
				db.write(str(current_possition))
			f.close()
			return lt 
	
	def _readnext(self, possition):
		dbfile = self.logfile.split('/')[-1].strip()
		with open(self.logfile.strip()) as f: 
			lt = set()
			print "possition: %s"  %(possition)
			f.seek(int(possition))
			for line in f:
				line = dbfile.split('.')[0] + ": "  + line  
				lt.add(line) 	
			with open(dbfile,'w') as db:
				db.write(str(f.tell())) 
			return lt 	

	def _log(self, line):
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		s.connect('/dev/log')
		s.send(line)
		s.close()          
		#print "Received: ", repr(data)

def __worker():
	while True:
		filelist = open('configuration')
		for f in filelist:
			print "Reading file %s" %(f) 
			logger = Reader(f)
			logs   = logger._readfirst() 
			if logs is not None:
				try:
					for line in logs:
						if line: 
							logger._log(line)
						else: break 
				except TypeError: pass
			else: continue
		time.sleep(5)
