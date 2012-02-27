#!/usr/bin/python
import tarfile, time, sys, os, imp
preparing = imp.load_source("preparing", "/usr/share/pyshared/spirulabackup/preparing.py")
##############################################FRONT END MODULES#######################################################  
#										==>DIRECTORIES MODULES SECTION<==

#	==>reading configuration file
backupDirectories = preparing.ConfFileReader('general', 'backupDirectories', True)
if not backupDirectories:
	sys.exit(2)

directoryList = preparing.ConfFileReader('directories', 'directoryList')

#	==>back up directories
def backupDir(backupDirs):
	'''backup directories listed in configuration file'''
	today = time.strftime("%Y-%m-%d", time.localtime())
	tar = tarfile.open(today+".tar.gz","w|gz") #archiving required directories / files
	for dir in backupDirs:
		archive = dir.split()
		try:
			tar.add(archive[0])
		except OSError:
			print archive[0]+" doesn't exist :("

	tar.close()
	return tar.name

#	==>execution zone.
dirArchiveNames = []
preparing.CreateWorkingDir()
backups = directoryList.split(",") 
dirArchiveNames.append(backupDir(backups))

