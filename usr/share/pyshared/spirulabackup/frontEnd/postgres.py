#!/usr/bin/python

import sys, commands, time, os, tarfile, imp
preparing = imp.load_source("preparing", "/usr/share/pyshared/spirulabackup/preparing.py")
##############################################FRONT END MODULES#######################################################
#										==>POSTGRESQL DATABASE MODULES SECTION<==

#	==>reading configuretion file
backupPostgresql = preparing.ConfFileReader('general', 'backupPostgresql', True)
if not backupPostgresql:
	sys.exit(2)

pgHost = preparing.ConfFileReader('postgresql', 'pgHost')
pgPassword = preparing.ConfFileReader('postgresql', 'pgPassword')
pgUser = preparing.ConfFileReader('postgresql', 'pgUser')
pgList = preparing.ConfFileReader('postgresql', 'pgList')

#backup required databases
def backupPg(pgList, pgHost, pgUser, pgPassword):
	"""Backup a database (dump + compress)"""
	today = time.strftime("%Y-%m-%d", time.localtime())
	os.putenv("PGPASSWORD",pgPassword) #set PGPASSWORD enviromental variable for unattended dumping 
	if (pgList == "all"):
		print "if" # dump all databases
		backupFile = "all-"+today+".sql"
		commands.getoutput("pg_dumpall -h %s -U %s -f %s" %(pgHost, pgUser, backupFile))
	else: # dump certin list of databases
		databaseList = pgList.split(",")
		tar = tarfile.open(today+"-postgres"+".tar.gz","w|gz") #preparing tar archiving file
		for db in databaseList:
			database = db.split()[0]
			backupFile = database + ".sql"
			commands.getoutput("pg_dump -h %s -U %s -f %s %s" %(pgHost, pgUser, backupFile, database)) #dump database
			tar.add(backupFile)
			os.remove(backupFile)
		tar.close()

#	==>execution zone
preparing.CreateWorkingDir()
backupPg(pgList, pgHost, pgUser, pgPassword)
