# SMART-Gantry

![demo_compressed](https://user-images.githubusercontent.com/85046928/216934870-4bd28f7c-9e69-41f9-bdf2-b48585137369.gif)

Short for *System for Monitoring and Automated Regulation of Transit - Gantry*.
Using AI Singapore's PeekingDuck computer vision library, the goal of this project is to automate the conversion of gantry entry and exit points based on the number of commuters entering and exiting a train station.

This is just a proof of concept demo, it is not connected to any MRT stations yet as of now. 

## Context
The context is Singapore's MRT Stations, but it is applicable to any train station with CCTVs.

## Method
1. Retrieve live video feed from the numerous CCTVs in Singapore's MRT station. (For the demo, we recorded our helpful classmates to simulate entering and exiting a gantry)
2. Detect for faces, and quantify the number of people approaching the entry and exit gantry.
3. The number of suitable entry and exit gantries will be calculated through the program by using condition based ratio.
4. The gantry ratio output is feeded to the gantries to be updated. (For the demo, it is feeded to the gantry objects from the gantry_simulation.py)
5. As a side function (for now), our program also gives an alert when a commuter is detected not wearing a mask. (A requirement when using Singapore public transport at the time of writing).

## Installation and Usage
(Tested and working in a Python 3.9 miniconda3 environment on Windows 10 and Windows 11)
1. pip install peekingduck (If installation fails, please refer to here for detailed installation instructions https://peekingduck.readthedocs.io/en/stable/getting_started/index.html)
2. git clone this repo
3. run main.py

## Note
If you want to move/resize the Turtle window, do it BEFORE the program starts the video inference loop. (ie. Do it before you enter the desired number of gantries).
This is a Turtle limitation, not with our program. It will crash the program as it cannot handle external interactions while active in a loop.
