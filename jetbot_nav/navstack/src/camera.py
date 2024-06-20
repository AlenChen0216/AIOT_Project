#!/usr/bin/env python3


#publish : image
#subscribe : get_item
#get_item : when remote server infer that the image is some item, it will publish "get ID" msgs.
#when receive "get ID", print "get ID" and wait for 5 sec.

import torch
import cv2
from jetbot import Camera
import rospy
from std_msgs.msg import String
import pandas as pd
import time
flag = False
result = 0


#model = torch.hub.load('./yolov5-python3.6.9-jetson','custom','./yolov5-python3.6.9-jetson/best.pt',source="local")
#model.cuda()
#model.conf=0.6
camera = Camera.instance(width=224, height=224)

def call(data):
	#Yolo detect
    global flag,result,model,camera
    rospy.loginfo(data.data)
    detail = data.data.split(' ')
    name = detail[1]
    stats = detail[0]
    result += 1
    if stats == '1':  # 1-> success, 0-> fail
        temp = ''
        detected = False
        while not detected:
            img = camera.value
            results = model(img,size=224)
            df = results.pandas().xyxy[0]
            detects = df.values.tolist()
            for detect in detects:
                if detect[6] == name:
                    rospy.loginfo('item detected')
                    detected = True
                    
    elif stats == '2':
        result = 0
    time.sleep(5)
    flag = True

def talker():
	global flag,result
	pub = rospy.Publisher(f'/J1/next_action',String,queue_size=10)
	sub = rospy.Subscriber(f'/J1/arrive',String,call)
	rospy.init_node('camera')
	rate = rospy.Rate(5)
	while not rospy.is_shutdown():
		if flag:
			s = 'J1 '+str(result) #J1 finish result-1 , and willing to get result's item
			rospy.loginfo(s)
			pub.publish(s)
			flag = False
		rate.sleep()
        
camera.stop()
if __name__=='__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass