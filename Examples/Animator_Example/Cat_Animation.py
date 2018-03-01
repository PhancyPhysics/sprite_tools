#!/usr/bin/env python

import sys, os

sys.path.append((os.path.abspath(os.path.join('..', '..'))))

from Animator import Frame, FrameElement

# The purpose of this script is to demonstrate the functionality of the
# animator module by walking through the creation of the Cat_Animation
# movie. 

# Define the prefix of the name of the output images and set the directory
#  where these animation frames will be saved to.
outPrefix = 'Frame_'
outDir = './Cat_Animation_Frames'

# Initialize all Frame Elements before creating the frame

# Initialize Background
background = FrameElement()
background.addNewEvent('exist', './Sprites/Background/Scene_1')

# Initialize Bowl
bowl = FrameElement()
bowl.addNewEvent('exist', './Sprites/Bowl/Exist')

# Initialize Exclamation Point
exclamPoint = FrameElement()
exclamPoint.addNewEvent('exist', './Sprites/Exclamation_Point/')

# Initialize Cat
cat = FrameElement()
cat.addNewEvent('sitting', './Sprites/Cat/Sitting')
cat.addNewEvent('standing', './Sprites/Cat/Standing')
cat.addNewEvent('walking', './Sprites/Cat/Walking')

# Initialize Frame
frame = Frame()

# The code is broken up into sections to highlight specific features of the
# animator module and how to use them.

# A. This section demonstrates how to add frame elements into the frame and
#    then save the frame. The add method follows this format:
#    
#    frame.add(frameElement, eventName, imageNum, position, alpha, rotation,
#              scale, flip=(false,false))
#
#   In this method, frameElement is the variable name of a FrameElement 
#   object, eventName is a user defined event associated with the
#   frameElement, imageNum is the index of the sprite image that is stored
#   in an event that will pasted to the frame, position is a tuple of the 
#   x and y coordinates of the top left corner of the sprite image, alpha is
#   is a float between 0 and 1 that sets the sprite's transparency, rotation
#   is the counter-clockwise rotation applied to the sprite image in degrees,
#   scale is a integer value greater than or equal to 1 that will define the
#   scale of the sprite image pasted to the frame compared to the image on 
#   file, and flip is a tuple of booleans where the first boolean flips the
#   image horizontally and the second boolean flips the image vertically.   

#   For loops are used to generate multiple identical frames. A frame rate of 
#   60 is used in this animation so increments of 60 and 30 are used throughout
#   the code for the range of the for loop.

#   The following code causes the cat to sit near the left side of the frame
#   for half a second. 
 
for f in xrange(30):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'sitting', 0, (52, 476), 1, 0, 10)
    frame.save(1)

# B. This section demonstrates how to implement parametric equations to create
#    sprite motion. The following code causes the bowl frame element to slide
#    into frame from the right and come to a stop within a one second duration.
#    This movie will have a frame rate of 60 frames per second,   

# B. Setup bowl motion
bowlStartX = 1920
bowlEndX = 1200
bowlVi = -24
bowlAcc = -bowlVi / 60.0
bowlPosX = [int(round((0.5 * bowlAcc * (f ** 2)) + (bowlVi * f) + bowlStartX)) \
           for f in range(60)]

# B. Bowl slides into frame
for f in xrange(60):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'sitting', 0, (52, 476), 1, 0, 10)
    frame.add(bowl, 'exist', 0, (bowlPosX[f], 836), 1, 0, 10)
    frame.save(1)

# C. This section demonstrates how to implement a Frame Element's
#    setCurSprite method to loop through all sprite images associated with an
#    event for an arbitrary amount of loops. The following code will have the
#    cat cycle through its sitting animation for roughly half a second. This 
#    will allow the sitting animation to loop four times which will emphasize
#    the cat's excitement at seeing the bowl.
#
#    This section also shows how the frame's save method can be used to
#    generate multiple identical frames instead of using the frame generating
#    for loop. This is done to extend the duration in which each sprite image
#    of the cat sitting animation is shown for in the animation.  
  
# C. The cat becomes excited
for f in xrange(32):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'sitting', cat.setCurSprite('sitting', 0), (52, 476), 1, \
              0, 10 \
             )
    frame.add(bowl, 'exist', 0, (bowlEndX, 836), 1, 0, 10)
    frame.save(4)

# D. This section demonstrates that a Frame Element's event dictionary can be
#    used in the frame generating for loop to restrict how many times an 
#    event animation will loop for. In the following code, all frames of the
#    cat's standing animation are shown precisely one time. 
#
#    This section also demonstrates that a Frame Element can be positioned 
#    outside the boundaries of the frame. Since the standing event sprite
#    images are differently sized from the sitting sprite images, the standing
#    sprite images x-coordinate was given a negative value to best match the
#    cat's previous position.     

