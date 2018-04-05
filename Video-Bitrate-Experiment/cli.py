#!/usr/bin/python3

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

from Encoding import Codec
from VideoConfigReader import ConfigReader

import os.path as path


VERSION = "0.0.2"

BANNER = """
R2D2 Encoder CLI Tool v%s
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

	class Meta:
		label = "base"
		description = "Bitrate Encoder Help Tool used for Live Video Feed R2D2 Research"
		arguments = [
			(["--conf"], dict(help="Allow for reading .conf files for bulk encoding. Usage: cli encode --conf videos.conf")),
			(["-v", "--version"], dict(action="version", version=BANNER)),
			(["-i", "--input"], dict(help="Input file")),
			(["-o", "--output"], dict(help="Output file (dir when --conf is specified)")),
			(["-c", "--codec"], dict(help="Codec options: " + ", ".join(Codec.codecs.keys()))),
			(["-b", "--bitrate"], dict(help="Encoding bitrate")),
			(["-res", "--resolution"], dict(help="Encoded video resolution")),
			(["-f", "--fps"], dict(help="Encoded video fps")),
			(["-s", "--start"], dict(help="Video timestamp to start encoding")),
			(["-t", "--duration"], dict(help="Video timestamp to last encoding")),
		]

	@expose(hide=True)
	def default(self):
		print("No command specified")

	@expose()
	def decode(self):
		print("Unimplemented!")
		exit(2)

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
				print("Encoding: " + target)
				print("\tresolution: " + str(f.resolution))
				print("\tfps: " + str(f.fps))
				print("\tcodec " + str(f.codec))
				print("\tbitrate " + str(f.bitrate) + "kbps")
				print("\tstart " + str(f.start))
				print("\tend " + str(f.duration))
			
				self.app.pargs.codec = f.codec
				codec = self.getCodec()

#codec.encode(inputFile, outputFile, resolution, fps, bitrate, start, duration)
				codec.encode(f.source, target, f.resolution, f.fps, f.bitrate, f.start, f.duration)
		else:
			inputFile = self.getInputFile()
			outputFile = self.getOutputFile()
			resolution = self.getResolution()
			fps = self.getFPS()
			codec = self.getCodec()
			bitrate = self.getBitrate()
			start = self.getVideoStart()
			duration = self.getVideoDuration()

			codec.encode(inputFile, outputFile, resolution, fps, bitrate, start, duration)

class App(CementApp):
	class Meta:
		label = "R2D2-Encoder-CLI-Tool"
		base_controller = Controller


with App() as app:
	app.run()
