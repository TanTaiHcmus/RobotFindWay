
#%%
import numpy as np
from Polygon import *
#%%
class AlgBFS:
    moveX=[1,-1,0,0,1,1,-1,-1]
    moveY=[0,0,1,-1,1,-1,1,-1]
    lenStep= [1, 1, 1, 1, 1.5, 1.5, 1.5, 1.5]
    def __init__(self,xRange,yRange,sx,sy,tx,ty,listPolygon):
        self.xRange=xRange
        self.yRange=yRange
        self.listPolygon=listPolygon
        self.sx=sx 
        self.sy=sy
        self.tx=tx
        self.ty=ty
        self.pathX=[]
        self.pathY=[]
        self.queueX = [0]*xRange*yRange
        self.queueY = [0]*xRange*yRange
        self.trace=[0]*xRange*yRange
        self.visited= np.array([False]*xRange*yRange).reshape(xRange,yRange)
        self.cost=[0]*xRange*yRange

    def isQualifiedStep(self, x, step, maxRange):
	    if (x + step < 1): return False
	    if (x + step >= maxRange): return False
	    return True

    def isInsidePolygon(self,Point):
        for polygon in self.listPolygon:
            if polygon.isInside(Point): return True
        return False
    
    def isInsideMovedPolygon(self,Point,step):
        for polygon in self.listPolygon:
            if polygon.isInsideMoved(Point,polygon.getMovedListPoint(step)):
                return True
        return False
    
    def BFS(self):
        dem = 1
        tmp = 1
        vt = 0
        self.queueX[0] = self.sx
        self.queueY[0] = self.sy
        while(True):
            for i in range(vt,dem):
                #print("i=",i,"  ","dem=",dem,"  ","tmp=",tmp)
                for j in range(0,8):
                    if (self.isQualifiedStep(self.queueX[i],self.moveX[j], self.xRange) and self.isQualifiedStep(self.queueY[i],self.moveY[j], self.yRange)):
                        if self.isInsidePolygon([self.queueX[i]+self.moveX[j],self.queueY[i]+self.moveY[j]])==False:
                            if (self.visited[self.queueX[i] + self.moveX[j],self.queueY[i] + self.moveY[j]]==False):
                                self.visited[self.queueX[i] + self.moveX[j],self.queueY[i] + self.moveY[j]] = True
                                self.queueX[tmp] = self.queueX[i] + self.moveX[j]
                                self.queueY[tmp] = self.queueY[i] + self.moveY[j]
                                self.cost[tmp]=self.cost[i]+self.lenStep[j]
                                self.trace[tmp] = i
                                tmp+=1
                                #print("new tmp=",tmp)
                                if (self.visited[self.tx,self.ty] == True): break
                if (self.visited[self.tx,self.ty] == True): break
            if dem==tmp: return self.pathX,self.pathY,10e9
            vt = dem
            dem = tmp
            #print("new vt=",vt,"  ","new dem=",tmp)
            if (self.visited[self.tx,self.ty] == True): break
        d = 1
        result=[0]*self.xRange*self.yRange
        result[0] = tmp - 1
        while (True):
            result[d] = self.trace[result[d - 1]]
            d+=1
            if (result[d - 1] == 0): break

        self.pathX.extend([self.queueX[result[i]] for i in range(d-1,-1,-1)][::-1])
        self.pathY.extend([self.queueY[result[i]] for i in range(d-1,-1,-1)][::-1])
        
        return self.pathX,self.pathY,self.cost[tmp-1]

    def BFSMoving(self):
        dem = 1
        tmp = 1
        vt = 0
        self.queueX[0] = self.sx
        self.queueY[0] = self.sy
        step=0
        while(True):
            step+=1
            for i in range(vt,dem):
                for j in range(0,8):
                    if (self.isQualifiedStep(self.queueX[i],self.moveX[j], self.xRange) and self.isQualifiedStep(self.queueY[i],self.moveY[j], self.yRange)):
                        if self.isInsideMovedPolygon([self.queueX[i]+self.moveX[j],self.queueY[i]+self.moveY[j]],step)==False:
                            if (self.visited[self.queueX[i] + self.moveX[j],self.queueY[i] + self.moveY[j]]==False):
                                self.visited[self.queueX[i] + self.moveX[j],self.queueY[i] + self.moveY[j]] = True
                                self.queueX[tmp] = self.queueX[i] + self.moveX[j]
                                self.queueY[tmp] = self.queueY[i] + self.moveY[j]
                                self.cost[tmp]=self.cost[i]+self.lenStep[j]
                                self.trace[tmp] = i
                                tmp+=1
                                if (self.visited[self.tx,self.ty] == True): break
                if (self.visited[self.tx,self.ty] == True): break
            if dem==tmp: return self.pathX,self.pathY,10e9,0
            vt = dem
            dem = tmp
            if (self.visited[self.tx,self.ty] == True): break
        d = 1
        result=[0]*self.xRange*self.yRange
        result[0] = tmp - 1
        while (True):
            result[d] = self.trace[result[d - 1]]
            d+=1
            if (result[d - 1] == 0): break

        self.pathX.extend([self.queueX[result[i]] for i in range(d-1,-1,-1)][::-1])
        self.pathY.extend([self.queueY[result[i]] for i in range(d-1,-1,-1)][::-1])
        
        return self.pathX,self.pathY,self.cost[tmp-1],step
