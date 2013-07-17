'''
  @file linear_regression.py
  @author Marcus Edel

  Class to benchmark the weka Linear Regression method.
'''

import os
import sys
import inspect

# Import the util path, this method even works if the path contains symlinks to
# modules.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(
	os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../util")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)

from log import *
from profiler import *

import shlex
import subprocess
import re
import collections

'''
This class implements the Linear Regression benchmark.
'''
class LinearRegression(object):

	''' 
	Create the Linear Regression benchmark instance.
  
  @param dataset - Input dataset to perform Linear Regression on.
  @param path - Path to the mlpack executable.
  @param verbose - Display informational messages.
	'''
	def __init__(self, dataset, path=os.environ["WEKA_CLASSPATH"], verbose=True): 
		self.verbose = verbose
		self.dataset = dataset
		self.path = path

	'''
	Destructor to clean up at the end.
	'''
	def __del__(self):		
		pass	
		
	'''
  Linear Regression. If the method has been successfully completed return 
  the elapsed time in seconds.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or -1 if the method was not successful.
  '''
	def RunMethod(self, options):
		Log.Info("Perform Linear Regression.", self.verbose)

		# Load input dataset.
    # If the dataset contains two files then the second file is the responses
    # file. In this case we add this to the command line.
		if len(self.dataset) == 2:
			cmd = shlex.split("java -classpath " + self.path + ":methods/weka" + 
				" LinearRegression -i " + self.dataset[0] + " -r " + self.dataset[1] 
				+ " " + options)
		else:
			cmd = shlex.split("java -classpath " + self.path + ":methods/weka" + 
				" LinearRegression -i " + self.dataset + " " + options)

		# Run command with the nessecary arguments and return its output as a byte
		# string. We have untrusted input so we disables all shell based features.
		try:
			s = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)		
		except Exception:
			Log.Fatal("Could not execute command: " + str(cmd))
			return -1

		# Return the elapsed time.
		timer = self.parseTimer(s)
		if not timer:
			Log.Fatal("Can't parse the timer")
			return -1
		else:
			time = self.GetTime(timer)
			Log.Info(("total time: %fs" % time), self.verbose)

			return time

	'''
	Parse the timer data form a given string.

	@param data - String to parse timer data from.
	@return - Namedtuple that contains the timer data.
	'''
	def parseTimer(self, data):
		# Compile the regular expression pattern into a regular expression object to
		# parse the timer data.
		pattern = re.compile(r"""
				.*?total_time: (?P<total_time>.*?)s.*?
				""", re.VERBOSE|re.MULTILINE|re.DOTALL)
		
		match = pattern.match(data)
		if not match:
			Log.Fatal("Can't parse the data: wrong format")
			return -1
		else:
			# Create a namedtuple and return the timer data.
			timer = collections.namedtuple("timer", ["total_time"])
			
			if match.group("total_time").count(".") == 1:
				return timer(float(match.group("total_time")))
			else:
				return timer(float(match.group("total_time").replace(",", ".")))

	'''
	Return the elapsed time in seconds.

	@param timer - Namedtuple that contains the timer data.
	@return Elapsed time in seconds.
	'''
	def GetTime(self, timer):
		time = timer.total_time
		return time