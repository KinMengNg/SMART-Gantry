from datetime import datetime as dt
from datetime import timedelta as td
import cv2

import gantry_simulation

import peekingduck_face_detector

#Initialise the face detection object
face_detector = peekingduck_face_detector.Detect_Face_Pipeline()

# Define a video capture object
# Currently using past videos, replace .mp4 files when live footage is used.
vid_in = cv2.VideoCapture('gantry_in_5fps.mp4') #Where our video stream goes in #The number refers to the input device, if theres more than one need to check which one is the right camera
vid_out = cv2.VideoCapture('gantry_out_5fps.mp4')

is_video_file = True #Change to false when using live feed

# Number of gantries as an integer
total_gantries = 'a' # arbitrary letter
while not total_gantries.isdigit():
    total_gantries = input('How many gantries are there? ')

total_gantries = int(total_gantries)

#Initialise gantry system for demo
gantry_system = gantry_simulation.Gantry_System(total_gantries)

#Intervals between updates
interval_btw_updates = ''
while not interval_btw_updates.isdigit():
    interval_btw_updates = input('What is the interval between gantry updates? [In seconds] ')
interval_btw_updates = int(interval_btw_updates)


#Initialise the first start time
#Start it being back by 180 seconds, by subtracting a timedelta of 180 seconds
#This is so that the first frame will trigger gantry update
start_time = dt.now() - td(seconds=180)

while(True):
    try:
        # Capture the video frame
        # by frame
        ret_in, frame_in = vid_in.read()
        ret_out, frame_out = vid_out.read()


        #######
        #For Video of people walking into MRT
        
        #Get the number of faces detected, and the drawn frame
        people_in, frame_in, no_mask_alert_in = face_detector.get_faces_and_bboxes(frame_in)
        #######


        #######
        #For Video of people walking out of MRT
        
        #Get the number of faces detected, and the drawn frame
        people_out, frame_out, no_mask_alert_out = face_detector.get_faces_and_bboxes(frame_out)
        #######

        # Obtaining live timing
        time_now = dt.now()

        # Obtaining time of the day in 24 hour format
        time_of_day = time_now.strftime('%H'+'%M')
        
        # Make time_of_day valid integer
        if time_of_day[0] == '0':
            time_of_day = time_of_day[1:]
        time_of_day_int = int(time_of_day)

        # Total number of people near gantries
        total_people = people_out + people_in
        gantries_in = 0
        gantries_out = 0

        #Check for time elapsed
        #Only change gantry every 3 minutes
        #To prevent incovenience to commuters
        
        #Get the difference between 2 datetime objects, it will be a time delta object
        time_delta = time_now - start_time
        time_elapsed_seconds = time_delta.seconds

        #IF it is more than 3 minutes, then update gantry, otherwise, dont even bother
        if time_elapsed_seconds >= interval_btw_updates:
            # If no one is near the gantries, half of the gantries will be for open for both going in and out of the MRT
            if total_people == 0:
                gantries_in = round(total_gantries/2)
                gantries_out = total_gantries - gantries_in

            # Controlling of gates during peak hours(8 am to 10 am and 6 pm and 8 pm) and when there are a lot of people
            elif (800 <= time_of_day_int <= 1000) or (1800 <= time_of_day_int <= 2000) or total_people >= 30:
                min_gantry_ratio = 0.2 #In reality, the number should be slightly larger (0.3-0.5), smaller number for demo for more exageratted changes
                min_gantry_open = round(min_gantry_ratio * total_gantries)

                if ((people_out/total_people) < min_gantry_ratio):
                    gantries_out = min_gantry_open
                    gantries_in = total_gantries - min_gantry_open

                elif ((people_in/total_people) < min_gantry_ratio):
                    gantries_in = min_gantry_open
                    gantries_out = total_gantries - min_gantry_open

                else:
                    gantries_in = round((people_in/total_people) * total_gantries)
                    gantries_out = total_gantries - gantries_in

            
            # Controlling of gates during non-peak hours/less crowded timings
            else:
                min_gantry_ratio = 0.3 #In reality, the number should be slightly larger (0.4-0.6), smaller number for demo for more exageratted changes
                min_gantry_open = round(min_gantry_ratio * total_gantries)

                if ((people_out/total_people) < min_gantry_ratio):
                    gantries_out = min_gantry_open
                    gantries_in = total_gantries - min_gantry_open

                elif ((people_in/total_people) < min_gantry_ratio):
                    gantries_in = min_gantry_open
                    gantries_out = total_gantries - min_gantry_open

                else:
                    gantries_in = round((people_in/total_people) * total_gantries)
                    gantries_out = total_gantries - gantries_in

            # Display desired output on terminal
            print(f'Number of gantries for people going out: {gantries_out}')
            print(f'Number of gantries for people going in: {gantries_in}')

            gantry_system.update_gantries(gantries_in, gantries_out)

            #Reset start time to be now
            start_time = dt.now()

        #SUBSYSTEM TO DETECT AND ALERT WHEN NO MASK DETECTED
        if no_mask_alert_in == True:
            print("ALERT: One or more commuter not wearing a mask is entering the station!")
        if no_mask_alert_out == True:
            print("ALERT: One or more commuter not wearing a mask is exiting the station!")
        

        # Display the resulting frame
        cv2.imshow('Frame_in', frame_in)
        cv2.imshow('Frame_out', frame_out)
        
        # the 'q' button is set as the quitting button you may use any desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        if is_video_file:
            print("End of video file")
            break # Because in the demo it is a video, need to break when reach the end of video file


  
# After the loop release the cap object
vid_in.release()
vid_out.release()

# Destroy all the windows
cv2.destroyAllWindows()