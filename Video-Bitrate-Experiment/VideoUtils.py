import sys, subprocess, cv2
from subprocess import Popen, PIPE
from configparser import NoOptionError, SafeConfigParser as ConfigParser
from os import path

class FrameImage:
	def __init__(self, source, target, faces, timestamp):
		self.source = source
		self.target = target
		self.faces = faces
		self.timestamp = timestamp
		self.image = None

	def buildImage(self):
		pargs = [
			"ffmpeg",
			"-i",
			self.source,
			"-vframes",
			"1",
#			"-q:v",
#			"2",
			"-ss",
			self.timestamp,
			self.target
		]

		Popen(pargs, stdout=PIPE).wait()

	def loadImage(self):
		assert path.isfile(self.target), "No such file \"" + str(self.target) + "\""
		self.image = cv2.imread(self.target)


class FrameExtracter:
	def __init__(self):
		self.outputFolder = None
		self.frames = None

	@staticmethod
	def extractFrame(istreamStr, ostreamStr, timestamp):
		pargs = [
			"ffmpeg",
			"-i",
			istreamStr,
			"-vframes",
			"1",
#			"-q:v",
#			"2",
			"-ss",
			timestamp,
			ostreamStr
		]

		Popen(pargs, stdout=PIPE).wait()

	def setOutputFile(self, folder):
		self.outputFolder = folder

	def setConfigFile(self, istream):
		parser = ConfigParser()
		parser.readfp(istream)

		sections = parser.section()

		self.frames = []

		for s in sections:
			source = parser.get(s, "source")

			try:
				faces = parser.get(s, "faces")
			except NoOptionError:
				faces = None

			timestamp = parser.get(s, "timestamp")

			target = str(s) + ".png"

			self.frames.append(FrameImage(source, target, faces, timestamp))
			self.frames[-1].loadFrameImage()

class CodecReference:
	def __init__(self, encode, decode):
		self.encode = encode
		self.decode = decode

class Codec:
	class Encode:
		@staticmethod
		def x265(istreamStr, ostreamStr, resolution, fps, bitrate, start, duration, frames):
			pargs = [
				"ffmpeg",
				"-i",
				str(istreamStr),
			]

			# remove sound channels
			pargs.append("-an")

			if resolution:
				pargs.append("-vf")
				pargs.append("scale=" + str(resolution))
			if fps:
				pargs.append("-r")
				pargs.append(str(fps))

			if bitrate:			
				pargs.append("-b:v")
				pargs.append(str(bitrate) + "k")

			if start:
				pargs.append("-ss")
				pargs.append(str(start))
			
			if duration:
				pargs.append("-t")
				pargs.append(str(duration))

			
			if frames:
				pargs.append("-frames")
				pargs.append(str(frames))

			pargs.append("-c:v")
			pargs.append("libx265")

			pargs.append(str(ostreamStr))

			print(pargs)

			encoder = Popen(pargs, stdout=PIPE)

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
		def x264(istreamStr, ostreamStr, resolution, fps, bitrate, start, duration, frames):
			pargs = [
				"ffmpeg",
				"-i",
				str(istreamStr),
			]

			# remove sound channels
			pargs.append("-an")

			if resolution:
				pargs.append("-vf")
				pargs.append("scale=" + str(resolution))
			if fps:
				pargs.append("-r")
				pargs.append(str(fps))

			if bitrate:			
				pargs.append("-b:v")
				pargs.append(str(bitrate) + "k")

			if start:
				pargs.append("-ss")
				pargs.append(str(start))
			
			if duration:
				pargs.append("-t")
				pargs.append(str(duration))

			
			if frames:
				pargs.append("-frames")
				pargs.append(str(frames))

			pargs.append("-c:v")
			pargs.append("libx265")

			pargs.append(str(ostreamStr))

			print(pargs)

			encoder = Popen(pargs, stdout=PIPE)

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
		"x264" : CodecReference(Encode.x264, Decode.x264),
		"h265" : CodecReference(Encode.x265, Decode.x265),
		"h264" : CodecReference(Encode.x264, Decode.x264)
	}
