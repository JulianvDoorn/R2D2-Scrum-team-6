#!/usr/bin/python3

# This script puts all video frames in the appropriate folder named after their corresponding bit rate segment in the filename.

from os import walk, rename
import re

def explode_filename(filename):
	m = re.search(r"(.+)_(.+?)_(.+?)_(.+?)_(.+?)_(.+?)\.(.+?)$", filename)

	if m is not None:
		name = m.group(1)
		dimensions = m.group(2)
		fps = m.group(3)
		encoding = m.group(4)
		bitrate = m.group(5)
		timestamp = m.group(6)
		return (name, dimensions, fps, encoding, bitrate, timestamp)
	else:
		return None

files = []
for (dirpath, dirnames, filenames) in walk("results/"):
    files.extend(filenames)
    break

for filename in files:
	t = explode_filename(filename)

	if t is not None:
		name, dimensions, fps, encoding, bitrate, timestamp = t
		rename("results/" + filename, "results/" + bitrate + "/" + filename)
