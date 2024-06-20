#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import actionlib
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import time
import pak
import os

class Car():
    def __init__(self):
        self.tally_car = list()
        self.send_car = list()

    def schedule(self):
        """"""
        sql = pak.cars()
	while pak.takeTask(sql) == "er": #get data from db
            print('no car need to schedule')
            time.sleep(5)
        #sql = [{'J1':(1,10,0)},{'J2':(1,10,1)}]#get car:taskID,max,type
        sql1 = list()
        for i in range(len(sql.carids)):
            sql1.append({str(sql.carids[i]):(int(sql.taskid),int(sql.accomodates[i]),int(sql.cartypes[i]))})
        sql2 = list()
        for i in range(len(sql.merchans)):
            sql2.append({int(sql.taskid):(int(sql.merchans[i][0]),int(sql.merchans[i][1]))})
        pak.launchMerchan(sql)
        
        for i in range(len(sql.merchans)):
            pak.carArrive(sql,sql.carids[0])
        
        if len(sql1) != 0:
            #sql2 = [{1:(0,2)}] #get taskID:itemID,weight
            for car in sql1:
                temp = list()
                mid = list(car.values())[0]
                max = int(mid[1])
                for task in sql2:
                    taskID,item = list(task.keys())[0],list(task.values())[0]
                    if mid[0] == taskID and max >= int(item[1]):
                        temp.append(item[0])
                        max -= int(item[1])
                if mid[2] == 0:
                    self.tally_car.append({list(car.keys())[0]:temp})
                elif mid[2] == 1:
                    self.send_car.append({list(car.keys())[0]:temp})
            print('tally_car:',self.tally_car)
            print('send_car:',self.send_car)
    def get_car(self):
        return self.tally_car,self.send_car
    
class Nav():
    # position data
    j1_init = [-0.023,-0.662,0.041,0.999]
    j2_init = [-0.837,-0.843,0.01,1.0]
    j2_end  = [-0.723,0.448,1.0,-0.008]
    j1_park = [0.148,0.064,-0.681,0.732]
    #x,y,w
    item_position = [  #1.045,-0.693,0.042,0.999
                        [1.066,-0.852,0.043,1.0], #item1
                        [1.06,-0.392,0.688,0.726],
                        [1.127,0.152,-0.009,1.0],
                        [1.016,0.602,0.688,0.726], #item4
                    ]
    park_position = [-0.026,-0.089,0.707,0.712]

    name = ["jetsonnano"  , "screw"  , "camera"  , "lidar"]

    def __init__(self):
        self.car = Car()
        rospy.init_node('nav_planner', anonymous=True)
 
    def callback(self,data): #print stats from camera.py
        log = data.data.split(' ')
        if log[1] == '0':
            print(str(log[0])+" to inital position finished")
        elif log[1] == '-1':
            print("Sending car "+str(log[0])+" to park position finished")
        else:
            print("car "+str(log[0])+" finished "+self.data_list[int(log[1])-1])

    def start(self):
        self.car.schedule()
        cid = list()
        for car in self.car.tally_car:
            cid.append(list(car.keys())[0])
        for car in self.car.send_car:
            cid.append(list(car.keys())[0])
        self.sub = [rospy.Subscriber('/'+str(id)+'/next_action', String, self.callback) for id in cid ]   #listen to next_action. For the purpose of knowing the stats of tally car

    def move(self,cmd):
        x = 1
        while x != 0 and x!=2:  
            x = os.system(cmd) #use subprogram to navigate
            print(x) 
            
    def navigating(self):
        route = list()
        tally_car,send_car = self.car.get_car()
	
        for car in send_car:  #1 send car, plan route
            points = ""
            cid = list(car.keys())[0]
            print("car:"+str(cid)+" is going to receive item ")
            route.append(self.park_position)
            for _,i in enumerate(route):
                temp = "-p"+str((_+1))+" "
                for j in i:
                    temp += str(j)+" "
                points+= temp
            points+=(("-pname "+str(cid)))
            cmd = 'rosrun navstack plan.py '+points
            self.move(cmd)  #start navigation
	""""""
        route = list()
        for car in tally_car:  #2 tally car, plan route
            cid = cid = list(car.keys())[0]
            points = ""
            data = ""
            for plan in  list(car.values())[0]:
		print("car:"+str(cid)+" is going to tally item "+str(plan))
                route.append(self.item_position[plan])
		data += self.name[plan]+" "
            data += "park init"
            self.data_list = data
            route.append(self.j1_park)
            route.append(self.j1_init)
            for _,i in enumerate(route):
                temp = "-p"+str((_+1))+" "
                for j in i:
                    temp += str(j)+" "
                points+= temp
            points += ("-pname "+str(cid))
            points += (" -pdata "+data)
            cmd = 'rosrun navstack plan.py '+points
            self.move(cmd) #start navigation
        
        route = list()

        for car in send_car:  #3 send car , plan route
            points = ""
            cid = list(car.keys())[0]
            print("car:"+str(cid)+" is going to send item ")
            route.append(self.j2_end)
            for _,i in enumerate(route):
                temp = "-p"+str((_+1))+" "
                for j in i:
                    temp += str(j)+" "
                points+= temp
            points+=(("-pname "+str(cid)))
            cmd = 'rosrun navstack plan.py '+points
            self.move(cmd) #start navigation
    	""""""
def main():
    while True:
        navigation = Nav()
        navigation.start() #get data from db and schedule cars
        
        
        navigation.navigating() #start navigation
        print('finish')

if __name__ == '__main__':
    main()
    
    
    
