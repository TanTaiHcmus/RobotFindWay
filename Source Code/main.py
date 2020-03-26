
#%%
import random 
import matplotlib.pyplot as plt
import numpy as np
from Polygon import *
from AlgorithmFunction import *
from ToolFunction import *
from time import time

#%%
#main program
def main_12(filename,choose=1):
  arrInput=loadFileInput(filename)
  
  #Export data from Input

  #1 Data range
  dataRange=arrInput[0].split(',')
  xRange,yRange=int(dataRange[0]),int(dataRange[1])
  #2 List Point of the route
  dataRoutePoint=arrInput[1].split(',')
  xRoute=[int(value) for index,value in enumerate(dataRoutePoint) if index%2==0]
  yRoute=[int(value) for index,value in enumerate(dataRoutePoint) if index%2==1]
  #3 List Polygon
  n=int(arrInput[2])
  listPolygon=[]
  for i in range(3,len(arrInput)):
    x=[int(value) for index,value in enumerate(arrInput[i].split(',')) if index%2==0]
    y=[int(value) for index,value in enumerate(arrInput[i].split(',')) if index%2==1]
    points=[[valuex,y[j]] for j,valuex in enumerate(x)]
    listPolygon.append(Polygon(len(x),points))

  pathX,pathY,cost=None,None,None
  
  start_time = time()
  if (choose==2):
    alg=AlgDijkstraHeap(xRange,yRange,xRoute[0],yRoute[0],xRoute[-1],yRoute[-1],listPolygon).dijkstraHeap()
    pathX,pathY=alg.getPath()
    cost=alg.getCost()
  elif (choose==3):
    alg=AlgAStar(xRange,yRange,xRoute[0],yRoute[0],xRoute[-1],yRoute[-1],listPolygon).aStar()
    pathX,pathY=alg.getPath()
    cost=alg.getCost()
  else:
    alg=AlgBFS(xRange,yRange,xRoute[0],yRoute[0],xRoute[-1],yRoute[-1],listPolygon)
    pathX,pathY,cost=alg.BFS()
  
  end_time = time()
  print('Time running this Algorithm: %f ms',(end_time - start_time) * 1000)
  resultX=[x for x in pathX if x>0][::-1]
  resultY=[y for y in pathY if y>0][::-1]
  plotResult(xRange, yRange, listPolygon, [resultX,resultY],[xRoute,yRoute],cost)

#%%
def main_3(filename):
  arrInput=loadFileInput(filename)

  #Export data from Input

  #1 Data range
  dataRange=arrInput[0].split(',')
  xRange,yRange=int(dataRange[0]),int(dataRange[1])
  #2 List Point of the route
  dataRoutePoint=arrInput[1].split(',')
  xRoute=[int(value) for index,value in enumerate(dataRoutePoint) if index%2==0]
  yRoute=[int(value) for index,value in enumerate(dataRoutePoint) if index%2==1]
  #3 List Polygon
  n=int(arrInput[2])
  listPolygon=[]
  for i in range(3,len(arrInput)):
    x=[int(value) for index,value in enumerate(arrInput[i].split(',')) if index%2==0]
    y=[int(value) for index,value in enumerate(arrInput[i].split(',')) if index%2==1]
    points=[[valuex,y[j]] for j,valuex in enumerate(x)]
    listPolygon.append(Polygon(len(x),points))
  
  alg=BitDynamicPlanning(xRange,yRange,[xRoute,yRoute],listPolygon)
  alg.bitDynamicPlanning()
  

#%%
def main_4(filename):
  arrInput=loadFileInput(filename)

  #Export data from Input

  #1 Data range
  dataRange=arrInput[0].split(',')
  xRange,yRange=int(dataRange[0]),int(dataRange[1])
  #2 List Point of the route
  dataRoutePoint=arrInput[1].split(',')
  xRoute=[int(value) for index,value in enumerate(dataRoutePoint) if index%2==0]
  yRoute=[int(value) for index,value in enumerate(dataRoutePoint) if index%2==1]
  #3 List Polygon
  n=int(arrInput[2])
  listPolygon=[]
  for i in range(3,len(arrInput)):
    x,y=[],[]
    direct=1
    area=[[],[]]
    speed=1
    for index,value in enumerate(arrInput[i].split(',')):
      if index==0:
        if value=="L": direct=2
        elif value=="U": direct=3
        elif value=="D": direct=4
      if index==2 or index==3:
        area[0].append(int(value))
      if index==4 or index==5:
        area[1].append(int(value))
      if index==1: speed=int(value)
      if index>5:
        if index%2==0: x.append(int(value))
        else: y.append(int(value))
    points=[[valuex,y[j]] for j,valuex in enumerate(x)]
    listPolygon.append(Polygon(len(x),points,area,direct,speed))
  
  alg=AlgBFS(xRange,yRange,xRoute[0],yRoute[0],xRoute[-1],yRoute[-1],listPolygon)
  pathX,pathY,cost,step=alg.BFSMoving()
  plotAnimationResult(xRange,yRange,listPolygon,[pathX[::-1],pathY[::-1]],[xRoute,yRoute],step)
  


#%%
main_4("inputMove3.txt")
#%%
main_12('input5.txt',1)
#%%
main_3("inputMultiRoute3.txt")
#%%
