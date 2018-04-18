import sys, subprocess
from subprocess import Popen, PIPE

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
