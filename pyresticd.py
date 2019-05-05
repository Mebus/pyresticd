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

restic_password = ''

# Load Configuration

config = configparser.ConfigParser()
config.read("pyresticd.cfg")
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

    restic_args = "backup " + config['pyresticd']['src_dir'] + " --exclude-file excludes.txt --cache-dir " + config['restic']['cache'] + " --exclude-caches"

    # run restic
    args = [config['restic']['binary']] + restic_args.split()

    ps = subprocess.Popen(args, env={
        'RESTIC_PASSWORD': password,
        'RESTIC_REPOSITORY': config['pyresticd']['repo'],
        'PATH': os.environ['PATH'],
    })

    ps.wait()

    #Log finish
    logthis('Finished pyresticd Backup')


print('=' * 30)
print('Restic Scheduler')
print('=' * 30)
print("Repository: " + config['pyresticd']['repo'])
print("backup at: " + backup_at)
print("day interval: " + str(backup_at))

print('-' * 30)

if not restic_password and 'RESTIC_PASSWORD' in os.environ:
    restic_password = os.environ['RESTIC_PASSWORD']

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
