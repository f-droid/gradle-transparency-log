#!/bin/sh -ex

basedir=`pwd`
cd /tmp/fdroidserver
git checkout master
for f in `git log --reverse -- makebuildserver| grep ^commit\ | awk '{print $2}'`; do
    git show $f | grep '^\+' | grep /gradle- | grep -F .zip > /dev/null || continue
    git checkout $f
    $basedir/get-sha256-from-makebuildserver.py
    git -C $basedir add $basedir/*.sha256
    git -C $basedir commit --allow-empty $basedir/*.sha256 \
	--author="`git log -n1 --pretty=format:'%an <%ae>' $f`" \
	--date=`git log -n1 --pretty=format:%at` \
	-m "`git log -n1 --pretty=format:%s`" \
	-m "from https://gitlab.com/fdroid/fdroidserver/commit/$f"
done
