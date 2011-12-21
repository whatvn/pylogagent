#!/usr/bin/env python
# Create a customize socket to send log

import socket 

class Lsocket(object):
	def __init__(self, lsocket, device='/dev/log'):
		self.device  = device 
		self.lsocket = lsocket  

	def _lconnect(self):
		self.lsocket.connect(self.device) 

	def sendStream(self, msg):
		if msg: self.lsocket.send(msg) 
		else: self._ldisconnect()


	def _ldisconnect(self):
		self.lsocket.close() 

