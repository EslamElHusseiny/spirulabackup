#!/usr/bin/python

import os, shutil, sys, time, imp
preparing = imp.load_source("preparing", "/usr/share/pyshared/spirulabackup/preparing.py")

###########################################Back End Modules############################################################  
#	==>reading configuration file
localFileSystem = preparing.ConfFileReader('general', 'localFileSystem', True)
if not localFileSystem:
	sys.exit(2)

workingDir = preparing.ConfFileReader('general', 'workingDir')
backupPath = preparing.ConfFileReader('localFS', 'backupPath')
retention = preparing.ConfFileReader('general', 'retention')

#	==>localFs Module
def localFS(backupPath,workingDir="/tmp/backup"):
	'''move backup to specific local filesystem'''
	if os.path.isdir(backupPath):
		archiveNames = os.listdir(workingDir) #list finished backups in working dir to be moved
		for archiveName in archiveNames:
			try:
				shutil.move(os.path.join(workingDir,archiveName),backupPath) #performing moving 
			except:
				os.rename(os.path.join(workingDir,archiveName),os.path.join(backupPath,archiveName)) #in case of existence of same backup forcing moving with overwriting
	else:
		print backupPath+" doesn't exist :("
		sys.exit(4)
###############################################RETENTION SECTION################################################################# 
#	==>local retention
def localRetention(days, backupPath):
	'''retention of local filesystem's backup'''
	archives = os.listdir(backupPath) #list current backups
	for archive in archives: 
		created = os.path.getmtime(os.path.join(backupPath,archive)) #get last modification time of backups
		today = time.strftime('%s',time.localtime())	#get today time
		diff = int(today)-created
		if (diff >= int(days)*8640): #performing retention according to given number of days to keep backup
			os.remove(os.path.join(backupPath,archive))

#	==>execution zone
try:
	if workingDir:
		localFS(backupPath,workingDir)
	else:
		localFS(backupPath)	
except OSError:
	sys.exit(4)

#	===>retention
localRetention(retention, backupPath)

