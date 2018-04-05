#!/usr/bin/python3

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

from Encoding import Codec


VERSION = "0.0.1"

BANNER = """
R2D2 Encoder CLI Tool v%s
""" % VERSION

class Controller(CementBaseController):
	class Meta:
		label = "base"
		description = "Bitrate Encoder Help Tool used for Live Video Feed R2D2 Research"
		arguments = [
			(["-v", "--version"], dict(action="version", version=BANNER)),
			(["-i", "--input"], dict(help="Input file")),
			(["-o", "--output"], dict(help="Output file")),
			(["-c", "--codec"], dict(help="Codec options: " + ", ".join(Codec.codecs.keys()))),
			(["-b", "--bitrate"], dict(help="Encoding bitrate")),
			(["-r", "--range"], dict(help="Range of frames to encode formatted as BEGIN:END (example: 100:200)"))
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
		selectedCodec = self.app.pargs.codec
		inputFile = self.app.pargs.input
		outputFile = self.app.pargs.output
		bitrate = self.app.pargs.bitrate if self.app.pargs.bitrate else 0
		frameRange = self.app.pargs.range
		frameBegin = 0
		frameEnd = -1

		if inputFile is None:
			print("No input file provided")
			exit(1)

		if selectedCodec in Codec.codecs:
			print("Selected codec: " + str(selectedCodec))
			selectedCodec = Codec.codecs[selectedCodec].encode
		else:
			print("No such codec: " + str(selectedCodec))
			exit(1)

		if outputFile is not None:
			outputFile = self.app.pargs.output
		elif outputFile == "-":
			print("Using mplayer...")
		else:
			print("No output specified, writing to 'out'")
			outputFile = "out"

		if frameRange is not None:
			li = frameRange.split(":")
			frameBegin = int(li[0])
			frameEnd = int(li[1])
			

		selectedCodec(inputFile, outputFile, bitrate, frameBegin, frameEnd)

class App(CementApp):
	class Meta:
		label = "R2D2-Encoder-CLI-Tool"
		base_controller = Controller


with App() as app:
	app.run()
