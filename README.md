# SMART-Gantry

Short for *System for Monitoring and Automated Regulation of Transit - Gantry*.
Using AI Singapore's PeekingDuck computer vision library, the goal of this project is to automate the conversion of gantry entry and exit points based on the number of commuters entering and exiting a train station.

This is just a proof of concept demo, it is not connected to any MRT stations yet as of now. 

## Context
The context is Singapore's MRT Stations, but it is applicable to any train station with CCTVs.

## Method
1. Retrieve live video feed from the numerous CCTVs in Singapore's MRT station.
2. Detect for faces, and quantify the number of people approaching the entry and exit gantry.
3. The number of entry and exit gantries will update automatically depending on the number of people by finding a ratio.

## Installation
(Tested and working in a Python 3.9 miniconda3 environment on Windows 10 and Windows 11)
1. pip install peekingduck
2. git clone this repo
3. run main.py


