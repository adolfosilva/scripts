#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
from datetime import datetime

def notify(title, message):
    subprocess.Popen(['notify-send', title, message])

while True:
    now = datetime.now()
    if (now.hour > 22):
        wakeup = now.replace(day=now.day + 1, hour=7, minute=30)
        remaining = wakeup - now
        hours, minutes = remaining.seconds // 3600, remaining.seconds // 60 % 60
        notify("Sleep Time", "You now have {}h{}m to sleep".format(hours, minutes))
    time.sleep(60*5)
