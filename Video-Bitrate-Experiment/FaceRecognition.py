import cv2
import os.path as path

from configparser import NoOptionError, SafeConfigParser as ConfigParser
from VideoUtils import FrameImage

class FaceRecognitionImage:
	def __init__(self, faceCascade, image, faceCount):
		self.faceCascade = faceCascade
		self.image = image
		self.faceCount = faceCount
		self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

	def recognize(self):
		faces = self.faceCascade.detectMultiScale(
		    self.gray,
		    minNeighbors=5,
		    minSize=(30, 30)
		)

		print("Found {0} faces of {1} faces".format(len(faces), self.faceCount))

		for (x, y, w, h) in faces:
	    		cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)

	def dumpImage(self, dumpFile):
		cv2.imwrite(dumpFile, self.image)

class FaceRecognition:
	def __init__(self):
		self.images = None
		self.faceCascade = None
		self.tempFolder = None

	def doRecognitionRoutine(self):
		for key, image in self.images.items():
			image.recognize()

	def setFaceCascadeFile(self, cascadeFile):
		self.faceCascade = cv2.CascadeClassifier(cascadeFile)

	def setTempFolder(self, folder):
		self.tempFolder = folder

	def dumpDebugInfo(self):
		for key, image in self.images.items():
			image.dumpImage(path.join(self.tempFolder, str(key) + ".png"))

	def setConfigFile(self, istream):
		parser = ConfigParser()
		parser.readfp(istream)

		self.images = {}

		sections = parser.sections()

		for s in sections:
			source = parser.get(s, "source")
			target = path.join(self.tempFolder, str(s) + ".png")
			faces = int(parser.get(s, "faces"))
			timestamp = parser.get(s, "timestamp")

			if not path.isfile(target):
				frameImage = FrameImage(source, target, faces, timestamp)
				frameImage.buildImage()
				frameImage.loadImage()

				self.images[str(s)] = FaceRecognitionImage(self.faceCascade, frameImage.image, faces)
			else:
				print("File \"" + str(target) + "\" already exists, skipping")
