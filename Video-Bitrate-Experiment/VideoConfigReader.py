import ast
from configparser import SafeConfigParser as ConfigParser

class VideoConfig:
	def __init__(self, filename, source, resolutions, fpss, bitrates):
		self.filename = filename
		self.source = source
		self.resolutions = resolutions
		self.fpss = fpss
		self.bitrates = bitrates

class Config:
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

			for r in resolutions:
				for b in bitrates:
					for f in fpss:
						li.append(VideoConfig(
							str(s) + "_" + str(r) + "_" + str(f) + "_" + str(b) + "k",
							source,
							r,
							f,
							b
						))

		return li
						
# example:
# configFile = Config(open("videos.conf"))
# for f in configFile.getOutputSets():
# 	print(f.filename)
