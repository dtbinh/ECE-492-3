from socket import *
from robot_structure import Robot
from Rendevous import rendezvous
import sys
import math
import camera_actions as ca
import cv2
import time

cap = cv2.VideoCapture(0)


##Create four robots
robot1 = Robot(3) #Blue
robot2 = Robot(2) #Green
robot3 = Robot(2)

#robot2.setPos(40,40,0)
#robot3.setPos(40,40,0)

HOST = '192.168.1.3'
PORT = 2390
BUFSIZE = 1024
FLAG = 0

ADDR = (HOST, PORT)

udpSerSock = socket(AF_INET, SOCK_DGRAM)

##angle1 = -90
##xpos1 = -10
i = 0
count = 1
MESSAGE = "q"
currMESSAGE = "q"
while True:
    ret, bgr_image = cap.read()
    cv2.imshow("cam_image", bgr_image)
    orig_image = bgr_image.copy()
    bgr_image = cv2.medianBlur(bgr_image, 3)
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    hue_image = ca.ID_hue_image(hsv_image, robot1.ID, orig_image)
    hue_image2 = ca.ID_hue_image(hsv_image, robot2.ID, orig_image)
    ca.acquire_locations(hue_image, robot1)
    ca.acquire_locations(hue_image2, robot2)
    robot3.setPos(robot2.xpos, robot2.ypos, robot2.dir)
	
    print(i)
    print "Robot 1 x:%d y:%d dir:%d" % (robot1.xpos, robot1.ypos, robot1.dir)
    print "Robot 2 and 3 x:%d y:%d" % (robot2.xpos, robot2.ypos)
	
    (xpos1, ypos1, angle1) = rendezvous(robot1, robot2, robot3)
    if i == 1000 :
        MESSAGE = 'stop'
        udpSerSock.sendto(MESSAGE, ADDR)
        cap.release()
        cv2.destroyAllWindows()
        udpSerSock.close()
        exit(0)

		 
    lower_range = angle1 - 10
    upper_range = angle1 + 10

    xpos_lower_range = xpos1 - 2
    xpos_upper_range = xpos1 + 2
    print "angle 1: %d" % angle1
    print "xpos1 : %d " % xpos1
    if (robot1.dir < lower_range or robot1.dir > upper_range) and (count == 1):  ## rotate untill rotate is good
        if rotcount == 1:
		a = (robot1.dir - angle1 + 360 ) % 360
		b = (angle1 - robot1.dir + 360 ) % 360
		if a > b:
			MESSAGE = 'a'
		else:
			MESSAGE = 'A'
		rotcount = 2
        
        print "Robot 1: x:%d y:%d dir:%d " % (robot1.xpos, robot1.ypos, robot1.dir)
    elif robot1.xpos < xpos_lower_range or robot1.xpos > xpos_upper_range: ## Move untill xpos is good
        if fwdcount == 1:
	        MESSAGE = 's'
	        fwdcount = fwdcount + 1
        else:
	        MESSAGE = 'f'
    else:
        MESSAGE = 'stop'
        (xpos1, ypos1, angle1) = rendezvous(robot1, robot2, robot3)
        fwdcount = 1
	rotcount = 1

    ##MESSAGE = raw_input('>')
    #print "send message: ", MESSAGE
    #i = i + 1

   # print(currMESSAGE)
    #print(MESSAGE)
    if MESSAGE != currMESSAGE:
        udpSerSock.sendto(MESSAGE, ADDR)
        print "send message: ", MESSAGE
        currMESSAGE = MESSAGE
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
		
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
	
	#time.sleep(1)

cap.release()
cv2.destroyAllWindows()
udpSerSock.close()

