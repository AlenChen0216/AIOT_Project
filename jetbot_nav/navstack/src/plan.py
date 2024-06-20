#!/usr/bin/env python
import rospy
import math

#program for navigating car to determined position
# From :  https://github.com/HotBlackRobotics/hotblackrobotics.github.io/blob/master/en/blog/_posts/2018-01-29-seq-goals-py.md
import actionlib
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler
import argparse
import sys
class MoveBaseSeq():
    def call(self,data):
	if not self.flag:
		self.flag=True

    def __init__(self,route,name,item):
	self.flag = False
	self.item = item
        rospy.init_node('move_base_sequence')
	self.pose_seq = list()
	self.route = route
	self.goal_cnt = 0
	self.rate = rospy.Rate(5)
	self.pub = rospy.Publisher('/'+name+'/arrive',String,queue_size=10)
	self.sub = rospy.Subscriber('/'+name+'/next_action',String,self.call)
        #Create action client
	for r in self.route: #change route to Pose information in order to use navigation
		temp = Pose(Point(r[0],r[1],0.0),Quaternion(0.0,0.0,r[2],r[3]))
		self.pose_seq.append(temp)
        self.client = actionlib.SimpleActionClient('/'+name+'/move_base',MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        wait = self.client.wait_for_server(rospy.Duration(5.0))
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            return 1
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting goals achievements ...")
        self.movebase_client()

    def active_cb(self):
        rospy.loginfo("Goal pose "+str(self.goal_cnt+1)+" is now being processed by the Action Server...")

    def feedback_cb(self, feedback):
        #To print current pose at each feedback:
        #rospy.loginfo("Feedback for goal "+str(self.goal_cnt)+": "+str(feedback))
        rospy.loginfo("Feedback for goal pose "+str(self.goal_cnt+1)+" received")

    def done_cb(self, status, result):
        self.goal_cnt += 1
    # Reference for terminal status values: http://docs.ros.org/diamondback/api/actionlib_msgs/html/msg/GoalStatus.html
        if status == 2:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request after it started executing, completed execution!")

        if status == 3:   #goal reached
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" reached") 
            if self.goal_cnt< len(self.pose_seq):
		if self.goal_cnt == len(self.pose_seq)-1:
			self.pub.publish("0 0")
		else :
			self.pub.publish("1 "+self.item[self.goal_cnt-1])
                next_goal = MoveBaseGoal()
                next_goal.target_pose.header.frame_id = "map"
                next_goal.target_pose.header.stamp = rospy.Time.now()
                next_goal.target_pose.pose = self.pose_seq[self.goal_cnt]
		while not self.flag:
			self.rate.sleep()
		self.flag = False
                rospy.loginfo("Sending next goal "+self.item[self.goal_cnt]+" to Action Server. With received "+self.item[self.goal_cnt-1])
                rospy.loginfo(str(self.pose_seq[self.goal_cnt]))
                self.client.send_goal(next_goal, self.done_cb, self.active_cb, self.feedback_cb) 
            else:
		self.pub.publish("2 2")
                rospy.loginfo("Final goal pose reached!")
                rospy.signal_shutdown("Final goal pose reached!")
                return 3

        if status == 4:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" was aborted by the Action Server")
            rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" aborted, shutting down!")
            return 4

        if status == 5:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" has been rejected by the Action Server")
            rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" rejected, shutting down!")
            return 5

        if status == 8:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request before it started executing, successfully cancelled!")

    def movebase_client(self):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now() 
        goal.target_pose.pose = self.pose_seq[self.goal_cnt]
        rospy.loginfo("Sending goal pose "+str(self.goal_cnt+1)+" to Action Server")
        rospy.loginfo(str(self.pose_seq[self.goal_cnt]))
        self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)
        rospy.spin()

if __name__ == '__main__':
	try:
		parser = argparse.ArgumentParser() #parameters  are passed by main.py for navigation
		parser.add_argument('-p1',nargs="+",type=float) #position
		parser.add_argument('-p2',nargs="+",type=float)
		parser.add_argument('-p3',nargs="+",type=float)
		parser.add_argument('-p4',nargs="+",type=float)
		parser.add_argument('-p5',nargs="+",type=float)
		parser.add_argument('-p6',nargs="+",type=float)
		parser.add_argument('-pname',type=str)  #car id
		parser.add_argument('-pdata',nargs="+",type=str) #desired item
		args = parser.parse_args()
		temp = list() #list of arg value
		i = 0
		for arg in sorted(vars(args)):
			i+=1
			if i == 7:
				break
			if getattr(args,arg) is not None:
				print(arg)
				temp.append(getattr(args,arg))
		print(temp)
        	MoveBaseSeq(temp,args.pname,args.pdata)
	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation finished.")
