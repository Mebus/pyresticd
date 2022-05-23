#!/usr/bin/python3

import urllib.request
import json
import datetime
import dateutil.parser


class PyresticDMonitor:
    def process_host(self, url):

        with urllib.request.urlopen(url) as remote:
            data = json.loads(remote.read().decode())
            when = dateutil.parser.isoparse(data["when"])
            time_delta = (datetime.datetime.utcnow() - when).days

            print(data["backup_name"])
            print("%s days ago" % str(time_delta))
            if data["success"] and (time_delta <= float(data["day_interval"])):
                print("OK")
            else:
                print("FAIL")

            print("-" * 30)

    def run(self):

        f = open("inventory.json")
        data = json.load(f)
        for ho in data["hosts"]:
            self.process_host(ho["url"])

        # Closing file
        f.close()


if __name__ == "__main__":

    print("=" * 30)
    pm = PyresticDMonitor()
    pm.run()
    print("=" * 30)
