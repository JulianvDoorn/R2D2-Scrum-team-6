import ast, cv2
import os.path as path

from configparser import NoOptionError, SafeConfigParser as ConfigParser
from VideoUtils import FrameImage

class FaceRecognitionImage:
	def __init__(self, faceCascade, image, imageDir, faceCount):
		self.faceCascade = faceCascade
		self.image = image
		self.imageDir = imageDir
		self.faceCount = faceCount
		self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

	def recognize(self):
		faces = self.faceCascade.detectMultiScale(
		    self.gray,
		    scaleFactor=1.3,
		    minNeighbors=5,
		    minSize=(30, 30)
		)

		print("Found {0} faces of {1} faces at \"{2}\"".format(len(faces), self.faceCount, self.imageDir))
		print("Found {0} faces of {1} faces at \"{2}\"".format(len(faces), self.faceCount, self.imageDir), file=open(path.dirname(self.imageDir) + "/face-recognitions.log", "a"))

		for (x, y, w, h) in faces:
			cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)

	def dumpImage(self, dumpFile):
		cv2.imwrite(dumpFile, self.image)

class FaceRecognition:
	def __init__(self):
		self.images = None
		self.faceCascade = None
		self.tempFolder = None
		self.parser = None

	def doRecognitionRoutine(self, forceOverwrite = False, recognizeOnly = False):
		self.images = {}

		sections = self.parser.sections()

		for s in sections:
			sources = ast.literal_eval(self.parser.get(s, "sources"))

			try:
				faces = int(self.parser.get(s, "faces"))
			except NoOptionError:
				faces = None

			timestamp = self.parser.get(s, "timestamp")

			for source in sources:
				target = path.join(self.tempFolder, path.splitext(path.basename(source))[0] + "_" + str(timestamp) + ".png")

				if not path.isfile(target) or forceOverwrite:
					frameImage = FrameImage(source, target, faces, timestamp)

					if not recognizeOnly:
						frameImage.buildImage()

					frameImage.loadImage()

					self.images[target] = FaceRecognitionImage(self.faceCascade, frameImage.image, target, faces)

					if faces is not None:
						self.images[target].recognize()

					self.images[target].dumpImage(target)
				else:
					print("File \"" + str(target) + "\" already exists, skipping")

	def setFaceCascadeFile(self, cascadeFile):
		self.faceCascade = cv2.CascadeClassifier(cascadeFile)

	def setTempFolder(self, folder):
		self.tempFolder = folder

	def dumpDebugInfo(self):
		for key, image in self.images.items():
			image.dumpImage(path.join(self.tempFolder, str(key) + ".png"))

	def setConfigFile(self, istream):
		self.parser = ConfigParser()
		self.parser.readfp(istream)
