#!/usr/bin/python
"""

	Simo Tuomisto, 2010

"""

import os
import re
import inspect

#------------------------------------------------------------------------------

class MasterData:

	def __init__(self, configfile):

		self.masterdata = dict()

		self.set("Caller", os.path.split(inspect.stack()[1][1])[1])
		self.set("ConfigFile", configfile)

		try:
			configfile = open(configfile, 'r')
		except IOError:
			print 
			raise IOError("No configuration file called " + str(configfile) + " found.")

		configExpression	= re.compile('\[(?P<configparagraph>.+)\]$')									#[<configparagraph>]
		numberExpression	= re.compile('(?P<float>[0-9.]+)$')												#<number> = <numbers 0-9 and .>
		stringExpression	= re.compile('\"(?P<string>.+)\"$')												#"<string>"
		tupleExpression		= re.compile('\(\s*(?P<number1>[0-9.]+)\s*,\s*(?P<number2>[0-9.]+)\s*\)$')		#(<number1> surrounded by whitespace,<number2> surrounded by whitespace)
		regExpression		= re.compile('\<(?P<reg>.+)\>$')												#<<regular expression group>>

		configparagraph = None

		for line in configfile:

			uncommentedline = line.split('#', 1)[0].strip()

			if uncommentedline == '':
				continue

			configmatch = configExpression.match(uncommentedline)

			if configmatch != None:
				configparagraph = configmatch.group('configparagraph')
				continue
				
			formattedline = uncommentedline.split('=', 1)

			if len(formattedline) == 1:
				raise Exception("Configuration file has a line that's not of the form <key>=<value>: " + line)

			if configparagraph == self.get("Caller") or configparagraph == "all":

				key		= formattedline[0].strip()
				value	= formattedline[1].strip()
				numbermatch	= numberExpression.match(value)
				stringmatch	= stringExpression.match(value)
				tuplematch	= tupleExpression.match(value)
				regmatch	= regExpression.match(value)

				if numbermatch != None:
					foundFloat = self.makeNumber(numbermatch.group('float'))
					self.set(key, foundFloat)
					
				elif tuplematch != None:
					value1 = tuplematch.group('number1')
					value2 = tuplematch.group('number2')
					foundTuple = (self.makeNumber(value1), self.makeNumber(value2))
					self.set(key, foundTuple)
					
				elif stringmatch != None:
					foundString = stringmatch.group('string')
					self.set(key, foundString)
					
				elif regmatch != None:
					foundReg = regmatch.group('reg')
					self.set(key, self.formatReg(foundReg))

				else:
					raise Exception("No proper type found for value on line: " + line)

		configfile.close()

	def makeNumber(self, number):
		try:
			try:
				inumber = int(number)
				return inumber
			except ValueError:
				fnumber = float(number)
				return fnumber
		except ValueError:
			raise Exception("Could not convert to a number: " + number)

	def get(self, key):

		# Get's data from dictionary.

		return self.masterdata[key]

	def set(self, key, value):

		# Put's data to dictionary.

		self.masterdata[key] = value

	def check(self, key):

		# Check if key is in dictionary.

		return key in self.masterdata

	def formatReg(self, regExpression):

		regExpression = regExpression.replace(".", "\.")
		regExpression = regExpression.replace("<ignore>", ".+")
		regExpression = regExpression.replace("<","(?P<")
		regExpression = regExpression.replace(">", ">\w+)")

		return regExpression
