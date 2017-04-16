from socket import *
from robot_structure import Robot
from Rendevous import rendezvous
from direction import direction
import sys
import math
from camera_actions import *
import cv2
import time

cap = cv2.VideoCapture(1)

#fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
video_writer = cv2.VideoWriter("output3.avi", -1, 20, (640, 480))

##Create four robots
robot1 = Robot(BLUE)  # Blue
robot2 = Robot(GREEN)  # Green
robot3 = Robot(RED)    # Red
robot4 = Robot(YELLOW) # Yellow

#Current map
# Robot1 F8:F0:05:F1:D6:1C  - .6 - blue
# Robot2 F8:F0:05:F7:FF:F9  - .2 - green
# Robot3 F8:F0:05:F7:FF:F1  - .4 - red
# Robot4 F8:F0:05:F7:FF:F2  - .5 - yellow
#


HOST1 = '192.168.1.6' # blue robot
HOST2 = '192.168.1.2' # green robot
HOST3 = '192.168.1.5' # red robot
HOST4 = '192.168.1.4' # Yellow Robot

PORT = 2390
BUFSIZE = 1024
FLAG = 0

ADDR1 = (HOST1, PORT)   # blue robot
ADDR2 = (HOST2, PORT) # green robot
ADDR3 = (HOST3, PORT) # red robot
ADDR4 = (HOST4, PORT) # Yellow robot

udpSerSock = socket(AF_INET, SOCK_DGRAM)

i = 0
count = 1
MESSAGE1 = "q"
currMESSAGE1 = "q"
MESSAGE2 = "q"
currMESSAGE2 = "q"
MESSAGE3 = "q"
currMESSAGE3 = "q"
MESSAGE4 = "q"
currMESSAGE4 = "q"
fwdcount1 = 1
rotcount1 = 1
fwdcount2 = 1
rotcount2 = 1
rotcount3 = 1
fwdcount3 = 1
rotcount4 = 1
fwdcount4 = 1
a1 = 1
a2 = 1
a3 = 1
a4 = 1

while True:
    ret, bgr_image = cap.read()
    cv2.imshow("cam_image", bgr_image)
    orig_image = bgr_image.copy()
    bgr_image = cv2.medianBlur(bgr_image, 3)
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    robot_in_view =  True
	
    find_robot(hsv_image, orig_image, BLUE, BLUE, BLUE, robot1)
    find_robot(hsv_image, orig_image, GREEN, GREEN, GREEN, robot2)
    find_robot(hsv_image, orig_image, RED, RED, RED, robot3)
    find_robot(hsv_image, orig_image, YELLOW, YELLOW, YELLOW, robot4)
	
    video_writer.write(bgr_image)

    if robot_in_view:

        print "i :%d" % i
		
        if i == 500:
            MESSAGE = 'stop'
            udpSerSock.sendto(MESSAGE, ADDR1)
            udpSerSock.sendto(MESSAGE, ADDR2)
            udpSerSock.sendto(MESSAGE, ADDR3)
            udpSerSock.sendto(MESSAGE, ADDR4)
            cap.release()
            cv2.destroyAllWindows()
            udpSerSock.close()
            video_writer.release()
            exit(0)

        (xpos1, ypos1, angle1) = rendezvous(robot1, robot2, robot2) #blue
        (xpos2, ypos2, angle2) = rendezvous(robot2, robot3, robot3) #green
        (xpos3, ypos3, angle3) = rendezvous(robot3, robot4, robot4) #red
        (xpos4, ypos4, angle4) = rendezvous(robot4, robot3, robot2)  # Yellow

        (MESSAGE1, rotcount1, fwdcount1, a1) = direction(robot1, xpos1, ypos1, angle1, rotcount1, fwdcount1, a1)
        (MESSAGE2, rotcount2, fwdcount2, a2) = direction(robot2, xpos2, ypos2, angle2, rotcount2, fwdcount2, a2)
        (MESSAGE3, rotcount3, fwdcount3, a3) = direction(robot3, xpos3, ypos3, angle3, rotcount3, fwdcount3, a3)
        (MESSAGE4, rotcount4, fwdcount4, a4) = direction(robot4, xpos4, ypos4, angle4, rotcount4, fwdcount4, a4)
		
        print("robot1blue", MESSAGE1, robot1.xpos, robot1.ypos, xpos1, ypos1, robot1.dir, angle1)
        print("robot2green", MESSAGE2, robot2.xpos, robot2.ypos, xpos2, ypos2, robot2.dir, angle2)
        print("robot3red", MESSAGE3, robot3.xpos, robot3.ypos, xpos3, ypos3, robot3.dir, angle3)
        print("robot4Yellow", MESSAGE4, robot4.xpos, robot4.ypos, xpos4, ypos4, robot4.dir, angle4)

        if (MESSAGE1 != currMESSAGE1):
            udpSerSock.sendto(MESSAGE1, ADDR1)
            currMESSAGE1 = MESSAGE1
        if (MESSAGE2 != currMESSAGE2):
            udpSerSock.sendto(MESSAGE2, ADDR2)
            currMESSAGE2 = MESSAGE2
        if (MESSAGE3 != currMESSAGE3):
            udpSerSock.sendto(MESSAGE3, ADDR3)
            currMESSAGE3 = MESSAGE3
        if (MESSAGE4 != currMESSAGE4):
         #   udpSerSock.sendto(MESSAGE4, ADDR4)
            currMESSAGE4 = MESSAGE4

        i = i + 1
    # try:
    # print(data)
    # data, ADDR = udpSerSock.recvfrom(BUFSIZE)
    # except:
    # print "FAIL"
    # data = "FAIL"

    # if data == "ACK0":
    # print "ACK received"
    # print "batterylow"
    # elif data == "ACK1":
    # print "batteryhigh"
    # elif data == "FAIL":
    # print "Robot not connected"
    # else:
    # print "Message not recieved by robot, re-send"

    else:
        print "Robot not in view - stopping robot"
        MESSAGE = "stop"
        udpSerSock.sendto(MESSAGE, ADDR1)
        udpSerSock.sendto(MESSAGE, ADDR2)
        udpSerSock.sendto(MESSAGE, ADDR3)
        udpSerSock.sendto(MESSAGE, ADDR4)


        #print "send message : ", MESSAGE
        #exit(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        # time.sleep(1)

cap.release()
video_writer.release()
cv2.destroyAllWindows()
udpSerSock.close()
