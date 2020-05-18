#!/usr/bin/env python3
#

import apt
import binascii
import debian.debfile
import hashlib
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
            with open(os.path.join('sha256', os.path.basename(url)), 'w') as fp:
                fp.write(sha256)
            checksums[url[:-7]] = sha256
        write_status_codes(status_codes)
    write_json(checksums, 'checksums.json')


# check Debian package
cache = apt.Cache()
cache.open()
package = cache.get('libgradle-core-java', None)
if package:
    packageFileName = os.path.basename(package.candidate.filename)
    package.candidate.fetch_binary()
    deb = debian.debfile.DebFile(packageFileName)
    for filepath, listed_md5 in deb.md5sums().items():
        filepath = filepath.decode()
        if filepath.startswith('usr/share/java/gradle-wrapper') \
           and filepath.endswith('.jar'):
            d = dict()
            md5_hasher = hashlib.md5()
            sha256_hasher = hashlib.sha256()
            with deb.data.get_file(filepath) as fp:
                content = fp.read()
            md5_hasher.update(content)
            md5 = binascii.hexlify(md5_hasher.digest()).decode()
            sha256_hasher.update(content)
            sha256 = binascii.hexlify(sha256_hasher.digest()).decode()
            if listed_md5 == md5:
                checksums[os.path.basename(packageFileName) + ':' + filepath] = sha256
                d['arch'] = package.architecture()
                d['md5'] = md5
                d['sha256'] = sha256
                d['filepath'] = filepath
                d['packageFileName'] = packageFileName
                d['packageMd5'] = package.candidate.md5
                d['packageName'] = package.name
                d['packageSha256'] = package.candidate.sha256
                d['packageSize'] = package.candidate.size
                d['url'] = package.candidate.uri
                d['version'] = package.candidate.version
                data.append(d)
    write_json(data, 'all.json')
    write_json(checksums, 'checksums.json')
