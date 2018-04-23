import ast
from configparser import NoOptionError, SafeConfigParser as ConfigParser

class VideoConfig:
	def __init__(self, filename, source, resolution, fps, bitrate, codec, start, duration, frames):
		self.filename = filename
		self.source = source
		self.resolution = resolution
		self.fps = fps
		self.bitrate = bitrate
		self.codec = codec
		self.start = start
		self.duration = duration
		self.frames = frames

class ConfigReader:
	def __init__(self, istream):
		self.parser = ConfigParser()
		self.parser.readfp(istream)

	# returns a list of all output files and their properties
	def getOutputSets(self):
		li = []
		sections = self.parser.sections()
		
		for s in sections:
			source = self.parser.get(s, "source")
			resolutions = ast.literal_eval(self.parser.get(s, "resolution"))
			bitrates = ast.literal_eval(self.parser.get(s, "bitrate"))
			fpss = ast.literal_eval(self.parser.get(s, "fps"))
			codecs = ast.literal_eval(self.parser.get(s, "codec"))

			try: # make optional
				start = self.parser.get(s, "start")
			except NoOptionError:
				start = None

			try:
				duration = self.parser.get(s, "duration")
			except NoOptionError:
				duration = None

			try:
				frames = self.parser.get(s, "frames")
			except NoOptionError:
				frames = None

			filetype = self.parser.get(s, "filetype")

			for r in resolutions:
				for b in bitrates:
					for f in fpss:
						for c in codecs:
							li.append(VideoConfig(
								str(s) + "_" + str(r) + "_" + str(f) + "_" + str(c) + "_" + str(b) + "k" + "." + filetype,
								source,
								r,
								f,
								b,
								c,
								start,
								duration,
								frames
							))

		return li
						
# example:
# configFile = ConfigReader(open("videos.conf"))
# for f in configFile.getOutputSets():
# 	print(f.filename)
