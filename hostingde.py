#!/usr/bin/python

import requests
import json


class HostingDe:
    def check_free_space_nextcloud(self, apikey):

        required_gib = 40  # GiB

        url = "https://secure.hosting.de/api/managedapplication/v1/json/nextcloudsFind"
        post_data = {
            "limit": 1,
            "page": 1,
            "authToken": apikey,
        }

        dat = {"limitok": False}

        x = requests.post(url, json=post_data)

        if x.status_code == 200:
            jsondata = json.loads(x.text)

            for k in ["storageQuota", "storageUsed"]:
                dat[k] = jsondata["response"]["data"][0][k]

            free_gib = (dat["storageQuota"] - dat["storageUsed"]) / 1024

            if free_gib < required_gib:
                print(
                    "Free Nextcloud space {} GiB is less than our limit: {} GiB.".format(
                        free_gib, required_gib
                    )
                )
                dat["limitok"] = False
            else:
                dat["limitok"] = True

            print(dat)
            return dat


if __name__ == "__main__":
    hde = HostingDe()
    hde.check_free_space_nextcloud("myapikey")
