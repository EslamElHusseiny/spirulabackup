#!/usr/bin/python

#requirements: apt-get install python-paramiko
import os, paramiko, sys, time, shutil
from ConfigParser import ConfigParser, NoOptionError, NoSectionError

###############################################PREPARATION SECTION#####################################################
configFile = '/etc/spirulabackup/backup.conf'

#	==>preparing working directory
def CreateWorkingDir(workingDir="/tmp/backup"):
	'''preparing working directory for different backup operations'''
	if not os.path.exists(workingDir):
		os.mkdir(workingDir)
	os.chdir(workingDir)

#	==>reading config file function
def ConfFileReader(section, option, boolean=False):
	'''reading configuration file parameter and set non exitstent parameter to False'''
	config = ConfigParser()
	config.read(configFile)

	if not boolean:	#for non boolean options
		try:		#check existence of section / option
			opt = config.get(section, option)
		except NoOptionError, NoSectionError:
			opt = False
	else:			#for boolean options
		try:		#check existence of section / option
			opt = config.getboolean(section, option)
		except NoOptionError, NoSectionError:
			opt = False
	return opt
##################################################CLEANING####################################################################### #	==>Cleaner 
def Cleaner(workingDir="/tmp/backup"):
	'''cleaning and removing working directory at the end of backup operation'''
	shutil.rmtree(workingDir)

