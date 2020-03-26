
#%%
import numpy as np
class Polygon:
  def __init__(self,numOfVer=3,listPoint=[],area=[],directMove=1,speed=1):
    self.numOfVer=numOfVer
    self.listPoint=listPoint
    self.eastPoint = min(self.listPoint, key = lambda t: t[0])
    self.westPoint = max(self.listPoint, key = lambda t: t[0])
    self.northPoint = max(self.listPoint, key = lambda t: t[1])
    self.southPoint = min(self.listPoint, key = lambda t: t[1])
    self.directMove = directMove
    self.area=area
    self.speed=speed
  
  def isInside(self,Point):
    #Đầu tiên kiểm tra nếu điểm không nằm trong khu vực chứa đa giác
    #so sánh tọa độ của điểm với các cực Đông, Tây, Nam, Bắc của đa giác
    if Point[0]<self.eastPoint[0] or Point[0]>self.westPoint[0] or Point[1]>self.northPoint[1] or Point[1]<self.southPoint[1]:
      return False

    #Nếu nằm trong khu vực đa giác
    #3 bước kiểm tra:
    #Bước 1: kiểm tra điểm có trùng với đỉnh nào của đa giác không
    #Bước 2: Kiểm tra điểm có nằm trên cạnh đa giác không
    #Bước 3: Kiểm tra điểm có nằm trong đa giác không thuật toán ray-casting
    n = self.numOfVer
    inside=False
    error=10e-3
    def cmp(a, b):
      return (a > b) - (a < b)
    for i in range(n):
      #Bước 1
      Ax,Ay=self.listPoint[i-1]
      Bx,By=self.listPoint[i]
      if (Point[0]==Ax and Point[1]==Ay) or (Point[0]==Bx and Point[1]==By): return True
      
      #Bước 2
      if ((Bx - Ax) * (Point[1] - Ay) == (Point[0] - Ax) * (By - Ay) and abs(cmp(Ax, Point[0]) + cmp(Bx, Point[0])) <= 1 and abs(cmp(Ay, Point[1]) + cmp(By, Point[1])) <= 1):
        return True
      
      #Bước 3
      #Kiểm tra nếu AB song song trục hoành và điểm P thuộc ĐOẠN AB
      if (abs(Ay - By) <= error) and (abs(By - Point[1]) <= error) and (Ax > Point[0]) != (Bx > Point[0]):
        return True
    
      #Kiểm tra nếu tung độ điểm P không lớn hơn max(Ay,By) và không nhỏ hơn min(Ay,By)
      #Nếu thỏa sẽ dùng thuật toán ray-casting
      if (Ay>=Point[1]) != (By>=Point[1]):
        coef=(Point[1]-By)*(Ax-Bx)/(Ay-By)+Bx
        if Point[0]==coef: return True
        elif Point[0]<coef: inside=not inside
    return inside

  def getMovedListPoint(self,step):
    flag=1
    move=0
    #nếu di chuyển ngang
    if self.directMove==1 or self.directMove==2:
      if self.directMove==2: flag=-1
      
      xLeft=self.area[0][0]
      xRight=self.area[1][0]-(self.westPoint[0]-self.eastPoint[0])
      width=xRight-xLeft
      
      if width==0: return self.listPoint
      
      if ((self.eastPoint[0]-xLeft + self.speed*step*flag) // width) % 2 ==0:
        xNew=(self.eastPoint[0]-xLeft + self.speed*step*flag) % width + xLeft
      else:
        xNew=-((self.eastPoint[0]-xLeft + self.speed*step*flag) % width) + xRight
      
      move=xNew-self.eastPoint[0]
      listPoint=np.array(self.listPoint)
      return (listPoint+[move,0]).tolist()
    else:
      if self.directMove==4: flag=-1
      
      yBot=self.area[0][1]
      yTop=self.area[1][1]-(self.northPoint[1]-self.southPoint[1])
      height=yTop-yBot
      if height==0: return self.listPoint
      
      if ((self.southPoint[1]-yBot + self.speed*step*flag) // height) % 2 ==0:
        yNew=(self.southPoint[1]-yBot + self.speed*step*flag) % height + yBot
      else:
        yNew=-((self.southPoint[1]-yBot + self.speed*step*flag) % height) + yTop
      
      move=yNew-self.southPoint[1]
      listPoint=np.array(self.listPoint)
      return (listPoint+[0,move]).tolist()
  
  def isInsideMoved(self,Point,movedListPoint):
    eastPoint = min(movedListPoint, key = lambda t: t[0])
    westPoint = max(movedListPoint, key = lambda t: t[0])
    northPoint = max(movedListPoint, key = lambda t: t[1])
    southPoint = min(movedListPoint, key = lambda t: t[1])
    #Đầu tiên kiểm tra nếu điểm không nằm trong khu vực chứa đa giác
    #so sánh tọa độ của điểm với các cực Đông, Tây, Nam, Bắc của đa giác
    if Point[0]<eastPoint[0] or Point[0]>westPoint[0] or Point[1]>northPoint[1] or Point[1]<southPoint[1]:
      return False

    #Nếu nằm trong khu vực đa giác
    #3 bước kiểm tra:
    #Bước 1: kiểm tra điểm có trùng với đỉnh nào của đa giác không
    #Bước 2: Kiểm tra điểm có nằm trên cạnh đa giác không
    #Bước 3: Kiểm tra điểm có nằm trong đa giác không thuật toán ray-casting
    n = self.numOfVer
    inside=False
    error=10e-3
    def cmp(a, b):
      return (a > b) - (a < b)
    for i in range(n):
      #Bước 1
      Ax,Ay=movedListPoint[i-1]
      Bx,By=movedListPoint[i]
      if (Point[0]==Ax and Point[1]==Ay) or (Point[0]==Bx and Point[1]==By): return True
      
      #Bước 2
      if ((Bx - Ax) * (Point[1] - Ay) == (Point[0] - Ax) * (By - Ay) and abs(cmp(Ax, Point[0]) + cmp(Bx, Point[0])) <= 1 and abs(cmp(Ay, Point[1]) + cmp(By, Point[1])) <= 1):
        return True
      
      #Bước 3
      #Kiểm tra nếu AB song song trục hoành và điểm P thuộc ĐOẠN AB
      if (abs(Ay - By) <= error) and (abs(By - Point[1]) <= error) and (Ax > Point[0]) != (Bx > Point[0]):
        return True
    
      #Kiểm tra nếu tung độ điểm P không lớn hơn max(Ay,By) và không nhỏ hơn min(Ay,By)
      #Nếu thỏa sẽ dùng thuật toán ray-casting
      if (Ay>=Point[1]) != (By>=Point[1]):
        coef=(Point[1]-By)*(Ax-Bx)/(Ay-By)+Bx
        if Point[0]==coef: return True
        elif Point[0]<coef: inside=not inside
    return inside
#%%
