#!/usr/bin/env python3

import os
import sys
import time
import json
import requests
from functools import partial
from datetime import datetime as dt

get_offer_endpoint = 'http://api.itjobs.pt/job/get.json'

list_offers_endpoint = 'http://api.itjobs.pt/job/list.json'

locations = ["Braga", "Porto", "Coimbra", "Internacional"]


class Job(object):
    def __init__(self, offer):
        self.title = offer["title"]
        self.company = offer["company"]["name"]
        self.locations = ", ".join([loc["name"] for loc in offer["locations"]])
        if offer.get("types"):
            self.horarios = ", ".join([t["name"] for t in offer["types"]])
        else:
            self.horarios = None
        self.contracts = ", ".join([c["name"] for c in offer["contracts"]])
        self.published = dt.strptime(offer["publishedAt"], "%Y-%m-%d %H:%M:%S")

    def __str__(self):
        footer = f'{self.locations}\t{self.contracts}\t{self.horarios}'
        return f'{self.title}\n{self.company}\n{footer}'


def locations_filter(preferred_locations, job_offer):
    for location in preferred_locations:
        if location in job_offer.locations:
            return True
    return False


coolCities = partial(locations_filter, locations)


def latest_job_offer(api_key):
    data = {'api_key': api_key, 'limit': 1}
    resp = requests.post(list_offers_endpoint, data=data)
    jobs = json.loads(resp.text)["results"]
    jobs = filter(coolCities, map(Job, jobs))
    jobs = sorted(jobs, key=lambda job: job.published, reverse=True)
    return jobs[0]


def notify(job_offer):
    os.system(f'notify-send "Job Offer" "{job_offer}"')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the api_key as an argument")
        sys.exit(1)
    api_key = sys.argv[1]
    current_offer = latest_job_offer(api_key)
    notify(current_offer)
    while True:
        offer = latest_job_offer(api_key)
        if offer.published > current_offer.published:
            current_offer = offer
            notify(current_offer)
        print("Sleeping for 5 minutes")
        time.sleep(5*60)
