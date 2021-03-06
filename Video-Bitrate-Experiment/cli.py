#!/usr/bin/python3

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

from VideoUtils import Codec, FrameExtracter
from VideoConfigReader import ConfigReader
from FaceRecognition import FaceRecognition

import os.path as path
import sys

VERSION = "0.0.4"

BANNER = """
R2D2 Encoding and Test CLI Tool v%s
""" % VERSION

class Controller(CementBaseController):
	def getResolution(self):
		return self.app.pargs.resolution if self.app.pargs.resolution else None

	def getBitrate(self):
		return self.app.pargs.bitrate if self.app.pargs.bitrate else None

	def getFPS(self):
		return self.app.pargs.fps if self.app.pargs.fps else None


	def getInputFile(self):
		inputFile = self.app.pargs.input

		if inputFile is not None:
			return inputFile
		else:
			print("No input file provided")
			exit(1)

	def getVideoStart(self):
		return self.app.pargs.start if self.app.pargs.start else None

	def getVideoDuration(self):
		return self.app.pargs.duration if self.app.pargs.duration else None

	def getOutputFile(self):
		outputFile = self.app.pargs.output

		if outputFile is not None:
			return outputFile
		elif outputFile == "-":
			print("Using mplayer...")
		else:
			print("No output specified, writing to 'out'")
			return "out"

	def getCodec(self):
		selectedCodec = self.app.pargs.codec

		if selectedCodec in Codec.codecs:
			print("Selected codec: " + str(selectedCodec))
			return Codec.codecs[selectedCodec]
		else:
			print("No such codec: " + str(selectedCodec))
			exit(1)

	def getVideoFrameCount(self):
		return self.app.pargs.frames if self.app.pargs.frames else None

	class Meta:
		label = "base"
		description = "Bitrate Encoder Help Tool used for Live Video Feed R2D2 Research"
		arguments = [
			(["--conf"], dict(help="Allow for reading .conf files for bulk operations. Usage: cli encode --conf videos.conf \n cli face-recognition-test --conf faces.conf")),
			(["-v", "--version"], dict(action="version", version=BANNER)),
			(["-i", "--input"], dict(help="Input file")),
			(["-o", "--output"], dict(help="Output file (dir when --conf is specified)")),
			(["-c", "--codec"], dict(help="Codec options: " + ", ".join(Codec.codecs.keys()))),
			(["-b", "--bitrate"], dict(help="Encoding bitrate")),
			(["-res", "--resolution"], dict(help="Encoded video resolution")),
			(["-f", "--fps"], dict(help="Encoded video fps")),
			(["-s", "--start"], dict(help="Video timestamp to start encoding")),
			(["-t", "--duration"], dict(help="Video timestamp to last encoding")),
			(["--frames"], dict(help="The amount of frames to extract")),
			(["--timestamp"], dict(help="The timestamp of the frame to extract"))
		]

	@expose(hide=True)
	def default(self):
		print("No command specified")

	@expose()
	def extract_frame(self):
		confFile = self.app.pargs.conf
		source = self.app.pargs.input
		target = self.app.pargs.output
		timestamp = self.app.pargs.timestamp
		
		if confFile:
			assert target == None, "No output folder specified"

			extracter = FrameExtracter()
			extracter.setConfigFile(confFile)
			extracter.setOutputFolder(target)
		else:
			assert source == None, "No input specified"
			
			if target == None:
				print("No output specified, writing to out.png")
				target = "out.png"

			FrameExtracter.extractFrame(source, target, timestamp)

	@expose()
	def bin_results(self):
		# This command puts all video frames in the appropriate folder named after their corresponding bit rate segment in the filename.
		# This snippet was directly copied from a file previously named extract.py
		# Excuse its alfulness

		source = self.app.pargs.input

		assert source is not None, "No input specified"

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
		for (dirpath, dirnames, filenames) in walk(source):
		    files.extend(filenames)
		    break

		for filename in files:
			t = explode_filename(filename)

			if t is not None:
				name, dimensions, fps, encoding, bitrate, timestamp = t
				rename(source + filename, source + bitrate + "/" + filename)

	@expose()
	def extract_logs(self):
		# This command extracts the result logs and prints them into stdout or a file in csv format.
		# This snippet was directly copied from a file previously named extract.py
		# Excuse its alfulness

		source = self.app.pargs.input
		target = self.app.pargs.output

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

		assert source is not None, "No input specified"
		fin = open(source)

		if target is not None:
			fout = open(target, "w+")
		else:
			fout = sys.stdout

		for line in fin:
			faces_found, faces_expected, fileDir = find(line.strip())
			print("; ".join(explode_filename(fileDir)), str(faces_found), str(faces_expected), sep="; ", file=fout)

	@expose()
	def face_recognition_test(self):
		confFile = self.app.pargs.conf
		dumpFolder = self.app.pargs.output

		if confFile is None:
			print("No --conf specified")
			exit(1)

		faceRecognition = FaceRecognition()
		faceRecognition.setTempFolder(dumpFolder)
		faceRecognition.setFaceCascadeFile("haarcascade_frontalface_default.xml")
		faceRecognition.setConfigFile(open(confFile))
		faceRecognition.doRecognitionRoutine()

		if dumpFolder is not None:
			faceRecognition.dumpDebugInfo()

	@expose()
	def encode(self):
		confFile = self.app.pargs.conf

		if confFile is not None:
			print("Using configuration file: " + str(confFile))
			config = ConfigReader(open(confFile))

			outputFile = self.app.pargs.output
			if outputFile is None:
				outputFile = ""

			for f in config.getOutputSets():
				target = path.join(outputFile, f.filename)
				if not path.isfile(target):
					print("Encoding: " + target)
					print("\tresolution: " + str(f.resolution))
					print("\tfps: " + str(f.fps))
					print("\tcodec " + str(f.codec))
					print("\tbitrate " + str(f.bitrate) + "kbps")
					print("\tstart " + str(f.start))
					print("\tend " + str(f.duration))
					print("\tframes " + str(f.frames))

					self.app.pargs.codec = f.codec
					codec = self.getCodec()

					#codec.encode(inputFile, outputFile, resolution, fps, bitrate, start, duration, frames)
					codec.encode(f.source, target, f.resolution, f.fps, f.bitrate, f.start, f.duration, f.frames)
				else:
					print("Skipping: " + str(target))
		else:
			inputFile = self.getInputFile()
			outputFile = self.getOutputFile()
			resolution = self.getResolution()
			fps = self.getFPS()
			codec = self.getCodec()
			bitrate = self.getBitrate()
			start = self.getVideoStart()
			duration = self.getVideoDuration()
			frames = self.getVideoFrameCount()

			codec.encode(inputFile, outputFile, resolution, fps, bitrate, start, duration, frames)

class App(CementApp):
	class Meta:
		label = "R2D2-Encoder-CLI-Tool"
		base_controller = Controller


with App() as app:
	app.run()