#%%
class Path:
    def __init__(self,startRoute,endRoute):
        self.sx,self.sy=startRoute[0],startRoute[1]
        self.tx,self.ty=endRoute[0],endRoute[1]
        self.cost=10e9
        self.pathX=[]
        self.pathY=[]
    def setRoad(self,pathX, pathY, numOfRoad, cost):
        self.numOfRoad=numOfRoad
        self.cost=cost
        self.pathX=pathX.copy()
        self.pathY=pathY.copy()
    def getIsRoad(self, value):
        return self.isRoad==value
    def setIsRoad(self,value):
        self.isRoad=value
    def getCost(self):
        return self.cost
    def getPath(self):
        return self.pathX,self.pathY
    def getNRoad(self):
        return self.numOfRoad
    
#%%
class AlgDijkstraHeap:    
    moveX = [ 1, 1, 1, 0, 0, -1, -1, -1 ]
    moveY = [ 0, -1, 1, 1, -1, 0, -1, 1 ]
    lenStep= [1, 1.5, 1.5, 1, 1, 1, 1.5, 1.5]
    maxValue=10e9
    #main class
    def __init__(self,xRange,yRange,sx,sy,tx,ty,listPolygon):
        self.xRange=xRange
        self.yRange=yRange
        self.sx,self.sy=sx,sy
        self.tx,self.ty=tx,ty
        self.listPolygon=listPolygon

        self.distance=np.array([self.maxValue]*xRange*yRange).reshape(xRange,yRange)
        self.distance[sx][sy]=0
        
        self.state=np.array([True]*xRange*yRange).reshape(xRange,yRange)
        
        self.nHeap=0
        
        self.traceX = np.zeros(shape=(xRange,yRange),dtype=int)
        self.traceY = np.zeros(shape=(xRange,yRange),dtype=int)
        
        self.heapX=[0]*xRange*yRange
        self.heapY=[0]*xRange*yRange
        
        self.position=np.zeros(shape=(xRange,yRange),dtype=int)

        self.pathX=[]
        self.pathY=[]

        self.cost=10e9
    
    def upHeap(self,i):
        if (i > 1 and self.distance[self.heapX[i],self.heapY[i]] < self.distance[self.heapX[i // 2],self.heapY[i // 2]]):
            self.heapX[i], self.heapX[i // 2]=self.heapX[i // 2],self.heapX[i]
            self.heapY[i], self.heapY[i // 2]=self.heapY[i // 2],self.heapY[i]
            self.position[self.heapX[i],self.heapY[i]], self.position[self.heapX[i // 2],self.heapY[i // 2]]=self.position[self.heapX[i // 2],self.heapY[i // 2]],self.position[self.heapX[i],self.heapY[i]]
            self.upHeap(i // 2)
    
    def downHeap(self,i):
        j = i * 2
        if (j > self.nHeap): return
        elif j < self.nHeap and self.distance[self.heapX[j],self.heapY[j]] > self.distance[self.heapX[j + 1],self.heapY[j + 1]]:
            j+=1
        if (self.distance[self.heapX[i],self.heapY[i]] > self.distance[self.heapX[j],self.heapY[j]]):
            self.heapX[i], self.heapX[j]=self.heapX[j], self.heapX[i]
            self.heapY[i], self.heapY[j]=self.heapY[j], self.heapY[i]
            self.position[self.heapX[i],self.heapY[i]], self.position[self.heapX[j],self.heapY[j]]=self.position[self.heapX[j],self.heapY[j]],self.position[self.heapX[i],self.heapY[i]]
            self.downHeap(j)
    
    def addHeap(self, x, y):
        self.nHeap+=1
        self.heapX[self.nHeap] = x
        self.heapY[self.nHeap] = y
        self.position[x][y] = self.nHeap
        self.upHeap(self.nHeap)
    
    def removeHeap(self):
        self.heapX[1], self.heapX[self.nHeap]= self.heapX[self.nHeap], self.heapX[1]
        self.heapY[1], self.heapY[self.nHeap]= self.heapY[self.nHeap], self.heapY[1]
        self.position[self.heapX[1],self.heapY[1]] = 1
        self.nHeap-=1
        self.downHeap(1)

    def isQualifiedStep(self,x, step, maxRange):
	    if (x + step < 1): return False
	    if (x + step >= maxRange): return False
	    return True
    
    def isInsidePolygon(self,Point):
        for polygon in self.listPolygon:
            if polygon.isInside(Point): return True
        return False

    def dijkstraHeap(self):
        self.nHeap=0
        self.pathX=[]
        self.pathY=[]
        path=Path([self.sx,self.sy],[self.tx,self.ty])
        check = False
        for i in range(1,self.xRange):
            for j in range(1,self.yRange):
                self.addHeap(i,j)
        while (True):
            ux = self.heapX[1]
            uy = self.heapY[1]
            if ux == self.tx and uy == self.ty:
                check = True
                break
            if self.distance[ux][uy] == self.maxValue: break
            self.removeHeap()
            self.state[ux][uy] = False
            for i in range(0,8):
                if self.isQualifiedStep(ux,self.moveX[i],self.xRange) and self.isQualifiedStep(uy, self.moveY[i], self.yRange):
                    if self.isInsidePolygon([ux+self.moveX[i],uy+self.moveY[i]])==False:
                        if (self.state[ux + self.moveX[i],uy + self.moveY[i]] ==True) and self.distance[ux + self.moveX[i],uy + self.moveY[i]] > self.distance[ux,uy] + self.lenStep[i]:
                            self.distance[ux + self.moveX[i],uy + self.moveY[i]] = self.distance[ux,uy] + self.lenStep[i]
                            self.traceX[ux + self.moveX[i],uy + self.moveY[i]] = ux
                            self.traceY[ux + self.moveX[i],uy + self.moveY[i]] = uy
                            self.upHeap(self.position[ux + self.moveX[i],uy + self.moveY[i]])
        if check:
            self.pathX.append(self.tx)
            self.pathY.append(self.ty)
            d = 0
            while (True):
                d+=1
                self.pathX.append(self.traceX[self.pathX[d - 1],self.pathY[d - 1]])
                self.pathY.append(self.traceY[self.pathX[d - 1],self.pathY[d - 1]])
                if (self.pathX[d] == self.sx and self.pathY[d] == self.sy): break
            path.setRoad(self.pathX, self.pathY, d + 1, self.distance[self.tx][self.ty])
            path.setIsRoad(True)
        else:
            path.setIsRoad(False)
        return path

#%%
class AlgAStar:    
    moveX = [ 1, 1, 1, 0, 0, -1, -1, -1 ]
    moveY = [ 0, -1, 1, 1, -1, 0, -1, 1 ]
    lenStep= [1, 1.5, 1.5, 1, 1, 1, 1.5, 1.5]
    maxValue=10e9
    #main class
    def __init__(self,xRange,yRange,sx,sy,tx,ty,listPolygon):
        self.xRange=xRange
        self.yRange=yRange
        self.sx,self.sy=sx,sy
        self.tx,self.ty=tx,ty
        self.listPolygon=listPolygon

        self.distanceSum=np.array([self.maxValue]*xRange*yRange).reshape(xRange,yRange)        
        self.distanceFromStart=np.array([self.maxValue]*xRange*yRange).reshape(xRange,yRange)
        self.distanceToEnd=np.array([self.maxValue]*xRange*yRange).reshape(xRange,yRange)

        self.state=np.array([True]*xRange*yRange).reshape(xRange,yRange)
        
        self.nHeap=0
        
        self.traceX = np.zeros(shape=(xRange,yRange),dtype=int)
        self.traceY = np.zeros(shape=(xRange,yRange),dtype=int)
        
        self.heapX=[0]*xRange*yRange
        self.heapY=[0]*xRange*yRange
        
        self.position=np.zeros(shape=(xRange,yRange),dtype=int)

        self.pathX=[]
        self.pathY=[]
    
    def upHeap(self,i):
        if (i > 1 and self.distanceSum[self.heapX[i],self.heapY[i]] < self.distanceSum[self.heapX[i // 2],self.heapY[i // 2]]):
            self.heapX[i], self.heapX[i // 2]=self.heapX[i // 2],self.heapX[i]
            self.heapY[i], self.heapY[i // 2]=self.heapY[i // 2],self.heapY[i]
            self.position[self.heapX[i],self.heapY[i]], self.position[self.heapX[i // 2],self.heapY[i // 2]]=self.position[self.heapX[i // 2],self.heapY[i // 2]],self.position[self.heapX[i],self.heapY[i]]
            self.upHeap(i // 2)
    
    def downHeap(self,i):
        j = i * 2
        if (j > self.nHeap): return
        elif j < self.nHeap and self.distanceSum[self.heapX[j],self.heapY[j]] > self.distanceSum[self.heapX[j + 1],self.heapY[j + 1]]:
            j+=1
        if (self.distanceSum[self.heapX[i],self.heapY[i]] > self.distanceSum[self.heapX[j],self.heapY[j]]):
            self.heapX[i], self.heapX[j]=self.heapX[j], self.heapX[i]
            self.heapY[i], self.heapY[j]=self.heapY[j], self.heapY[i]
            self.position[self.heapX[i],self.heapY[i]], self.position[self.heapX[j],self.heapY[j]]=self.position[self.heapX[j],self.heapY[j]],self.position[self.heapX[i],self.heapY[i]]
            self.downHeap(j)
    
    def addHeap(self, x, y):
        self.nHeap+=1
        self.heapX[self.nHeap] = x
        self.heapY[self.nHeap] = y
        self.position[x][y] = self.nHeap
        self.upHeap(self.nHeap)
    
    def removeHeap(self):
        self.heapX[1], self.heapX[self.nHeap]= self.heapX[self.nHeap], self.heapX[1]
        self.heapY[1], self.heapY[self.nHeap]= self.heapY[self.nHeap], self.heapY[1]
        self.position[self.heapX[1],self.heapY[1]] = 1
        self.nHeap-=1
        self.downHeap(1)

    def isQualifiedStep(self,x, step, maxRange):
	    if (x + step < 1): return False
	    if (x + step >= maxRange): return False
	    return True
    
    def isInsidePolygon(self,Point):
        for polygon in self.listPolygon:
            if polygon.isInside(Point): return True
        return False

    def euclideanDistance(self,point1,point2):
        return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**(1/2.0)

    def aStar(self):
        path=Path([self.sx,self.sy],[self.tx,self.ty])
        check = False

        for i in range(1,self.xRange):
            for j in range(1,self.yRange):
                self.distanceToEnd[i][j] = self.euclideanDistance([i,j],[self.tx,self.ty])
        self.distanceSum[self.sx][self.sy] = self.distanceToEnd[self.sx][self.sy]
        self.distanceFromStart[self.sx][self.sy] = 0
        
        for i in range(1,self.xRange):
            for j in range(1,self.yRange):
                self.addHeap(i,j)


        while (True):
            ux = self.heapX[1]
            uy = self.heapY[1]
            if ux == self.tx and uy == self.ty:
                check = True
                break
            if self.distanceSum[ux][uy] == self.maxValue: break
            self.removeHeap()
            self.state[ux][uy] = False
            for i in range(0,8):
                if self.isQualifiedStep(ux,self.moveX[i],self.xRange) and self.isQualifiedStep(uy, self.moveY[i], self.yRange):
                    if self.isInsidePolygon([ux+self.moveX[i],uy+self.moveY[i]])==False:
                        if (self.state[ux + self.moveX[i],uy + self.moveY[i]] ==True) and self.distanceFromStart[ux + self.moveX[i],uy + self.moveY[i]] > self.distanceFromStart[ux,uy] + self.lenStep[i]:
                            self.distanceFromStart[ux + self.moveX[i],uy + self.moveY[i]] = self.distanceFromStart[ux,uy] + self.lenStep[i]
                            self.distanceSum[ux + self.moveX[i],uy + self.moveY[i]] = self.distanceFromStart[ux + self.moveX[i],uy + self.moveY[i]] + self.distanceToEnd[ux + self.moveX[i],uy + self.moveY[i]]
                            self.traceX[ux + self.moveX[i],uy + self.moveY[i]] = ux
                            self.traceY[ux + self.moveX[i],uy + self.moveY[i]] = uy
                            self.upHeap(self.position[ux + self.moveX[i],uy + self.moveY[i]])
        if check:
            self.pathX.append(self.tx)
            self.pathY.append(self.ty)
            d = 0
            while (True):
                d+=1
                self.pathX.append(self.traceX[self.pathX[d - 1],self.pathY[d - 1]])
                self.pathY.append(self.traceY[self.pathX[d - 1],self.pathY[d - 1]])
                if (self.pathX[d] == self.sx and self.pathY[d] == self.sy): break
            path.setRoad(self.pathX, self.pathY, d + 1, self.distanceFromStart[self.tx][self.ty])
            path.setIsRoad(True)
        else:
            path.setIsRoad(False)
        return path

#%%
import matplotlib.pyplot as plt
from time import time
class BitDynamicPlanning:
    maxValue=10e9
    maxNumOfRoute=20
    def __init__(self,xRange,yRange,route,listPolygon):
        self.xRange=xRange
        self.yRange=yRange
        self.xRoute=route[0]
        self.yRoute=route[1]
        self.listPolygon=listPolygon
        self.numOfRoute=len(route[0])
        self.arr=np.array([self.maxValue]*(2**self.maxNumOfRoute)*self.maxNumOfRoute).reshape(2**self.maxNumOfRoute,self.maxNumOfRoute)
        self.prev=np.array([0]*(2**self.maxNumOfRoute)*self.maxNumOfRoute).reshape(2**self.maxNumOfRoute,self.maxNumOfRoute)
        self.distanceRoute=np.array([None]*self.maxNumOfRoute*self.maxNumOfRoute).reshape(self.maxNumOfRoute,self.maxNumOfRoute)
        self.path=np.array([None]*self.maxNumOfRoute*self.maxNumOfRoute).reshape(self.maxNumOfRoute,self.maxNumOfRoute)
    def getBit(self,x, i):
        return (x >> (self.numOfRoute - i)) & 1
    
    def plotPath(self,result=[[],[]]):
        plt.plot(np.array(result[0]),np.array(result[1]),linestyle='solid', marker='o',markerfacecolor='blue', markersize=5)
    
    def plotRoute(self):
        plt.plot(np.array(self.xRoute),np.array(self.yRoute),'go',marker='o',markerfacecolor='white',markersize=12)
        plt.text(self.xRoute[0]+0.5,self.yRoute[0]+0.5,'Start',fontsize=12)
        plt.text(self.xRoute[-1]+0.5,self.yRoute[-1]+0.5,'End',fontsize=12)
    
    def plotPolygon(self):
        fig = plt.figure(figsize=(self.xRange/2.5,self.yRange/2.5))
        ax = fig.gca()
        plt.xlim(0,self.xRange)
        plt.ylim(0,self.yRange)
        ax.set_xticks(np.arange(0, self.xRange, 1))
        ax.set_yticks(np.arange(0, self.yRange, 1))
        plt.grid(which='major', axis='both', linestyle='solid', color='red', linewidth=0.2)
        for i in self.listPolygon:
            poly=i.listPoint.copy()
            poly.append(poly[0])
            plt.plot(np.array(poly)[:,0],np.array(poly)[:,1],'go-')

    def bitDynamicPlanning(self):
        start_time = time()
        for i in range(0,self.numOfRoute):
            for j in range(0,self.numOfRoute):
                if (i!=j):
                    self.path[i,j] = AlgDijkstraHeap(self.xRange,self.yRange,self.xRoute[i],self.yRoute[i],self.xRoute[j],self.yRoute[j],self.listPolygon).dijkstraHeap()
        self.arr[2**(self.numOfRoute - 1)][0] = 0
        for i in range(2**(self.numOfRoute - 1)+1,2**self.numOfRoute):
            state=[False]*self.maxNumOfRoute
            
            for j in range(0,self.numOfRoute):
                if self.getBit(i,j+1)==1: state[j]=True
            
            if (i != (2**self.numOfRoute - 1) and state[self.numOfRoute - 1] == True):
                continue
            
            for j in range(1,self.numOfRoute):
                if (state[j]):
                    for k in range(0,self.numOfRoute-1):
                        if state[k] and k!=j:
                            if self.arr[i - 2**(self.numOfRoute - j - 1),k] + self.path[k,j].getCost() < self.arr[i,j]:
                                self.arr[i][j] = self.arr[i - 2**(self.numOfRoute - j - 1),k] + self.path[k,j].getCost()
                                self.prev[i,j] = k
        end_time = time()
        print('Time running this Algorithm: %f ms',(end_time - start_time) * 1000)
        
        self.plotPolygon()
        self.plotRoute()
        h=2**(self.numOfRoute)-1
        k=self.numOfRoute-1
        if self.arr[h,k]!=self.maxValue:
            totalCost=0
            while (True):
                pathX,pathY=self.path[k,self.prev[h,k]].getPath()
                self.plotPath([pathX,pathY])
                totalCost+=self.path[k,self.prev[h,k]].getCost()
                tmp=self.prev[h,k]
                h=h-2**(self.numOfRoute - k - 1)
                k=tmp
                if k==0: break
            print("Total length: ",totalCost)
        else:
            plt.text(self.xRange/2, self.yRange/2, 'SORRY WE CAN\'T FIND THE WAY', horizontalalignment='center',verticalalignment='center',fontsize=self.yRange/2*1.5)    
        plt.show()

