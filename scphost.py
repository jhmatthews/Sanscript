


'''

usage 
	scphost.py put/get/c/go host file1 file2
'''

import pexpect
import sys


######################
# read arguments

if len(sys.argv) < 2:
	print 'Usage: put/get/go host [path/to/file1 path/to/file2]'
	print "No arguments specified, Exiting."
	sys.exit()

for i in range(len(sys.argv)):
	if sys.argv[i]=='help':
		print 'Usage: put/get/go host [path/to/file1 path/to/file2]'
		sys.exit()


# are we doing scp?
if sys.argv[1]=='put' or sys.argv[1]=='get':

	# default Truth value is false
	Folder = False

	# check for folder flag
	for i in range(len(sys.argv)):
		if sys.argv[i]=='-r':
			Folder = True	

	# get arguments
	file1 = sys.argv[3]
	file2 = sys.argv[4]
	hostname = sys.argv[2]

	# if Folder we want to use -r 
	if Folder: 
		scp = "scp -r -oPubKeyAuthentication=no"
	else:
		scp= "scp -oPubKeyAuthentication=no"


# are we doing ssh?
elif sys.argv[1]=='go' or sys.argv[1]=='c' or sys.argv[1]=='connect' or sys.argv[1]=='con':

	ssh = "ssh"		# put ssh flags here!

	hostname = sys.argv[2]		# hostname only argument

elif sys.argv[1] == 'sftp':

	sftp = "sftp"

	hostname = sys.argv[2]		# hostname only argument

else:
	print 'Usage: put/get/go/sftp host [path/to/file1 path/to/file2]'
	print "Did not understand arguments, Exiting."
	sys.exit()



######################
# get hostnames and usernames


# Login for iridis 3
if hostname=='iridis':
	USER = "jm8g08"
	HOST = "iridis3_c.soton.ac.uk"
	PASS = "111Neverlose"
	HOME = "/home/jm8g08/"


# Login for iridis 4
if hostname=='i4':
	USER = "jm8g08"
	HOST = "iridis4_a.soton.ac.uk"
	PASS = "111Neverlose"
	HOME = "/home/jm8g08/"


# Login for ICG sciama cluster
if hostname=='sciama':
	USER = 'jmatthews'
	HOST = 'login2.sciama.icg.port.ac.uk'
	PASS = 'quidditch1'
	HOME = '/users/jmatthew'


# Login for astroaips
if hostname=='aips':
	USER = "jm8g08"
	HOST = "152.78.192.83"
	PASS = "11Neverlose"
	HOME = "/home/jm8g08/"


######################
#get commands

# if run with put then do scp to put file on remote
if sys.argv[1]=='put':
	FILE = file1
	REMOTE_FILE = HOME + file2
	COMMAND = "%s %s %s@%s:%s" % (scp, FILE, USER, HOST, REMOTE_FILE)


# if run with get then do scp to get file from remote
elif sys.argv[1]=='get':
	FILE = file2
	REMOTE_FILE = HOME + file1
	COMMAND = "%s %s@%s:%s %s" % (scp, USER, HOST, REMOTE_FILE, FILE)

# else, ssh into cluster
elif sys.argv[1]=='go' or sys.argv[1]=='c' or sys.argv[1]=='connect' or sys.argv[1]=='con':
	 COMMAND = "%s %s@%s" % (ssh, USER, HOST)


elif sys.argv[1]=='sftp':
	COMMAND = "%s %s@%s" % (sftp, USER, HOST)

######################
# finally RUNCMD
print COMMAND
child = pexpect.spawn(COMMAND)
child.expect('password:')
child.sendline(PASS)
child.expect(pexpect.EOF)
