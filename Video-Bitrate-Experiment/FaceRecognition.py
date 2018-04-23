import cv2
import os.path as path

from configparser import NoOptionError, SafeConfigParser as ConfigParser

# Get user supplied values
#imagePath = sys.argv[1]
#cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
#faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
#image = cv2.imread(imagePath)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
#faces = faceCascade.detectMultiScale(
#    gray,
#    scaleFactor=1.1,
#    minNeighbors=5,
#    minSize=(30, 30)
#)

#print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
#for (x, y, w, h) in faces:
#    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

#cv2.imshow("Faces found", image)
#cv2.waitKey(0)

class FaceRecognitionImage:
	def __init__(self, faceCascade, imageDir, faceCount):
		self.faceCascade = faceCascade
		self.image = cv2.imread(imageDir)
		self.faceCount = faceCount
		self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

	def recognize(self):
		faces = self.faceCascade.detectMultiScale(
		    self.gray,
		    scaleFactor=1.1,
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
		self.debugDumpFolder = None

	def doRecognitionRoutine(self):
		for key, image in self.images.items():
			image.recognize()

	def setFaceCascadeFile(self, cascadeFile):
		self.faceCascade = cv2.CascadeClassifier(cascadeFile)

	def dumpDebugInfo(self, dumpFolder):
		for key, image in self.images.items():
			image.dumpImage(path.join(dumpFolder, str(key) + ".png"))

	def setConfigFile(self, istream):
		parser = ConfigParser()
		parser.readfp(istream)

		self.images = {}

		sections = parser.sections()

		for s in sections:
			source = parser.get(s, "source")
			faceCount = int(parser.get(s, "faces"))
			self.images[str(s)] = FaceRecognitionImage(self.faceCascade, source, faceCount)