# D. The cat stands up
for f in xrange(len(cat.eventDict['standing'])):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'standing', f, (-7, 476), 1, 0, 10)
    frame.add(bowl, 'exist', 0, (bowlEndX, 836), 1, 0, 10)
    frame.save(4)

# E. This section implements all of the previously mentioned features to allow
#    the cat to walk towards the bowl. 

# E. Setup walking cycle
walkFrames = len(cat.eventDict['walking']) * 4 
walkStartX = -6
walkEndX = 485
walkEndY = 476
walkLength = walkEndY - walkStartX
walkStepX = [int(round(((walkLength/walkFrames) * i) + walkStartX)) for i in xrange(walkFrames+1)]

# E. The cat walks to the bowl for four cycles
for f in xrange(len(walkStepX)):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(bowl, 'exist', 0, (bowlEndX,836), 1, 0, 10)
    frame.add(cat, 'walking', (f % 2), (walkStepX[f], 476), 1, 0, 10)
    frame.save(8)

# F. This section of the code demonstrates how parametric equations can be
#    applied to the alpha and rotation parameters of a sprite. The following
#    code will cause the bowl to rotate 360 degrees and dissappear within one
#    second.

# F. Setup the bowl to rotate one full rotation within one second
angAcc = 0.2 
rotation = [int(round(0.5 * angAcc * (f ** 2))) for f in range(61)]

# F. Setup the bowl to become completely transparency within one a second
alphaAcc = -0.0005
alpha = [round((0.5 * alphaAcc * (f ** 2)) + 1, 3) for f in range(61)]

# F. The Bowl dissappears as the cat continues to walk towards the bowl for one more cycle
for i in xrange(3):
    for f in xrange(8):
        frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
        frame.add(bowl, 'exist', 0, (bowlEndX,836), alpha[(i*8)+f], \
                  rotation[(i*8)+f], 10 \
                 )
        frame.add(cat, 'walking', ((i + 1) % 2), \
                  (int(round(((i + 1) * walkLength)/walkFrames) + walkEndX), \
                  476), 1, 0, 10 \
                 )
        frame.save(1)

for f in xrange(6):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(bowl, 'exist', 0, (bowlEndX,836), alpha[24+f], \
              rotation[24+f], 10 \
             )
    frame.add(cat, 'walking', 0, \
              (int(round((4*walkLength)/walkFrames) + walkEndX), 476), \
               1, 0, 10 \
              )
    frame.save(1)

for f in xrange(30):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(bowl, 'exist', 0, (bowlEndX,836), alpha[30+f], \
              rotation[30+f], 10 \
             )
    frame.add(cat, 'standing', 3, \
              (int(round((4*walkLength)/walkFrames) + walkEndX), 476), \
              1, 0, 10 \
             )
    frame.save(1)

# G. This section of the code demonstrates how the flip parameter can be 
#    invoked to flip a sprite. Because the flip parameter has a default
#    value of (false,false) it does not need to be included with the other
#    method arguments if flipping a sprite is unneccessary. The flip
#    parameter is used here to make the cat turn around in confusion over
#    the disappearance of the bowl. 

# G. The cat stand in bewilderment for half a second, turns around for a 
#    second, then back around
for f in xrange(30):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'standing', 3, (726, 476), 1, 0, 10)
    frame.save(1)

for f in xrange(30):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'standing', 3, (726, 476), 1, 0, 10, (1,0))
    frame.save(1)

for f in xrange(30):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'standing', 3, (726, 476), 1, 0, 10)
    frame.save(1)

# H. This section demonstrates how to reverse the order in which an event
#    animation is shown. The following code will have the cat sit back 
#    down after accepting that the bowl has dissappeared.

# H. The cat sits back down
for f in xrange(len(cat.eventDict['standing']) - 1, 0, -1):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'standing', f, (726, 476), 1, 0, 10)
    frame.save(4)

# I. This section does not demonstrate any new features but is used to finish
#    the remainder of the animation. The following code will have the cat sit 
#    for roughly a second while it slaps it tail against the ground in mild 
#    frustration over the missing bowl.

# I. The cat continues to sit for half a second but the sitting animation 
#    idles on the first frame
for f in xrange(30):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'sitting', 0, (786, 476), 1, 0, 10)
    frame.save(4)

# I. The cat continues to sit for 2 cycles 
for f in xrange(2*len(cat.eventDict['sitting'])):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'sitting', cat.setCurSprite('sitting', 0), (786, 476), \
              1, 0, 10)
    frame.save(4)

# I. The cat continues to sit for half a second and the animation ends
for f in xrange(30):
    frame.add(background, 'exist', 0, (0, 0), 1, 0, 1)
    frame.add(cat, 'sitting', 0, (786, 476), 1, 0, 10)
    frame.save(4)

# J. This final line of code is used to render the frames that the code above
#    has created

# Save the frames
frame.render(outDir,outPrefix)
