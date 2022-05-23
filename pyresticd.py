#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import getpass
import schedule
import configparser
import subprocess
import syslog
import datetime
import json

# Configuration

restic_password = ""

# Load Configuration

config = configparser.ConfigParser()
config.read("pyresticd.cfg")
backup_at = config["pyresticd"]["backup_at"]
day_interval = int(config["pyresticd"]["day_interval"])

# Constants

infofile_api_version = "0.1.0-beta"

# Program


def logthis(msg):

    msg = msg + " at {}".format(time.ctime())

    print(msg)
    syslog.syslog(msg)


def do_restic_backup(password):

    # Log start
    logthis("Starting pyresticd Backup")

    restic_args = (
        "backup "
        + config["pyresticd"]["src_dir"]
        + " --exclude-file excludes.txt --cache-dir "
        + config["restic"]["cache"]
        + " --exclude-caches"
    )

    # run restic
    args = [config["restic"]["binary"]] + restic_args.split()

    ps = subprocess.Popen(
        args,
        env={
            "B2_ACCOUNT_ID": config["B2"]["B2_ACCOUNT_ID"],
            "B2_ACCOUNT_KEY": config["B2"]["B2_ACCOUNT_KEY"],
            "RESTIC_PASSWORD": password,
            "RESTIC_REPOSITORY": config["pyresticd"]["repo"],
            "PATH": os.environ["PATH"],
        },
    )

    ps.wait()

    # Log finish
    logthis("Finished pyresticd Backup")

    if config["infofile"]["enabled"]:

        success = False
        if ps.returncode == 0:
            success = True

        # write infofile
        infofile = {
            "infofile_api_version": infofile_api_version,
            "backup_name": config["pyresticd"]["backup_name"],
            "day_interval": config["pyresticd"]["day_interval"],
            "when": datetime.datetime.utcnow().isoformat(),
            "success": success,
        }

        print(json.dumps(infofile))

        with open(config["infofile"]["path"], "w") as f:
            json.dump(infofile, f)


print("=" * 30)
print("Restic Scheduler")
print("=" * 30)
print("Repository: " + config["pyresticd"]["repo"])
print("backup at: " + backup_at)
print("day interval: " + str(day_interval))

print("-" * 30)

if not restic_password and "RESTIC_PASSWORD" in os.environ:
    restic_password = os.environ["RESTIC_PASSWORD"]

if not restic_password:
    restic_password = getpass.getpass(
        prompt="Please enter the restic encryption password: "
    )
    print("Password entered.")

# Immediate Backup

answer = input("Run a backup just now? [y/n]")
if answer and answer[0].lower() == "y":
    do_restic_backup(restic_password)

# Scheduling

schedule.every(day_interval).days.at(backup_at).do(do_restic_backup, restic_password)

while True:
    schedule.run_pending()
    time.sleep(1)
