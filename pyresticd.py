#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import getpass
import schedule
import configparser
import subprocess
import syslog

# Configuration

restic_args = ''
restic_password = ''

# Load Configuration

config = configparser.ConfigParser()
config.read("pyresticd.cfg")
restic_command = config['pyresticd']['restic_command']
backup_at = config['pyresticd']['backup_at']
day_interval = int(config['pyresticd']['day_interval'])

# Program

def logthis(msg):

    msg = msg + " at {}".format(time.ctime())

    print(msg)
    syslog.syslog(msg)


def do_restic_backup(password):

    # Log start
    logthis('Starting pyresticd Backup')

    # run restic
    args = [restic_command] + restic_args.split()

    ps = subprocess.Popen(args, env={
        'RESTIC_PASSWORD': password,
        'PATH': os.environ['PATH'],
    })

    ps.wait()

    #Log finish
    logthis('Finished pyresticd Backup')


print('=' * 30)
print('Restic Scheduler')
print('=' * 30)

print("restic command: " + restic_command)
print("backup at: " + backup_at)
print("day interval: " + str(backup_at))

print('-' * 30)

if not restic_password:
    restic_password = getpass.getpass(
        prompt='Please enter the restic encryption password: ')
    print("Password entered.")

# Immediate Backup

answer = input('Run a backup just now? [y/n]')
if answer and answer[0].lower() == 'y':
    do_restic_backup(restic_password)

# Scheduling

schedule.every(day_interval).days.at(backup_at).do(do_restic_backup, restic_password)

while True:
    schedule.run_pending()
    time.sleep(1)
