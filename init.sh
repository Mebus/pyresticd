#!/bin/bash
export B2_ACCOUNT_ID="yyy"
export B2_ACCOUNT_KEY="xxx"
~/restic/restic -r b2:mybackup init

