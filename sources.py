import pygame
import numpy


imgs = [pygame.image.load('bmp/wall.png'),
        pygame.image.load('bmp/Worker.png'),
        pygame.image.load('bmp/Box.png'),
        pygame.image.load('bmp/Passageway.png'),
        pygame.image.load('bmp/Destination.png'),
        pygame.image.load('bmp/WorkerInDest.png'),
        pygame.image.load('bmp/RedBox.png')]

# 0代表墙，1代表人，2代表箱子，3代表路，4代表目的地
# 5代表人在目的地，6代表放到目的地的箱子
wall = 0
worker = 1
box = 2
road = 3
destination = 4
man_in_des = 5
box_in_des = 6

map = [[0, 3, 1, 4, 3, 3, 3],
       [0, 3, 3, 2, 3, 3, 0],
       [0, 0, 3, 0, 3, 3, 0],
       [3, 3, 2, 3, 0, 0, 0],
       [3, 4, 3, 3, 3, 0, 0],
       [0, 0, 3, 3, 3, 3, 0],
       [0, 0, 0, 0, 0, 0, 0]]


def readmap(mymap, level):
    """从txt文件读取关卡信息"""
    loc = 'level/' + str(level) + '.txt'
    mymap.clear()
    mymap1 = numpy.loadtxt(loc, dtype=bytes).astype(int)
    for item in mymap1:
        mymap.append(list(item))
