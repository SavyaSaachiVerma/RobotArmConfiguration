# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

import math
import numpy as np

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """
    #print(angle)
    #print(start, length)
    xCord = start[0] + length*math.cos(math.radians(angle))
    yCord = start[1] - length*math.sin(math.radians(angle))
    #print(xCord, yCord)
    return(xCord, yCord)
    pass

def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """

    for (start, end) in armPos:
        for (x, y, r) in obstacles:
            # finding angle between lines start,end and start, point
            lenPoint = math.sqrt((x-start[0])*(x-start[0]) + (start[1] - y)*( start[1] - y))
            lenPointEnd = math.sqrt((x-end[0])*(x-end[0]) + (end[1] - y)*(end[1] - y))
            # len1 = math.sqrt((x-start[0]-10)*(x-start[0]-10) + (start[1] - y)*(start[1] - y))
            # len2 = math.sqrt((x - start[0] + 10) * (x - start[0] + 10) + (start[1] - y) * (start[1] - y))
            # len3 = math.sqrt((x - start[0]) * (x - start[0]) + (start[1] - y - 10) * (start[1] - y - 10))
            # len4 = math.sqrt((x - start[0]) * (x - start[0]) + (start[1] - y + 10) * (start[1] - y + 10))
            #print("point:", lenPoint)
            lenSeg = math.sqrt((end[0]-start[0])*(end[0]-start[0]) + (end[1] - start[1])*(end[1] - start[1]))
            #print("seg:", lenSeg)
            dotProd = np.dot([x-start[0], start[1] - y], [end[0]-start[0], start[1] - end[1]])
            #print("dot:", dotProd)
            cosAngle = dotProd/(lenPoint*lenSeg)
            sinAngle = math.sqrt(1 - (cosAngle*cosAngle))
            minDistPointSeg = lenPoint * sinAngle
            #print("Dist", minDistPointSeg)
            if minDistPointSeg <= r:
                if lenPointEnd <= r:
                    return True
                side1 = math.sqrt(lenPointEnd*lenPointEnd - minDistPointSeg*minDistPointSeg)
                side2 = math.sqrt(lenPoint*lenPoint - minDistPointSeg*minDistPointSeg)
                lenSS = side1 + side2
                if math.fabs(lenSeg - lenSS) < 1e-6:
                #if len1 <= lenSeg or len2 <= lenSeg or len3 <= lenSeg or len4 <= lenSeg:
                    #print("TRUE")
                    return True
    return False


def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    for (x,y,r) in goals:
        distTickPoint = math.sqrt((armEnd[0] - x)*(armEnd[0] - x) + (armEnd[1] - y)*(armEnd[1] - y))
        if distTickPoint <= r:
            return True
    return False



def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.

    """
    (width,height) = window
    for (start,end) in armPos:
        if (start[0] < 0 or start[0] > width) or (start[1] < 0 or start[1] > height) or (end[0] < 0 or end[0] > width) or (end[1] < 0 or end[1] > height):
            return False
    return True