#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import getpass
import time
from twisted.internet import task
from twisted.internet import reactor


# Configuration 

timeout = 3600*24*3 # Period
restic_command = "/home/mebus/restic" # your restic command here

# Program

def do_restic_backup():
    print "\nStarting Backup at " + str(time.ctime())
    os.system(restic_command)

print "\nRestic Scheduler\n----------------------------\n"
print "Timout ist: " + str(timeout)
restic_password = getpass.getpass(prompt="Please enter the restic encryption password: ")
os.environ["RESTIC_PASSWORD"] = restic_password

l = task.LoopingCall(do_restic_backup)
l.start(timeout)

reactor.run()
