#!/usr/bin/env python3
#

import json
import os
import requests
import sys

def write_status_codes(l):
    with open('status_codes.json', 'w') as fp:
        json.dump(sorted(l), fp, indent=2, sort_keys=True)

status_codes = []
url = 'https://services.gradle.org/versions/all'
r = requests.get(url)
status_codes.append([url, r.status_code])
if r.status_code != 200:
    write_status_codes(status_codes)
    sys.exit()
data = []
for i in r.json():
    if i.get('snapshot') or i.get('nightly') or i.get('releaseNightly'):
        continue
    data.append(i)
with open('all.json', 'w') as fp:
    json.dump(data, fp, indent=2, sort_keys=True)

for i in data:
    for url in (i.get('checksumUrl'), i.get('wrapperChecksumUrl'), i['downloadUrl'][:-7] + 'all.zip.sha256'):
        if not url:
            continue
        print(url)
        r = requests.get(url)
        status_codes.append([url, r.status_code])
        if r.status_code == 200:
            with open(os.path.basename(url), 'w') as fp:
                fp.write(r.text)
        write_status_codes(status_codes)
