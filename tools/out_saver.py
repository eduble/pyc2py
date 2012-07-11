#!/usr/bin/python2

import sys

class out_saver:
	def __init__(self):
		self.saved_stdout = sys.stdout
	def write(self, text):
		self.s += text
	def retrieve(self):
		return self.s
	def start(self):
		self.s = ""
		sys.stdout = self
	def stop(self):
		sys.stdout = self.saved_stdout
		return self.s


