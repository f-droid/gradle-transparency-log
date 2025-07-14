#!/usr/bin/python3

import glob
import os
import re

for f in glob.glob('/tmp/fdroidserver/makebuildserver'):
    print(f)
    with open(f, encoding='utf8') as fp:
        data = fp.read()
    for m in re.finditer(
        r'''['"](https?://[^'"]+gradle*[^'"]+)['"],\s*['"]([0-9a-f]+)['"]''',
        data,
        re.DOTALL,
    ):
        print(os.path.basename(m.group(1)), m.group(2))
        with open(
            f'/home/hans/code/fdroid/gradle-transparency-log/{os.path.basename(m.group(1))}.sha256',
            'w',
            encoding='utf8',
        ) as fp:
            fp.write(m.group(2).strip().lower())
    break
