import cv2
import operator
import numpy as np

MIN_CONTOUR_AREA = 200.0
MAX_CONTOUR_AREA = 500.0
RESIZED_IMAGE_WIDTH = 100
RESIZED_IMAGE_HEIGHT = 100
PATH = 'testImages/sample9.jpg'

class ContourWithData():

	npaContour = None           # contour
	boundingRect = None         # bounding rect for contour
	intRectX = 0                # bounding rect top left corner x location
	intRectY = 0                # bounding rect top left corner y location
	intRectWidth = 0            # bounding rect width
	intRectHeight = 0           # bounding rect height
	fltArea = 0.0               # area of contour

	def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
		
		[intX, intY, intWidth, intHeight] = self.boundingRect
		self.intRectX = intX
		self.intRectY = intY
		self.intRectWidth = intWidth
		self.intRectHeight = intHeight


	def checkIfContourIsValid(self):                            # contour selection
		ratio = float( self.intRectWidth ) / self.intRectHeight
		if ratio >= 2  and ratio <= 5 and (self.fltArea > MIN_CONTOUR_AREA and self.fltArea < MAX_CONTOUR_AREA) : return True        # much better validity checking would be necessary
		return False 


def preprocessing(img):

	imgCopy=img.copy()
	img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgGrayCopy=img.copy()
	imgBlur = cv2.medianBlur(img, 1, 0)
	otsuReturn, imgThresh = cv2.threshold ( imgBlur, 0, 255, cv2.THRESH_OTSU)
	imgThreshCopy = imgThresh.copy()
	imgMorphed = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, (5, 5))
	edge = cv2.Canny (imgBlur, 100, 255 )
	cv2.imshow("Number Plates detected", edge)
	return edge, imgGrayCopy, imgCopy


