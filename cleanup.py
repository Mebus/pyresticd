#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import getpass
import schedule
import configparser
import subprocess
import syslog
import json
import datetime
import dateutil.parser
from time import gmtime, strftime
from pytz import timezone
import pytz
from datetime import timedelta

# Configuration

restic_args = ''
restic_password = ''

# Load Configuration

config = configparser.ConfigParser()
config.read("pyresticd.cfg")

restic_args = "-r " + config['pyresticd']['repo'] + " snapshots --json"

backup_interval_allowed = timedelta(days=int(config['cleanup']['interval_days']),
                                    hours=int(config['cleanup']['interval_hours']),  
                                    minutes=int(config['cleanup']['interval_minutes']),
                                    seconds=int(config['cleanup']['interval_seconds']))

def snapshots_to_delete(password):


    last_removed = False
    removelist = []             # list of snapshots to be removed!

    # run restic
    args = [config['restic']['binary']] + restic_args.split()

    ps = subprocess.Popen(args, env={
        'RESTIC_PASSWORD': password,
        'PATH': os.environ['PATH'],
    },
    stdout=subprocess.PIPE,
    )
    
    #ps.wait()

    json_input = ps.stdout.read()
    json_parsed = json.loads(json_input)
   
    last_backup = datetime.datetime(1, 1, 1, tzinfo=timezone('Europe/Berlin'))

    for data in json_parsed:

        data_datum = dateutil.parser.parse(data['time'])
        data_id = data['id'][:8]

        print("--------------")
        #print(data_datum.strftime('%d.%m.%Y %H:%M:%S'))
        print(data_id + " || " + data['time'])

        backup_interval_current = data_datum - last_backup
        print(backup_interval_current)

        if backup_interval_current < backup_interval_allowed and not last_removed:
            last_removed = True
            print("REMOVE")
            removelist.append(data_id)

        else:
            last_removed = False
        
        
        # save backup date for the next step
        last_backup = data_datum


    print("\nSummary for interval " + str(backup_interval_allowed) + "\n==========\n\nI found " + str(len(removelist)) + " of " + str(len(json_parsed)) + " snapshots to delete:\n")
    
    remove_string = ""

    for i in removelist:
        print(i+" ", end='')
        remove_string = remove_string + i + " "
    
    print()

    remove_command = config['restic']['binary'] + " -r " + config['pyresticd']['repo'] + " forget " + remove_string
    print("Suggested command: \n")
    print(remove_command)



if not restic_password:
    restic_password = os.environ['RESTIC_PASSWORD']

if not restic_password:
    restic_password = getpass.getpass(
        prompt='Please enter the restic encryption password: ')
    print("Password entered.")


snapshots_to_delete(restic_password)
