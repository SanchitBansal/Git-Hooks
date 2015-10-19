#!C:\Python27\python

#
# An example hook script to check the commit log message.

# Called by "git commit" with one argument, the name of the file

# that has the commit message.  The hook should exit with non-zero

# status after issuing an appropriate message if it wants to stop the

# commit.  The hook is allowed to edit the commit message file.


import sys, re, os
import bugz
import bugz.bugzilla

def notify_and_exit(msg):
	print msg
	os._exit(1)

sBZUrl = "http://localhost/web/bugzilla427/"
sBZUser = "user@example.com"
sBZPasswd = "pass1234"
sBZAllowedStates = ['NEW', 'ASSIGNED', 'REOPENED']

with open(sys.argv[1], 'r') as f:
	first_line = f.readline()

log_bugid_regex = re.compile("^BugID:(?P<bug>\d+)")

if log_bugid_regex.match(first_line):
		
	bug_number = log_bugid_regex.search(first_line)
	bug_number = int(bug_number.group('bug'))

	## Bugzilla authentication check
	try:
		oBZ = bugz.bugzilla.Bugz(sBZUrl, user=sBZUser, password=sBZPasswd)
		oBZ.auth()
	except:
		notify_and_exit("Could not contact Bugzilla!")
	
	## Check if Bug exists
	try:
		oBug = oBZ.get(bug_number)
		if oBug is None:
			notify_and_exit("Bug %d does not exist" % (bug_number))			
	except:	
		notify_and_exit("Could not get status for bug %d" % (bug_number))	

	## Get Bug State
	oBugState = oBug.getroot().find("bug/bug_status").text
	if oBugState not in sBZAllowedStates:
		notify_and_exit("Bug %d is in '%s' state.\nPermissible Bug States are: %s." % (bug_number, oBugState, ", ".join(sBZAllowedStates)))
	else:
		os._exit(0)

else:
	print "The commit message does not match the required specifications"
	print "The first line must start from BugID:<bug number> commit message"
	print "Please note: BugID, at beginning of message, is case sensitive"
	print "\nExample:"
	print "BugID:1234 This is a sample commit message"
	os._exit(1)
