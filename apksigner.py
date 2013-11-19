#!/usr/bin/env python

import argparse
import glob
import os
import os.path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description='Filter logcat by package name')
parser.add_argument('apkfile', help='Original Apk file')
parser.add_argument('-o', '--output', dest='output', help='output apk path')

args = parser.parse_args()

# default android debug key
# TODO: make it configurable
keystore = os.path.join(os.path.expanduser("~"), ".android/debug.keystore")
keypass = "android"
storepass = "android"
alias = "androiddebugkey"

# output apk file
if args.output:
	newapk = args.output
else:
	name, ext = os.path.splitext(args.apkfile)
	newapk = name + "-signed" + ext

tempdir = tempfile.mkdtemp()

unzip_command = ['unzip']
unzip_command.extend(['-d', tempdir])
unzip_command.append('-q')
unzip_command.append(args.apkfile)

subprocess.call(unzip_command)

filelist = glob.glob(os.path.join(tempdir, "META-INF/*"))
for f in filelist:
	os.remove(f)

os.chdir(tempdir)
zip_command = ['zip']
zip_command.append('-r')
zip_command.append('-q')
zip_command.append(newapk)
zip_command.append('.')

subprocess.call(zip_command)

jarsigner_command = ['jarsigner']
jarsigner_command.extend(['-keystore', keystore])
jarsigner_command.extend(['-keypass', keypass])
jarsigner_command.extend(['-storepass', storepass])
jarsigner_command.append(newapk)
jarsigner_command.append(alias)

subprocess.call(jarsigner_command)

print "output to " + newapk
