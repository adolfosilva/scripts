#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exports your Twitter following users list to a CSV file.
"""

import sys
import csv

from twitter import Twitter, OAuth


def following_list(twitter):
    r = twitter.friends.list(count=200)
    friends = r["users"]
    while r["next_cursor"] != 0:
        r = twitter.friends.list(count=200, cursor=r["next_cursor"])
        friends += r["users"]
    return friends


def save_file(filename, friends):
    with open(filename, 'w') as f:
        fieldnames = ['id', 'username', 'name']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for friend in friends:
            id_str = friend["id_str"]
            username = friend["screen_name"]
            name = friend["name"]
            writer.writerow({'id': id_str, 'username': username, 'name': name})


def _usage():
    args = "token token_secret consumer_key consumer_secret output_file.csv"
    print("Usage: {} {}".format(sys.argv[0], args))


if __name__ == '__main__':
    if len(sys.argv) < 6:
        _usage()
        sys.exit(1)
    else:
        auth = OAuth(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        t = Twitter(auth=auth)
        save_file(sys.argv[5], following_list(t))
