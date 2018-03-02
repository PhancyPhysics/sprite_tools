#!/usr/bin/env python

import numpy as np
import cv2
import os
import re
from scipy import ndimage

class Extractor(object):
	def getSprite(self,inputFolderName,inputFilePrefix):
		"""Store a list of cv2 numpy image arrays for the image sequences at the given folder and file name 
		
		Keyword Arguments:
		inputFolderName -- relative directory where sprite image sequence is located
		inputFilePrefix -- beginning of name of sprite image file (assumes file name is of pattern FILENAME_000.png)
		"""		
		inputFiles = []
		inputFilePattern = inputFilePrefix +'\d{1,3}.png'
		sprites = []
		for curFile in os.listdir(inputFolderName):
			if re.match(inputFilePattern,curFile):
				inputFiles.append(curFile)
		inputFiles = sorted(inputFiles)
		for curFile in inputFiles:
			imageDir = inputFolderName +'/'+ curFile
			sprites.append(cv2.imread(imageDir))
		return sprites

	def cropSprite(self,sprites,cropX,cropY,cropWidth,cropHeight):
		"""Crops a list of cv2 numpy image arrays and returns the cropped image arrays 
		
		Keywords Arguments:
		sprites	-- list of cv2 numpy image arrays corresponding to sprite image seqeunce
		cropX -- X coordinate (in pixels) of top left corner of crop bounding box
		cropY -- Y coordinate (in pixels) of top left corner of crop bounding box
		cropWidth -- horizontal length (in pixels) of crop bounding box
		cropHeight -- vertical length (in pixels) of crop bounding box   
		"""
		if len(sprites) > 0:
			sprites  = [x[(cropY):(cropY+cropHeight),cropX:(cropX+cropWidth),:] for x in sprites]
			return sprites
		else:
			print('Error in cropSprite Method: No sprites found')	
			return

	def getRelPos(self,cropX,cropY,spriteX,spriteY):
		"""Returns the relative coordinates of the pixel corresponding to the top left corner of a sprite pixel 
		
		Keywords Arguments:
		cropX -- X coordinate (in pixels) of top left corner of crop bounding box
		cropY -- Y coordinate (in pixels) of top left corner of crop bounding box
		spriteX -- X coordinate (in pixels) of top left corner of sprite pixel
		spriteY -- Y coordinate (in pixels) of top left corner of sprite pixel 
		"""
		newX = spriteX - cropX
		newY = spriteY - cropY
		return (newX,newY)	

	def cleanSprite(self,sprites,pixelRef,spritePixelSize):
		"""Returns a list of cv2 numpy image arrays that corresponds to the colors and dimensions of the original uncompressed sprite
		
		Keyword Arguments:
		sprites -- list of cv2 numpy image arrays corresponding to image sequence
		pixelRef -- tuple of coordinates of top left corner of sprite pixel relative to the top left corner of the cropped image
		spritePixelSize -- length of sides (in pixels) of the sprite pixel in relation to the video pixels (i.e. input 3 if one sprite pixel corresonds to a 3 by 3 square of video pixels) 
		"""
		spritesCleaned = []
		for curSprite in sprites:		
			# Use the coordinate of the top left corner of the sprite pixel and check if the distance between the edges of the image and the pixel are divisible by the desired pixel size. Delete the rows and columns equal to the remainder associated with each edge.
			[rowCount,columnCount,BGR] = curSprite.shape
			cut = []
			cut.append(columnCount - pixelRef[0]) # right edge length
			cut.append(pixelRef[1]) # Top edge length
			cut.append(pixelRef[0]) # Left edge length	
			cut.append(rowCount - pixelRef[1]) # bottom edge length
			cut = [x % spritePixelSize for x in cut] # gives number of rows or columns that need to be removed from each edge
			newHeight = rowCount - (cut[1] + cut[3])
			newWidth = columnCount - (cut[0] + cut[2])
			spriteCropped = curSprite[cut[1]:newHeight-cut[1],cut[2]:newWidth-cut[0],:] # sprite[height,width,bgr]

			# Create the cleaned sprite by averaging the BGR values of each pixel contained within 
			newHeight = newHeight / spritePixelSize
			newWidth = newWidth / spritePixelSize
			curSpriteCleaned = np.zeros((newHeight,newWidth,3), dtype=np.uint8)
			for x in range(newWidth):
				for y in range(newHeight):
					testPixel = spriteCropped[(spritePixelSize*y):(spritePixelSize*(y+1)),(spritePixelSize*x):(spritePixelSize*(x+1))]
					pixelMean = np.mean(testPixel,axis=0)
					pixelMean2 = np.mean(pixelMean,axis=0)
					newPixelMean = pixelMean2.astype(int)
					curSpriteCleaned[y,x] = newPixelMean
			spritesCleaned.append(curSpriteCleaned)
		return spritesCleaned

	def isolateSprite(self,sprites, background, limit, areaToggle = False):
		"""Attempts to return a cv2 numpy image array corresponding to the image sequence with the background removed
		
		Keyword Arguments:
		sprites -- list of cv2 numpy image arrays corresponding to image sequence
		background -- background image to be removed from the image seqeunce
		limit -- a nonnegative integer cleaning multiplier for finding background pixels
		areaToggle -- Used to toggle which collection of pixels to remove from the image sequence. 
		"""
		spritesIsolated = []
		upperLimit = np.add(background,limit)
		lowerLimit = np.subtract(background,limit)
		for curSprite in sprites:
			# Find all pixels that have bgr values outside of the limit range
			comCheck = np.logical_and((curSprite <= upperLimit),(curSprite >= lowerLimit))
			comCheck = np.invert(comCheck) 
			n = np.any(comCheck, axis=2)

			# Create a black and white image array where white pixels represent found sprite pixels
			(Xn,Yn) = n.shape
			n2 = np.zeros((Xn,Yn,3), dtype=np.uint8)
			n2[:,:,0] = n[:,:]
			n2[:,:,1] = n[:,:]
			n2[:,:,2] = n[:,:]
			n2 = n2 * 255

			# erode and dialate the image to reduce noise in the image
			kernel = np.ones((5,5),np.uint8)
			n2 = cv2.dilate(n2,kernel,iterations = 1)	
			n2 = cv2.erode(n2,kernel,iterations = 1)	
			n2 = cv2.dilate(n2,kernel,iterations = 1)

			# Find sprite area by locating the first or second largest region of clustered pixels
			n3 = np.zeros((Xn,Yn), dtype=np.uint8)
			n3[:,:] = n2[:,:,0]
			labelArray, numFeatures = ndimage.label(n3)
			uniqueLabel, labelCount = np.unique(labelArray, return_counts=True)
			backgroundIndex = np.argmax(labelCount)
			if areaToggle == True:
				uniqueLabel = np.delete(uniqueLabel, backgroundIndex)
				labelCount = np.delete(labelCount, backgroundIndex)
			spriteAreaIndex = np.argmax(labelCount)

			# Use the sprite area to mask all non sprite related pixels to isolate the sprite against a black background
			spriteAreaMask = np.zeros((Xn,Yn), dtype=np.uint8)
			spriteAreaMask[:][:] = uniqueLabel[spriteAreaIndex]
			spriteMasked = np.equal(labelArray,spriteAreaMask)
			spriteComposite = np.zeros((Xn,Yn,3), dtype=np.uint8)
			spriteComposite[:,:,0] = spriteMasked[:,:]
			spriteComposite[:,:,1] = spriteMasked[:,:]
			spriteComposite[:,:,2] = spriteMasked[:,:]
			spriteIsolated = np.multiply(curSprite,spriteComposite)
			spritesIsolated.append(spriteIsolated)
			
		return spritesIsolated

	def saveSprite(self,sprites,outputFolderName,outputFilePrefix):
		""" Outputs the image sequence to file 
		
		Keyword Arguments:
		sprites -- list of cv2 numpy image arrays corresponding to image sequence
		outputFolderName -- relative directory where sprite image sequence will be saved to
		outputFilePrefix --beginning of name of sprite image file (assumes file name is of pattern FILENAME_000.png)
		"""
		if len(sprites) > 0:
			if not os.path.exists(outputFolderName):
    				os.makedirs(outputFolderName)
			for i in range(len(sprites)):
				newFileName = outputFolderName + '/' + outputFilePrefix + ('%.*d' % ((len(str(len(sprites)))),i)) + '.png'
				cv2.imwrite(newFileName, sprites[i])
		else:
			print('Error in saveSprite Method: No sprites found')
