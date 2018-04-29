#!/usr/bin/python3

# This script extracts the result logs and prints them into stdout in csv format. Use the bash ">" operator to pipe the contents into a file.

import re

def find(str):
	m = re.search(r"Found (\d) faces of (\d) faces at \"(.+)\"", str)
	return (m.group(1), m.group(2), m.group(3))

def explode_filename(filename):
	m = re.search(r"/(.+)_(.+?)_(.+?)_(.+?)_(.+?)_(.+?)\.(.+?)$", filename)
	name = m.group(1)
	dimensions = m.group(2)
	fps = m.group(3)
	encoding = m.group(4)
	bitrate = m.group(5)
	timestamp = m.group(6)
	return (name, dimensions, fps, encoding, bitrate, timestamp)

fin = open("results/face-recognitions.log")

for line in fin:
	faces_found, faces_expected, fileDir = find(line.strip())
	print("; ".join(explode_filename(fileDir)), str(faces_found), str(faces_expected), sep="; ")
