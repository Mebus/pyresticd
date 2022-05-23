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
from monitor.monitor import PyresticDMonitor

# Configuration
restic_password = ""

# Load Configuration
config = configparser.ConfigParser()
config.read("pyresticd.cfg")

# Program
def logthis(msg):

    msg = msg + " at {}".format(time.ctime())

    print(msg)
    syslog.syslog(msg)

def do_cleanup(password):
    
    # Log start
    logthis("Starting pyresticd Cleanup")

    restic_args = (
        " forget --keep-weekly=260 --keep-monthly=30000 --keep-yearly=1000 "
        + " --cache-dir "
        + config["restic"]["cache"]
    )

    return run_restic_with_args(restic_args, password)

def do_prune(password):
    
    # Log start
    logthis("Starting pyresticd Prune")

    restic_args = (
        " prune "
        + " --cache-dir "
        + config["restic"]["cache"]
    )

    return run_restic_with_args(restic_args, password)

def do_unlock(password):

    # Log start
    logthis("Starting pyresticd Unlock")

    restic_args = (
        " unlock "
        + " --cache-dir "
        + config["restic"]["cache"]
    )

    return run_restic_with_args(restic_args, password)

def run_restic_with_args(restic_args, password):
    
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
    logthis("Finished restic run")

    return ps.returncode

if __name__ == "__main__":

    pm = PyresticDMonitor()
    print(pm.ascii_art())

    print("PyResticD Cleanup")

    if not restic_password and "RESTIC_PASSWORD" in os.environ:
        restic_password = os.environ["RESTIC_PASSWORD"]

    if not restic_password:
        restic_password = getpass.getpass(
            prompt="Please enter the restic encryption password: "
        )
        print("Password entered.")

    """
    run the cleanup
    """

    #do_unlock(restic_password)

    # forget
    if do_cleanup(restic_password) == 0:

        # prune if forget was ok
        do_prune(restic_password)


