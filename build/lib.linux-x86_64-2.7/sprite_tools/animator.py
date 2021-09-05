#!/usr/bin/env python

""" Creates an image sequence of animation frames from sprites. 

    Description:

    This module is a programmatic approach to creating and modifying frames
    for sprite animations. It is designed to be used along side existing 
    image editing software to more efficiently create animation frames. 

    Traditionally, sprite animations are created using image editing software
    such as GIMP or Paint.NET. Although this software comes with many tools
    and features to modify a single image, the work flow for image editing
    software is not optimized for making and saving incremental changes to an
    image needed for animation. For example, when using GIMP, the user must 
    manually invoke the 'export' command and manually change the name of the
    image file to create a new frame. Additionally, sprites in GIMP must be 
    pasted into their own layers for isolated sprite transformations such as
    translations or rotations. Creating and naming new image files, then 
    creating and naming new layers, then pasting new sprites into layers, then
    navigating to other layers for additional sprite transformations or 
    deletion leads to the user spending the majority of their time on the
    method of creating animation rathe than the design of the animation.

    This module attempts to resolve these issues with the following features:

    Implicit Frame Creation -- Creating new animation frames does not require
    the user to explicitly name and initialize the frame. Saving a frame will
    automatically create a new frame to work on. Additionally, the dimensions
    of the frame will match the dimensions of the previous frame if they have
    the same background.

    Entity-Event Based Sprite Expression -- Related sprites are grouped as a 
    single entity called a FrameElement. Specific sprites can be accessed 
    through a FrameElement based on an event that happens to this entity and
    when the sprite occurs in the event. As an example, a collection of images
    depicting a cat would belong to the FrameElement of 'cat'. This collection
    of images can be subdivided based on what the cat is doing. Images
    depicting the cat while walking would be catagorized under the 'walking'
    event. This grouping system is a more intuitive method of retrieving
    specific sprites than copying and pasting sprites from a sprite sheet 
    through standard image editing software.

    Automated Sprite Animation Looping -- The user does not need to manually
    paste sprites for subsequent cycles of a looping sprite animation.
    Instead, the user defines the number of frames that a looping animation
    should occur in. This is useful for a FrameElement with a 'running' event
    animation.

    Simplified Parametric Motion Execution -- Parametric equations can be made
    within the script and its results can be applied directly to a 
    FrameElement's positional data to create complex motion. The user does not
    need to know the explicit positional information of each sprite to 
    accomplish motion.

    Implementation of Other Basic Sprite Transforms -- Sprites can be 
    translated, rotated, flipped, scaled and given transparency without the 
    need to create and save transformed versions of a sprite through image 
    editing software. Parametric equations can also be used with these 
    transforms for more complex transformations.    

    Required Packages:
    - Python 2.7
    - OpenCV (cv2)
    - numpy

    Additional Requirements/Details:
    - All sprites must be png image files.
    - Sprites related by an event must be stored in an empty directory
        - For example, do not store sprites  for a 'walking' animation with
          sprites for a 'jumping' animation in the same folder. Create  
          seperate folders called 'Walking' and 'Jumping' and store the
          sprites to their respective event folders. It is reccomended to make
          these event folders subdirectories to a FrameElement folder for 
          further organization.
    - Sprites should be in alphanumerical order within their directory 
    - The image sequence is outputed as a collection of png image files.

    Example:
    - Refer to example script in GitHub Examples Folder.  

    TODO:
    - Add back float based scaling for continuous (albeit lossful) scaling. 
    - Create Python3 version of module. 
"""

__version__ = '0.1.01'
__author__ = 'Kimberly McIntyre'

import os

import numpy as np
import cv2

