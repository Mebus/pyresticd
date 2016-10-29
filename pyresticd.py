#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import time
from subprocess import Popen
from twisted.internet import task
from twisted.internet import reactor


# Configuration

timeout = 3600*24*3 # Period
restic_executable = 'restic'
restic_args = ''
restic_password = ''

# Program


def do_restic_backup(password):
    print('Starting Backup at {}'.format(time.ctime()))
    args = [restic_executable] + restic_args.split()
    Popen(args, env={
        'RESTIC_PASSWORD': password
    })


print('Restic Scheduler')
print('-' * 30)
print('Timeout: {}'.format(timeout))
if not restic_password:
    restic_password = getpass.getpass(
        prompt='Please enter the restic encryption password: ')

l = task.LoopingCall(do_restic_backup, restic_password)
l.start(timeout)

reactor.run()
