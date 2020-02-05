#!/usr/bin/env python3
#

import json
import os
import requests
import sys
import time

def write_status_codes(l):
    write_json(sorted(status_codes), 'status_codes.json')

def write_json(l, f):
    with open(f, 'w') as fp:
        json.dump(l, fp, indent=2, sort_keys=True)

status_codes = []
url = 'https://services.gradle.org/versions/all'
r = requests.get(url)
status_codes.append([url, r.status_code])
if r.status_code != 200:
    write_status_codes(status_codes)
    sys.exit()
data = []
checksums = dict()
for i in r.json():
    if i.get('snapshot') or i.get('nightly') or i.get('releaseNightly'):
        continue
    data.append(i)
write_json(data, 'all.json')

for i in data:
    for url in (i.get('checksumUrl'), i.get('wrapperChecksumUrl'), i['downloadUrl'][:-7] + 'all.zip.sha256'):
        if not url:
            continue
        print(url)
        while True:
            try:
                r = requests.get(url)
                break
            except Exception as e:
                print('retry', e)
                time.sleep(60)
        status_codes.append([url, r.status_code])
        if r.status_code == 200:
            sha256 = r.text.strip().lower()
            with open(os.path.basename(url), 'w') as fp:
                fp.write(sha256)
            checksums[url[:-7]] = sha256
        write_status_codes(status_codes)
    write_json(checksums, 'checksums.json')
