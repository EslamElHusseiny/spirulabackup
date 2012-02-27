#!/usr/bin/python

import paramiko, os, sys, imp
preparing = imp.load_source("preparing", "/usr/share/pyshared/spirulabackup/preparing.py")
#####################################################Back End Module###########################################################  

#	==>reading configuration file
remoteFileSystem = preparing.ConfFileReader('general', 'remoteFileSystem', True)
if not remoteFileSystem:
	sys.exit(2)

workingDir = preparing.ConfFileReader('general', 'workingDir')
remoteHost = preparing.ConfFileReader('remoteFS', 'remoteHost')
remoteSSHPort = preparing.ConfFileReader('remoteFS', 'remoteSSHPort')
remoteUser = preparing.ConfFileReader('remoteFS', 'remoteUser')
remotePasswd = preparing.ConfFileReader('remoteFS', 'remotePasswd')
remotePath = preparing.ConfFileReader('remoteFS', 'remotePath')
retention = preparing.ConfFileReader('general', 'retention')

#	==>ssh connect
def sshConnect(hostName, port, userName, passwd):
	'''preparing a sftp object to be used later in either ssh or scp operations'''
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(hostName, port, userName, passwd)
	except:
		sys.exit(3)
	
	return ssh

#	==>SFTP Module
def remoteFS(ssh, remotePath, localPath='/tmp/backup'):
	'''performing secure copy of reday backup to remote filesystem'''
	sftp = ssh.open_sftp()
	archives = os.listdir(localPath) #listing ready backups from working directory
	for archive in archives:
		sftp.put(os.path.join(localPath, archive), os.path.join(remotePath, archive)) # moving ready backups to remote filesystem
	sftp.close()
###############################################RETENTION SECTION################################################################# #	==>remote retention
def remoteRetention(days,backupPath, ssh):
	'''performing remote retention according to given remote filesystem and number of days to keep backups'''
	stdout, stdin, stderr = ssh.exec_command('find '+backupPath+' -mtime '+days) #get remote filesystem's backups according to their last modification time
	archives = stdout.read().split('\n')
	for archive in archives:
			ssh.exec_command('rm -f '+archive) # perfoming retention 

#	===>execution zone
try:
	if workingDir:
		ssh = sshConnect(remoteHost, remoteSSHPort, remoteUser, remotePasswd)
		remoteFS(ssh, remotePath, workingDir)
	else:
		ssh = sshConnect(remoteHost, remoteSSHPort, remoteUser, remotePasswd)
		remoteFS(ssh, remotePath)
except:
	sys.exit(4)

#	===>retention
ssh = sshConnect(remoteHost, remoteSSHPort, remoteUser, remotePasswd)
remoteRetention(retention, remotePath, ssh)

