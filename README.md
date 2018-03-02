# sprite_tools

## Synopsis

A Python package used to extract, create, and animate sprites.

## Description

### Animator Module

This module is a programmatic approach to creating and modifying frames for sprite animations. It is designed to be used along side existing image editing software to more efficiently create animation frames. Traditionally, sprite animations are created using image editing software such as GIMP or Paint.NET. Although this software comes with many tools and features to modify a single image, the workflow for image editing software is not optimized for making and saving incremental changes to an image needed for animation. For example, when using GIMP, the user must manually invoke the 'export' command and manually change the name of the image file to create a new frame. Additionally, sprites in GIMP must be pasted into their own layers for isolated sprite transformations such as translations or rotations. Creating and naming new image files, then creating and naming new layers, then pasting new sprites into layers, then navigating to other layers for additional sprite transformations or deletion leads to the user spending the majority of their time on the method of creating animation rather than the design of the animation. This module attempts to resolve these issues with the following features: 

* __Implicit Frame Creation__ -- Creating new animation frames does not require the user to explicitly name and initialize the frame. Saving a frame will automatically create a new frame to work on. Additionally, the dimensions of the frame will match the dimensions of the previous frame if they have the same background.

* __Entity-Event Based Sprite Expression__ -- Related sprites are grouped as a single entity called a FrameElement. Specific sprites can be accessed  through a FrameElement based on an event that happens to this entity and when the sprite occurs in the event. As an example, a collection of images depicting a cat would belong to the FrameElement of 'cat'. This collection of images can be subdivided based on what the cat is doing. Images depicting the cat while walking would be categorized under the 'walking' event. This grouping system is a more intuitive method of retrieving specific sprites than copying and pasting sprites from a sprite sheet through standard image editing software.

* __Automated Sprite Animation Looping__ -- The user does not need to manually paste sprites for subsequent cycles of a looping sprite animation. Instead, the user defines the number of frames that a looping animation should occur in. This is useful for a FrameElement with a 'running' event
animation.

* __Simplified Parametric Motion Execution__ -- Parametric equations can be made within the script and its results can be applied directly to a FrameElement's positional data to create complex motion. The user does not need to know the explicit positional information of each sprite to accomplish motion.

* __Implementation of Other Basic Sprite Transforms__ -- Sprites can be translated, rotated, flipped, scaled and given transparency without the  need to create and save transformed versions of a sprite through image editing software. Parametric equations can also be used with these transforms for more complex transformations. 

### Extractor Module

(Extractor Module description to be added)

## Getting Started

### Prerequisites

* Python Version: 2.7

* Module Dependencies: NumPy, cv2, SciPy, os, re

### Installing

If the package is cloned from the Git repository or downloaded and extracted
from GitHub, Use the terminal to navigate to the directory where the
sprite_tools folder was saved to. Give the setup.py script permission to 
execute and then install the sprite\_tools package to Python using the 
following terminal command: (to be implemented)      

```
python setup.py install
```
  
Running the setup.py script is not necessary to execute the example Cat_Animation.py script. 

The package can also be installed through the Python Package Index using the
following terminal command: (to be implemented)

```
pip install sprite_tools
```

## Testing sprite_tools Package

### Testing Animator Module

The animator module can be tested by running the Cat_Animation.py script. After using the terminal to navigate to the Cat_Animation script and giving the script execution permissions, run the following terminal command:

```
./cat_animation.py
```

Note that this script will generate roughly 760 png images in the 'Cat_Animation_Frames' folder. This should amount to roughly 30 Mb with an execution time of roughly 10 minutes depending on the computer. 

This script implements all user accessible animator methods to generate the png images stored in the Cat_Animation_Frames folder. A detailed explanation on how to use the features of the animator module can be viewed within the comments of the Cat_Animation script. Additional details on method arguments and uses are found within the docstrings of the Animator module. 

### Testing Extractor Module

(Extractor Module test to be implemented)

## Deployment

### How to Use Animator Module Outputs

The Animator module produces a png image sequence. It is recommended to use ffmpeg to use the image sequence to generate the movie file for best results. However other options are available such as Blender’s video editor or imagemagick's convert command for gif creation. Here is an example terminal command used to generate the movie file for the cat animation using the image sequence. 

```
ffmpeg -r 60 -f image2 -s 1920x1080 -i Frame_%03d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p Cat_Animation.mp4
```

### How to Use Extractor Module Outputs

The extractor module is a loosely connected set of methods used to extract sprites from image files to generate assets for an animation. As a consequence of this, not all methods will need to be called to obtain sprites ready for use. Sprites created by the extractor module can be used by by the animator module methods given the correct directories. 

## Authors

* **Kenneth McIntyre** - *Initial work* - [PhancyPhysics](https://github.com/PhancyPhysics)

See also the list of contributors (to be added) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/PhancyPhysics/sprite_tools/blob/master/LICENSE) file for details

## Acknowledgements

* [FuryForged](https://youtu.be/s3S-qbnq3F0) for inspiring the creation of this package through his Iconoclasts Let’s Play series (Linked video contains intro animation using the sprite_tool package). 
* [Joakim Sandberg](http://www.konjak.org) for producing Iconoclasts with its beautiful sprite work.
* [Peter Bone](https://www.youtube.com/user/peterboneg)  for introducing me to sprite animations through the implementation of sprites in version 3-Beta of [Pivot Animator](http://pivotanimator.net). 
* Billie Thompson - [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) for the readme.md template.