class Frame(object):

    """Processes sprite images and pastes them into a png image sequence. 

       Summary of Class Methods:
       setAlpha -- Converts a sprite image color into an alpha channel.  
       add -- Creates sprite image processing instructions for a frame.
       save -- Saves processing instructions to frame and creates a new frame. 
       render -- Processes frames and outputs to file.

       This object is the canvas that all sprites are pasted to. Sprites 
       are pasted to this canvas using the add method. The sprites can be 
       transformed (rotated, scaled, flipped, etc) before pasting to this
       canvas using the appropiate parameters in the add method. The order 
       in which sprites are added is important as sprites can be layered on
       top of each other.   

       Once this canvas contains sprites, the save method can be used to 
       save the current canvas as a single frame of the animation. The save
       method will also clear the contents of the canvas to work on the next
       frame of the animation. 

       Once all frames of the animation are finished, the render method can 
       be used to export the frames to file as a sequence of png images.      
    """
    
    def __init__(self):
        self.alphaChannel = 0
        self.frameList = []
        self.instrKeys = ['image', 'position', 'alpha', 'rotation', 'scale', 'flip'] 
        self.instr = {key:[] for key in self.instrKeys}

    def setAlpha(channel):
        """ Converts RGB defined color into an alpha channel for all sprites.
        
        Keyword Arguments:
        channel -- An integer defining value of R, G, and B channel of color
                   (i.e. channel = 60 corresponds to RGB color (60,60,60). 
        """
        self.alphaChannel = channel 

    def add(self, frameElem, eventName, imgNum, position, alpha, 
                  rotation, scale, flip=(False, False)):
        """Prepares instructions for processing a FrameElement before it
           is pasted to a Frame.

           Keyword Arguments:
           frameElem -- FrameElement object where sprite images are stored
           eventName -- Dictionary key for FrameElement that accesses the 
                        corresponding image sequence on file.
           imgNum    -- Index of an image in the FrameElement image sequence.
           position  -- Tuple of x and y coordinates of top left corner of 
                        image.
           alpha     -- Float value between 0 and 1 inclusively that defines 
                        the alpha channel of an image.
           rotation  -- Signed Integer value that corresponds to the degrees 
                        of rotation (counter-clockwise) of the image.
           scale     -- Positive integer value that will be multiplied to the
                        dimensions of the image. (scale >= 1).
           flip      -- Tuple of Booleans where the first boolean will flip the
                        image horizontally and the second will flip it 
                        vertically.

           Additional Notes:
           - The first added frameElem will define the size of the frame. 
           - The first added frameElem is at the lowest layer of the frame.         
        """

        self.instr['image'].append(frameElem.eventDict[eventName][imgNum])
        self.instr['position'].append(position)
        self.instr['alpha'].append(alpha)
        self.instr['rotation'].append(rotation)
        self.instr['scale'].append(scale)
        self.instr['flip'].append(flip)

    def save(self,repeatFrames=1):
        """Appends instructions to Frame for processing of all FrameElements.

           Keyword Arguments:
           repeatFrames -- Number of frames with the current set of 
                           instructions that will be added to the animation.  
        """		
        for curFrame in xrange(repeatFrames):			
            self.frameList.append(self.instr)
        self.instr = {key:[] for key in self.instrKeys}

    def render(self, outDir, outPrefix):
        """ Outputs a seqeuence of png images to the specified directory
            using the instructions stored from the save() method

            Keyword Arguments:
            outDir    -- Directory where the image sequence will be saved to.
            outPrefix -- Start of name for each image in the image sequence.
                         This prefix will be followed by the index of the 
                         image in the image sequence.    
        """
        frameIndex = 0
        frameCount = len(self.frameList)
        for curFrame in self.frameList:
            objCount = len(curFrame['image'])
            frameElement = [curFrame['image'][x] for x in range(objCount)]
            frameElement = [self._flipSprite(frameElement[x], curFrame['flip'][x]) for x in range(objCount)]		
            frameElement = [self._scaleSprite(frameElement[x], curFrame['scale'][x]) for x in range(objCount)]
            unPack = [self._rotateSprite(frameElement[x], curFrame['rotation'][x], curFrame['position'][x]) for x in range(objCount)]
            frameElement = [elem[0] for elem in unPack]
            curFrame['position'] = [elem[1] for elem in unPack]
            frameElement = [self._alphaSprite(frameElement[x], curFrame['alpha'][x]) for x in range(objCount)]
            frame = np.ones((frameElement[0].shape), dtype = np.uint8) * 255
            for i in range(objCount):				
                frame = self._layerSprite(frameElement[i], frame, curFrame['position'][i])
            # save/export frame to file
            newFileName = outDir + '/' + outPrefix + ('%.*d' % ((len(str(frameCount))), frameIndex)) + '.png'
            cv2.imwrite(newFileName, frame[:, :, 0:3])
            frameIndex += 1

    def _flipSprite(self, sprite, flipTuple):
        """Flips the sprite image horizontally and/or vertically."""
        spriteFlipped = sprite
        if flipTuple[0]:
            spriteFlipped = np.fliplr(sprite)
        if flipTuple[1]:
            spriteFlipped = np.flipud(sprite)
        return spriteFlipped

    def _scaleSprite(self, sprite, scaleFactor):
        """Scales the sprite image by a positive integer multiplier."""
        newDims = [x * scaleFactor for x in sprite.shape]		
        scaleArray = np.ones((scaleFactor, scaleFactor),dtype = np.uint8)
        spriteScaled = np.zeros((newDims[0], newDims[1],3), dtype = np.uint8)
        spriteScaled[:, :, 0] = np.kron(sprite[:, :, 0], scaleArray)
        spriteScaled[:, :, 1] = np.kron(sprite[:, :, 1], scaleArray)
        spriteScaled[:, :, 2] = np.kron(sprite[:, :, 2], scaleArray)
        return spriteScaled

    def _rotateSprite(self, sprite, rotation, position):
        """Rotates the sprite image 

           Rotation is in degrees where positive values produce a
           counter-clockwise rotation.
        """
        [rowCount, columnCount, BGR] = sprite.shape		
        (cXR, cYR) = (columnCount // 2, rowCount // 2)
        (cXA, cYA) = (position[0] + cXR, position[1] + cYR)
        rotationMatrix = cv2.getRotationMatrix2D((cXR, cYR), rotation, 1)
        cos = np.abs(rotationMatrix[0, 0])
        sin = np.abs(rotationMatrix[0, 1])
        newWidth = int(round((rowCount * sin) + (columnCount * cos)))
        newHeight = int(round((rowCount * cos) + (columnCount * sin)))
        newPos = (cXA - (newWidth // 2) , cYA - (newHeight // 2))
        rotationMatrix[0, 2] += (newWidth / 2) - cXR
        rotationMatrix[1, 2] += (newHeight / 2) - cYR
        spriteRotated = cv2.warpAffine(sprite, rotationMatrix, (newWidth, newHeight))
        return (spriteRotated, newPos)

    def _alphaSprite(self, sprite, alpha):
        """Adds an alpha channel to a sprite image with specified transparency."""
        [rowCount,columnCount,BGR] = sprite.shape
        # Prepare the alpha channel for current sprite
        blackBands = np.where(sprite == self.alphaChannel, 1, 0)
        blackPixels = np.all(blackBands, axis=2)
        blackPixels = np.invert(blackPixels) * int(round(255 * alpha))
        # Add alpha channel to sprite array
        spriteAlpha = np.zeros((rowCount, columnCount, 4), dtype = np.uint8)
        spriteAlpha[:, :, 0] = sprite[:, :, 0]
        spriteAlpha[:, :, 1] = sprite[:, :, 1]
        spriteAlpha[:, :, 2] = sprite[:, :, 2]
        spriteAlpha[:, :, 3] = blackPixels[:, :]
        return spriteAlpha

    def _layerSprite(self, sprite, frame, position):
        """Pastes the sprite image onto the frame at position (x,y)."""		
        # Crop the background and frame element to obtain the intersection				
        [rowCount, columnCount, BGRA] = sprite.shape 				
        cropY1 = position[1]
        cropY2 = (position[1] + rowCount)
        cropX1 = position[0]
        cropX2 = (position[0] + columnCount) 				
        cropSpriteY1 = 0
        cropSpriteY2 = rowCount				
        cropSpriteX1 = 0
        cropSpriteX2 = columnCount				
        if cropY1 < 0:
            cropSpriteY1 = -cropY1
            cropY1 = 0
        if cropX1 < 0:
            cropSpriteX1 = -cropX1
            cropX1 = 0				
        if cropY2 > frame.shape[0]:
            cropSpriteY2 = rowCount - (cropY2 - frame.shape[0])
            cropY2 = frame.shape[0]
        if cropX2 > frame.shape[1]:
            cropSpriteX2 = columnCount - (cropX2 - frame.shape[1])				
            cropX2 = frame.shape[1]				
        frameCropped = frame[cropY1:cropY2, cropX1:cropX2, :]
        spriteCropped = sprite[cropSpriteY1:cropSpriteY2, cropSpriteX1:cropSpriteX2, :]

        # Get the composite alpha channel
        cropHeight = cropSpriteY2 - cropSpriteY1
        cropWidth = cropSpriteX2 - cropSpriteX1				
        one = np.ones((cropHeight, cropWidth))
        spriteCroppedNorm = np.divide(spriteCropped[:, :, 3], 255, \
                                      dtype = float \
                                     )
        frameCroppedNorm = np.divide(frameCropped[:, :, 3], 255, \
                                     dtype = float \
                                    )
        firstElem = np.subtract(one, spriteCroppedNorm)
        secondElem = np.subtract(one, frameCroppedNorm)
        newAlpha = np.subtract(one,np.multiply(firstElem, secondElem))
        newAlpha2 = np.zeros(((cropSpriteY2 - cropSpriteY1), \
                              (cropSpriteX2 - cropSpriteX1), 3 \
                             ), dtype = float \
                            )
        newAlpha2[:, :, 0] = newAlpha[:, :]
        newAlpha2[:, :, 1] = newAlpha[:, :]
        newAlpha2[:, :, 2] = newAlpha[:, :]
        frameElementAlpha = np.zeros((cropHeight, cropWidth, 3), \
                                     dtype = float \
                                    ) 
        frameElementAlpha[:, :, 0] = spriteCroppedNorm
        frameElementAlpha[:, :, 1] = spriteCroppedNorm				
        frameElementAlpha[:, :, 2] = spriteCroppedNorm
        frameCroppedAlpha = np.zeros((cropHeight, cropWidth, 3), \
                                     dtype = float \
                                    )
        frameCroppedAlpha[:, :, 0] = frameCroppedNorm
        frameCroppedAlpha[:, :, 1] = frameCroppedNorm
        frameCroppedAlpha[:, :, 2] = frameCroppedNorm				
        firstElem2 = np.multiply(frameElementAlpha, spriteCropped[:, :, 0:3])
        secondElem2a = np.multiply(frameCroppedAlpha, frameCropped[:, :, 0:3])
        secondElem2b = np.subtract(one, spriteCroppedNorm)
        secondElem2b2 =	np.zeros((cropHeight, cropWidth, 3), \
                                 dtype = float \
                                )
        secondElem2b2[:, :, 0] = secondElem2b[:, :]
        secondElem2b2[:, :, 1] = secondElem2b[:, :]
        secondElem2b2[:, :, 2] = secondElem2b[:, :] 			
        secondElem2 = np.multiply(secondElem2a, secondElem2b2)
        newColor = np.divide(np.add(firstElem2, secondElem2), newAlpha2, dtype = float)
        newColor = newColor.astype(np.uint8)
        newAlpha = np.multiply(newAlpha, 255).astype(np.uint8)
		
        # Get the composite frame element 
        compFrame = np.zeros((cropHeight, cropWidth, 4), dtype = np.uint8)
        compFrame[:, :, 0] = newColor[:, :, 0]
        compFrame[:, :, 1] = newColor[:, :, 1]
        compFrame[:, :, 2] = newColor[:, :, 2]
        compFrame[:, :, 3] = newAlpha[:, :]
		
        # Paste composite frame element into frame
        frame[cropY1:cropY2, cropX1:cropX2, :] = compFrame

        return frame

class FrameElement(object):
    
    """Stores related sprite data to be used with Frame
    
       Summary of Class Methods:
       addNewEvent  -- Stores and Catagorizes image sequences of sprites.
       setCurSprite -- Returns index of image that loops image sequence. 

       A FrameElement is technically a collection of related sprites. These
       sprites are subdivided into groups called events. Before a Frame can be
       saved, the sprite of at least one FrameElement must be added to the 
       Frame by referencing the FrameElement and event that the sprite belongs
       to.  

       Sprites are added to a FrameElement through the addNewEvent method. The
       addNewEvent method gives a name to a collection of sprites that matches
       the event that the sprites convey. 

       The first FrameElement added to the Frame is considered the background.
       the Frame will inherit the width and height of the first FrameElement.
       All subsequent FrameElements pasted to the Frame that exceeds the size 
       of the background will be cropped to fit the dimensions of the Frame.
   
       Paste sprites of FrameElements to the Frame by using the Frame's add
       method. 
    """
    
    def __init__(self): 
        self.eventDict = {}
        self.curSpriteIndex = -1

    def addNewEvent(self, eventName, imageFolderDir):
        """Stores related sprite images into dictionary

        Keyword Arguments:
        eventName      -- String name for collection of related sprite images.
        imageFolderDir -- Folder directory where related sprite images.
                          are located. The folder must only contain related
                          sprite images. The sprite images must be sequenced
                          in alphanumerical order.   
        """		
        inputFileList = os.listdir(imageFolderDir)
        inputFileList.sort()
        inputFileList = [imageFolderDir + '/' + x for x in inputFileList] 
        imgList = [cv2.imread(x) for x in inputFileList]
        self.eventDict[eventName] = imgList

    def setCurSprite(self,eventName, startIndex=0):
        """Defines the current image that will continue a looping animation

           Keyword Arguments:
           eventName  -- String name for collection of related sprite images.
           startIndex -- Index of sprite image in the image sequence. (i.e)
                         the first image in the event folder will have a
                         startIndex of 0. 

           This is useful for sprite animations that need to repeat over a
           frame interval that does not allow the animation to start and 
           end at the same sprite image.
        """
        self.curSpriteIndex = self.curSpriteIndex + startIndex		
        if self.curSpriteIndex < (len(self.eventDict[eventName])-1):
            self.curSpriteIndex += 1
        else:
            self.curSpriteIndex = -1
        return self.curSpriteIndex

