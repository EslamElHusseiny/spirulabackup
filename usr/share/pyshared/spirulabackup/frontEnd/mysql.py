#!/usr/bin/python
#requirements: apt-get install python-mysqldb
import MySQLdb, sys, commands, time, os, imp, tarfile
preparing = imp.load_source("preparing", "/usr/share/pyshared/spirulabackup/preparing.py")
##############################################FRONT END MODULES#######################################################
#										==>MYSQL MODULES SECTION<==

#	==>reading configuretion file
backupDatabases = preparing.ConfFileReader('general', 'backupMysql', True)
if not backupDatabases:
	sys.exit(2)

dbHost = preparing.ConfFileReader('mysql', 'dbHost')
dbPassword = preparing.ConfFileReader('mysql', 'dbPassword')
dbUser = preparing.ConfFileReader('mysql', 'dbUser')
databaseList = preparing.ConfFileReader('mysql', 'databaseList')

#prepare existing databases list
def getDatabaseList(dbHost,dbUser,dbPassword,db="mysql"):
	"""Gets the databases list from mysql.db table."""
	# if you have any deleted databases still exists in mysql.db, you'll get an error
	# user must have select, lock tables on all existing databases (including mysql)
	try:
		db = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPassword, db='mysql') #connecting to database using giving username and password
	except:
		print "Could not connect to 'mysql' database [%s@%s]" % (dbUser, dbHost)
		sys.exit(3)

	cursor = db.cursor()
	cursor.execute("select Db from db") #list all available databases 
	tmpDatabaseList = cursor.fetchall()
	cursor.close()
	
	databaseList = []
	for currentDatabase in tmpDatabaseList: #prepare a list of all available databases
		databaseList.append(currentDatabase[0])
	
	return databaseList
	
#backup required databases	
def backupDb(currentDatabase, dbHost, dbUser, dbPassword):
	"""Backup a database (dump + compress)"""
	backupFile = currentDatabase + ".sql"
	commands.getoutput("/usr/bin/mysqldump --host=%s --user=%s --password=%s %s > %s" % (dbHost, dbUser, dbPassword, currentDatabase, backupFile)) #dumping databases
	today = time.strftime("%Y-%m-%d", time.localtime())
	tar = tarfile.open(currentDatabase+"-"+today+".tar.gz","w|gz") #archiving dumped databases
	tar.add(backupFile)	
	tar.close()
	os.remove(backupFile)
	return tar.name

#	==>execution zone
commands.getoutput("/usr/bin/mysqlcheck --all-in-1 --silent --all-databases --auto-repair --optimize --host=%s --user=%s --password=%s" % (dbHost, dbUser, dbPassword))
preparing.CreateWorkingDir()
dbArchiveNames = []
if (databaseList == 'all'):
	dbList = getDatabaseList(dbHost,dbUser,dbPassword)
	for currentDatabase in dbList:
		dbArchiveNames.append(backupDb(currentDatabase, dbHost,dbUser,dbPassword))
else:
	dbList = databaseList.split(",")
	for currentDatabase in dbList:
			dbArchiveNames.append(backupDb(currentDatabase, dbHost,dbUser,dbPassword))

