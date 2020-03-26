#%%
#READ INPUT
def loadFileInput(filename):
#return string array with all of lines in input.txt
    arrInput = []
    try:
        fileInput = open(filename, 'r')
        for line in fileInput:
            arrInput.append(line)
    finally:
        fileInput.close()
    return arrInput

#%%
import numpy as np
import matplotlib.pyplot as plt
def plotResult(xRange, yRange, listPolygon, result, route,cost=10e9):
    fig = plt.figure(figsize=(xRange/2.5,yRange/2.5))
    ax = fig.gca()
    plt.xlim(0,xRange)
    plt.ylim(0,yRange)
    ax.set_xticks(np.arange(0, xRange, 1))
    ax.set_yticks(np.arange(0, yRange, 1))
    plt.grid(which='major', axis='both', linestyle='solid', color='red', linewidth=0.2)
    for i in listPolygon:
        poly=i.listPoint.copy()
        poly.append(poly[0])
        plt.plot(np.array(poly)[:,0],np.array(poly)[:,1],'go-')
    if len(result[0])>0:
        plt.plot(np.array(result[0]),np.array(result[1]),linestyle='solid', marker='o', markerfacecolor='blue', markersize=5)
    else:
        plt.text(xRange/2, yRange/2, 'SORRY WE CAN\'T FIND THE WAY', horizontalalignment='center',verticalalignment='center',fontsize=yRange/2*1.5)
    plt.plot(np.array(route[0]),np.array(route[1]),'go',marker='o',markerfacecolor='white',markersize=12)
    plt.text(route[0][0]+0.5,route[1][0]+0.5,'Start',fontsize=12)
    plt.text(route[0][-1]+0.5,route[1][-1]+0.5,'End',fontsize=12)
    if (abs(cost-10e9)>0.001):
        print("Length=",cost)
    plt.show()

#%%
#%%
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def plotAnimationResult(xRange,yRange,listPolygon,result, route, step):
    fig = plt.figure(figsize=(xRange/2.5,yRange/2.5))
    ax = fig.gca()
    ax.set_xlim(0,xRange)
    ax.set_ylim(0,yRange)
    ax.set_xticks(np.arange(0, xRange, 1))
    ax.set_yticks(np.arange(0, yRange, 1))
    plt.grid(which='major', axis='both', linestyle='solid', color='red', linewidth=0.2)

    poly = [plt.plot([], [])[0] for _ in range(len(listPolygon))]
    plt.plot(np.array(route[0]),np.array(route[1]),'go',marker='o',markerfacecolor='white',markersize=12)
    plt.text(route[0][0]+0.5,route[1][0]+0.5,'Start',fontsize=12)
    plt.text(route[0][-1]+0.5,route[1][-1]+0.5,'End',fontsize=12)

    if len(result[0])>0:
        def animate(i):
            for j in range(len(listPolygon)):
                newList=listPolygon[j].getMovedListPoint(i)
                newList.append(newList[0])
                poly[j].set_data(np.array(newList)[:,0].tolist(),np.array(newList)[:,1].tolist())
            plt.plot([result[i][0]],[result[i][1]],linestyle='solid', marker='o', markerfacecolor='blue', markersize=5)
            return poly
        anim = animation.FuncAnimation(fig, animate, frames=step, interval=200, blit=True)
        anim.save('test1.gif', writer='imagemagick')
    else:
        plt.text(xRange/2, yRange/2, 'SORRY WE CAN\'T FIND THE WAY', horizontalalignment='center',verticalalignment='center',fontsize=yRange/2*1.5)

#%%
