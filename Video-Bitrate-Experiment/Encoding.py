import sys, subprocess
from subprocess import Popen, PIPE

class CodecReference:
	def __init__(self, encode, decode):
		self.encode = encode
		self.decode = decode

class Codec:
	class Encode:
		@staticmethod
		def x265(istreamStr, ostreamStr, bitrate, beginFrame, endFrame):
			print([
				"x265",
				"--bitrate", str(bitrate),
				"--input", str(istreamStr),
				"--output", str(ostreamStr),
				"--seek", str(beginFrame),
				"--frames", str(endFrame - beginFrame)
			])

			encoder = Popen([
				"x265",
				"--bitrate", str(bitrate),
				"--input", str(istreamStr),
				"--output", str(ostreamStr),
				"--seek", str(beginFrame),
				"--frames", str(endFrame - beginFrame)
			], stdout=PIPE)

			if ostreamStr == "-":
				mplayer = Popen([
					"mplayer",
					"-cache", "524288",
					"-"
				], stdin=encoder.stdout, stdout=PIPE)

				mplayer.wait()
				print("Finished playback")

			encoder.wait()

		@staticmethod
		def x264(istreamStr, ostreamStr, bitrate, beginFrame, endFrame):
			encoder = Popen([
				"x264",
				"--bitrate", str(bitrate),
				"--seek", str(beginFrame),
				"--frames", str(endFrame - beginFrame),
				"-o", str(ostreamStr),
				str(istreamStr)
			], stdout=PIPE)

			if ostreamStr == "-":
				mplayer = Popen([
					"mplayer",
					"-cache", "524288",
					"-"
				], stdin=encoder.stdout, stdout=PIPE)

				mplayer.wait()
				print("Finished playback")

			encoder.wait()

	class Decode:
		@staticmethod
		def x265(instream, outstream):
			raise Exception("Unimplemented!")

		@staticmethod
		def x264(instream, outstream):
			raise Exception("Unimplemented!")

	codecs = {
		"x265" : CodecReference(Encode.x265, Decode.x265),
		"x264" : CodecReference(Encode.x264, Decode.x264)
	}