def main():

	img = cv2.imread(PATH)
	imgShape = img.shape [:2]
	resizingParameter = imgShape[1] / 1000 if (imgShape[1] > imgShape[0]) else imgShape[0] / 1000
	increment = 0.2

	for counter in xrange(1, 20, 1):

		allContoursWithData = []
		validContoursWithData = []
		PlatesContour = []
		crossingContour = []
		imgResized = cv2.resize(img, ( int(imgShape[1]/resizingParameter), int(imgShape[0]/resizingParameter) ))
		
		# imgBlurred = cv2.GaussianBlur(img, (5,5), 0)
		# cv2.imshow("Blurr",imgBlurred)
		# ret,imgThresh = cv2.threshold(img,100,255,cv2.THRESH_BINARY_INV)     #for detecting car
		# cv2.waitKey(0)
		# # cv2.imshow('imgThresh', imgThresh)
		# imgThreshCopy = imgThresh.copy()
		# # gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
		# # gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
		# # cv2.imshow("sobelx",gx)
		# # cv2.imshow("sobely",gy)
		# npaContours, npaHierarchy = cv2.findContours(imgThresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		
		# # print len (npaContours)
		# for npaContour in npaContours:
		#     contourWithData = ContourWithData()                                             # instantiate a contour with data object
		#     contourWithData.npaContour = npaContour                                         # assign contour to contour with data
		#     contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     # get the bounding rect
		#     contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
		#     contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           # calculate the contour area
		#     allContoursWithData.append(contourWithData)
		# # print allContoursWithData
		# c=0
		# for contourWithData in allContoursWithData: 

		#     [intX,intY,intWidth,intHeight] = contourWithData.boundingRect
		#     # if contourWithData.checkIfContourIsValid():
		#     ratio = float(intWidth)/intHeight
		#     if ( ratio > 2 and ratio < 5 ) :
		#         if contourWithData.checkIfContourIsValid():
		#             # contourWithData=np.array(contourWithData)
		#             print contourWithData.fltArea, ratio
		#             cv2.rectangle(imgCopy,(contourWithData.intRectX, contourWithData.intRectY),(contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),(255, 255, 0),2)
		#             # cv2.drawContours(imgCopy,contourWithData.npaContour,-1,(255,255,0),2)
		#             c+=1
		#             print c
		#             PlatesContour.append(contourWithData)
		# cv2.imshow("Number Plates",imgCopy)
		# cv2.waitKey(0)
		# i=0


		
		edge, imgGrayCopy, imgCopy = preprocessing (imgResized)
		Contour, Hierarchy  = cv2.findContours ( edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

		for npaContour in Contour:

			contourWithData = ContourWithData()                                             # instantiate a contour with data object
			contourWithData.npaContour = npaContour                                         # assign contour to contour with data
			contourWithData.boundingRect = cv2.boundingRect( contourWithData.npaContour )     # get the bounding rect
			contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
			contourWithData.fltArea = cv2.contourArea( contourWithData.npaContour )           # calculate the contour area
			allContoursWithData.append (contourWithData)

		for contourWithData in allContoursWithData: 

			[intX,intY,intWidth,intHeight] = contourWithData.boundingRect

			# if contourWithData.checkIfContourIsValid():
			ratio = float( intWidth ) / intHeight
			mask = np.zeros(imgGrayCopy.shape , np.uint8) 
			# cv2.drawContours(imgGrayCopy, contourWithData.npaContour, 0, 255, -1)
			# pixelpoints = cv2.findNonZero (mask)
			meanVal = cv2.mean (imgCopy)
			if (contourWithData.checkIfContourIsValid() ):
			# if contourWithData.checkIfContourIsValid():
				# contourWithData=np.array(contourWithData)
				print contourWithData.fltArea, ratio, meanVal[:3] 
				# cv2.matchShapes ( contourWithData.npaContour, 'plateTemplate.jpg', 1, 0.0)
				# contourWithData.npaContour, len ( contourWithData.npaContour )
				# for i in xrange (len(contourWithData.npaContour)):
				#     print contourWithData.npaContour[i].
					# M = cv2.moments(contourWithData.npaContour[i])
					# cx1 = int( M['m10'] / M['m00'] )
					# cy1 = int( M['m01'] / M['m00'] )

					# cv2.drawContours(imgCopy,(cx1,cy1),2,(255,0,255),-1)
				cv2.rectangle(imgCopy, (contourWithData.intRectX, contourWithData.intRectY), (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight ),( 255, 255, 0 ),2 )
				crossingContour.append(contourWithData)
			# cv2.drawContours(imgCopy,contourWithData.npaContour,-1,(255,255,0),2)
			# c+=1
			# print c
			

		cv2.imshow("Contours After Edge Detection", imgCopy )

		ch = chr(cv2.waitKey(0) & 255)

		if (ch == 'y'):
			print counter

			i = 0

			for Data in crossingContour:
				i+=1
				contourCharacters=[]
				# cv2.rectangle (img, (Data.intRectX, Data.intRectY), (Data.intRectX + Data.intRectWidth, Data.intRectY + Data.intRectHeight),(0, 255, 0),2)
				imgROI = img[Data.intRectY * resizingParameter : (Data.intRectY + Data.intRectHeight )*resizingParameter, Data.intRectX * resizingParameter : (Data.intRectX + Data.intRectWidth) * resizingParameter]
				# imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
				# npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
				# npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
				# cv2.namedWindow('Detected Contours'+str(i), cv2.WINDOW_NORMAL)
				cv2.imshow('Detected Contours'+str(i), imgROI)
				imgROIGray = cv2.cvtColor (imgROI , cv2.COLOR_BGR2GRAY)
				
				threshPlate = cv2.adaptiveThreshold(imgROIGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,  11, 2)
				contourInNumberPlate, contourHierarchy = cv2.findContours (threshPlate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				
				cv2.waitKey(0)

				for npaContour in contourInNumberPlate:

					contourWithData = ContourWithData()                                             # instantiate a contour with data object
					contourWithData.npaContour = npaContour                                         # assign contour to contour with data
					contourWithData.boundingRect = cv2.boundingRect (contourWithData.npaContour)     # get the bounding rect
					contourWithData.calculateRectTopLeftPointAndWidthAndHeight ()                    # get bounding rect info
					contourWithData.fltArea = cv2.contourArea (contourWithData.npaContour)           # calculate the contour area
					contourCharacters.append (contourWithData)

				for validCharacters in contourCharacters:
					characterRatio = float(validCharacters.intRectWidth) /validCharacters.intRectHeight
					# print validCharacters

					if(validCharacters.fltArea > 10 and validCharacters.fltArea < 100 and characterRatio > 0.25 and characterRatio < 0.75):
						cv2.rectangle(imgROI, (validCharacters.intRectX, validCharacters.intRectY), (validCharacters.intRectX + validCharacters.intRectWidth, validCharacters.intRectY + validCharacters.intRectHeight ), (255,0,125),2)
						# cv2.namedWindow("Characters in Number Plate", cv2.WINDOW_NORMAL)
						cv2.imshow("Characters in Number Plate", imgROI [validCharacters.intRectY : validCharacters.intRectY + validCharacters.intRectHeight , validCharacters.intRectX : validCharacters.intRectX + validCharacters.intRectWidth])
						print characterRatio
						cv2.waitKey(0)

				cv2.waitKey(0)







			break

		resizingParameter += increment
		

		# # x = crossingContour[0].intRectX + 2
		# # y = crossingContour[0].intRectY + 2
		# # X = x + crossingContour[-1]
		# # Y = 
		# # cv2.rectangle(imgCopy,(), (crossingContour[0].intRectX + 2, ((crossingContour[-1].intRectX - crossingContour[0].intRectX) + crossingContour[-1].intWidth + 2, (crossingContour[0].intRectY + 2, ((crossingContour[-1].intRectY - crossingContour[0].intRectY) + crossingContour[-1].intWidth + 2 )
		# # cv2.imshow("Crossings and number plate",imgCopy)
		# cv2.waitKey(0)


main()