import requests
from bs4 import BeautifulSoup as bs
import time
class cars:
    def __init__(self):
        self.carids=[]
        self.cartypes=[]
        self.merchans=[]
        self.accomodates=[]
        self.taskid=-1
    def pushMerchan(self,merchan,quantity):
        arr=[merchan,quantity]
        self.merchans.append(arr)
    def pushCar(self,cid,accomodate,ctype):
        self.carids.append(cid)
        self.accomodates.append(accomodate)
        self.cartypes.append(ctype)

ipp="http://192.168.39.243:3000"
def concatUrl(string):
    return ipp+"?"+string
def takeTask(car):
    url=concatUrl("command=takeTask")
    res=requests.get(url)
    content=res.text.split("\n")
    contentType=0
    j = 0
    for i in content:
        j+=1
        print("J: ",j)	
        if(("," not in i) and ("task" not in i)):
            
            break
        if("task" in i):
            if(len(car.carids)==0):
                return "er"
            contentType=1
            continue
        if(contentType==0):
            data=i.split(",")
            car.pushCar(data[0],data[2],data[3])
        if(contentType==1):
            print(i)
            data=i.split(",")
            car.taskid=data[0]
            car.pushMerchan(data[1],data[2])
            print(data)
    if len(car.merchans) == 0:
        car.carids.clear()
        return "er"
    url=concatUrl("command=taskDecided&taskID="+car.taskid)
    print(url)
    requests.get(url)
    return "success"
    
def launchMerchan(car):
    for i in car.merchans:
        time.sleep(0.5)
        print("OP  : ",len(car.merchans))
        url=concatUrl("command=startTransferring&taskID="+str(car.taskid)+"&merchanID="+str(i[0])+"&quantity="+str(i[1]))
        print(url)
        requests.get(url)
def afind(arr,ele):
    for i in range(0,len(arr)):
        if arr[i]==ele:
            return i
    return -1
def carArrive(car,cid):
    url=concatUrl("command=transferArrive&carID="+str(cid))
    print(url)
    requests.get(url)
    index=afind(car.carids,cid)
    car.carids.pop(index)
    car.cartypes.pop(index)
    car.accomodates.pop(index)
    car.merchans.pop(index)
