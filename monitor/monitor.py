#!/usr/bin/python3

from tkinter import W
import urllib.request
import json
import datetime
import dateutil.parser
import sys


class PyresticDMonitor:

    failure = False

    def aprint(self, text):
        self.ascii += text + "\n"

    def ascii_art(self):
        return """
                                  __                  __     
                                 /\ \__ __           /\ \    
 _____   __  __  _ __   __    ___\ \ ,_/\_\    ___   \_\ \   
/\ '__`\/\ \/\ \/\`'__/'__`\ /',__\ \ \\/\ \  /'___\ /'_` \  
\ \ \L\ \ \ \_\ \ \ \/\  __//\__, `\ \ \\ \ \/\ \__//\ \L\ \ 
 \ \ ,__/\/`____ \ \_\ \____\/\____/\ \__\ \_\ \____\ \___,_\\
  \ \ \/  `/___/> \/_/\/____/\/___/  \/__/\/_/\/____/\/__,_ /
   \ \_\     /\___/                                          
    \/_/     \/__/
"""

    def process_host(self, ho):

        with urllib.request.urlopen(ho["url"]) as remote:
            data = json.loads(remote.read().decode())
            when = dateutil.parser.isoparse(data["when"])
            time_delta = (datetime.datetime.utcnow() - when).days

            self.ascii += data["backup_name"] + "\n"
            self.ascii += "%s days ago\n" % str(time_delta)
            if data["success"] and (time_delta <= float(data["day_interval"])):
                self.ascii += "OK\n"
            else:
                if ho["ignore"]:
                    self.ascii += "fail (ignored)\n"
                else:
                    self.failure = True
                    self.ascii += "FAIL\n"

            self.aprint("-" * 30)

    def run(self):

        self.ascii = ""
        self.aprint(self.ascii_art())

        f = open("inventory.json")
        data = json.load(f)
        for ho in data["hosts"]:
            self.process_host(ho)

        # Closing file
        f.close()


if __name__ == "__main__":
    pm = PyresticDMonitor()
    pm.run()
    print(pm.ascii)

    if pm.failure:
        print("\nWARNING: at least one backup >>> HAS FAILED <<<.\n")
        sys.exit(2)

    else:
        sys.exit(0)
