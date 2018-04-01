#!/usr/bin/python3

import sys, subprocess
from subprocess import Popen, PIPE


def x265(file_in, file_out, bitrate, begin, frames):
	encoder = Popen([
		"x265",
		"--seek", "0",
		"--frames", "0",
		"--bitrate", str(bitrate),
		"--input", str(file_in),
		"--output", str(file_out),
		"--seek", str(begin),
		"--frames", str(frames)
	], stdout=PIPE)

	if file_out == "-":
		mplayer = Popen([
			"mplayer",
			"-cache", "524288",
			"-"
		], stdin=encoder.stdout, stdout=PIPE)

		mplayer.wait()
		print("Finished playback")

	encoder.wait()


def x264(file_in, file_out, bitrate, begin, frames):
	encoder = Popen([
		"x264",
		"--seek", "0",
		"--frames", "0",
		"--bitrate", str(bitrate),
		"--seek", str(begin),
		"--frames", str(frames),
		"-o", str(file_out),
		str(file_in)
	], stdout=PIPE)

	if file_out == "-":
		mplayer = Popen([
			"mplayer",
			"-cache", "524288",
			"-"
		], stdin=encoder.stdout, stdout=PIPE)

		mplayer.wait()
		print("Finished playback")

	encoder.wait()


# args:
# arg[1] = x265 | x264,
# arg[2] = bitrate,
# arg[3] = input video file,
# arg[4] = output video file (default: -),
# arg[5] = begin:frames
def main(args):
	codec = args[1]
	bitrate = args[2]
	input_file = args[3]

	if len(args) > 4:
		output_file = args[4]
	else:
		output_file = "-"

	if len(args) > 5:
		li = args[5].split(":")
		begin = int(li[0])
		frames = int(li[1])
	else:
		begin = 0
		frames = 0

	if codec == "x265":
		x265(input_file, output_file, bitrate, begin, frames)
	elif codec == "x264":
		x264(input_file, output_file, bitrate, begin, frames)


if __name__ == "__main__":
	main(sys.argv)
