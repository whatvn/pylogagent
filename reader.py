#!/usr/bin/env python
# Logging agent
#       Copyright 2011 Hung Nguyen <hungnv@opensource.com.vn>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import socket
import sys
import os, time
import atexit
from signal import SIGTERM 

class Reader(object):
	def __init__(self, logfile):
		self.logfile = logfile 
	
	def _readfirst(self):
		"""
		Every log file configured in configuration has a temporary db
		if we define a log file: /data/log/application.log, temprorary db 
		will have name application.log, it store last position when pylogagent check 
		for new lines.
		Do not read if files don't have new lines.
		"""
		dbfile = self.logfile.split('/')[-1].strip()  
		if os.path.isfile(dbfile):
			try:
				f = open(self.logfile.strip()) 
				f.seek(-3,2)
				p  = open(dbfile)
				cp = p.read()
				print "last possition: " + cp 
				print "current possition: " + str(f.tell())
				if (f.tell() + 3)  != int(cp):
					print "Read next!"
					lt = self._readnext(cp)
				else:
					f.close() 
					return 
				f.close() 
				return lt
			except IOError: 
				f.close() 
				return 
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
		"""
		If files are updated, use this function
		"""
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
		"""Put lines to log socket"""
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		s.connect('/dev/log')
		s.send(line)
		s.close()          

def _worker():
	while True:
		with open('configuration') as filelist:
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


	
