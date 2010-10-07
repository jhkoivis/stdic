#!/usr/bin/python
"""

	Simo Tuomisto, 2010

"""


import inspect 
import os
import configparser

class MasterData:
	""" XXX: to be removed """
	
	def __init__(self):
		self.masterdata = dict()
		
	def get(self, key):
		""" Get's data from dictionary."""
		return self.masterdata[key]

	def check(self, key):
		""" Check if key is in dictionary. """
		return key in self.masterdata

	def set(self, key, value):
		""" Put's data to dictionary."""
		self.masterdata[key] = value
