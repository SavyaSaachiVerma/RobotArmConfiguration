
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *
import numpy as np

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    #granularity = 1
    angles = arm.getArmLimit()
    (alphaMin,alphaMax) = angles[0]
    (betaMin, betaMax) = angles[1]

    numRows = int((alphaMax - alphaMin)/granularity)
    numCols = int((betaMax - betaMin)/granularity)

    Matrix = [[SPACE_CHAR for x in range(numCols+1)] for y in range(numRows+1)]

    iniAngles = arm.getArmAngle()
    #print("angles :: ", iniAngles)
    #print(numRows,numCols)
    for i in range(numRows+1):
        for j in range(numCols+1):

            alphaAngle = alphaMin + i*granularity
            betaAngle = betaMin + j*granularity
            angleToCheck = (alphaAngle, betaAngle)
            #print(angleToCheck)
            arm.setArmAngle([alphaAngle, betaAngle])
            listArmPos = arm.getArmPos()
            (start1, end1) = listArmPos[0]
            (start2, end2) = listArmPos[1]

            if iniAngles[0] == alphaAngle and iniAngles[1] == betaAngle:
                Matrix[i][j] = START_CHAR

            elif doesArmTouchGoals(arm.getEnd(), goals) and not doesArmTouchObstacles(listArmPos, obstacles):
                Matrix[i][j] = OBJECTIVE_CHAR

            elif doesArmTouchObstacles(listArmPos, obstacles+goals) or not isArmWithinWindow(listArmPos, window):
                Matrix[i][j] = WALL_CHAR

    # for i in range(numRows + 1):
    #     for j in range(numCols + 1):
    #         print(Matrix[i][j], end="")
    #     print()

    maze = Maze(Matrix, [alphaMin, betaMin], granularity)
    return maze
