import pygame
from enum import Enum
import os, sys
from _thread import *
import threading
import time
import datetime
import random
white = (255, 255, 255)

tetrominoHeight = 40
tetrominoWidth = 40


WIDTH, HEIGHT = 600, 800
gameOn = True
seconds = 0
shapesCreating = {}
shapesCounter = 0
allowed = True
shouldCreateNewPiece = True
clearLines = 19
FPS = 60
timer = 0
score = "000000"
zeros = 5
name = ""
theNewRecord = False

with open(r"C:\Users\44749\PycharmProjects\Tetris\records.txt") as f:
    lines = f.readlines()
scores = []


def readTheLines(lines):
    global scores
    theScore = ""
    recordHolder = ""
    mode = 0
    for ind, i in enumerate(lines):
        for k in i:
            if k != ":" and mode == 0:
                theScore += k
            elif k != ":" and mode == 1:
                recordHolder += k
            elif k == ":" and mode == 0:
                scores.append([int(theScore), 0])
                theScore = ""
                mode = 1
            elif k == ":" and mode == 1:
                scores[ind][1] = recordHolder
                recordHolder = ""
                mode = 0
                break
    scores.sort()
    f.close()

readTheLines(lines)

print(scores)

pygame.init()
Display = pygame.display.set_mode((WIDTH, HEIGHT))
Syntax: pygame.display.set_caption('Tetris by Wadood Ahmed Taibek')
logo = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'logo.png')),
                                         (tetrominoWidth, tetrominoHeight))
Syntax: pygame.display.set_icon(logo)
font = pygame.font.SysFont('comiscans', 40)
fontOver = pygame.font.SysFont('comiscans', 60)
text = font.render(str(datetime.timedelta(seconds=timer)), True, (255, 255, 255))
scoreText = font.render(str(score), True,(255, 255, 255))
gameOver = fontOver.render("Game Completed", True, (66, 80, 30))
yourName = fontOver.render("Your Name:", True, (66, 80, 30))
endGame = False
scoreWord = font.render("Score: ", True, (255, 255, 255))
recordWord = font.render("Record: ", True, (255, 255, 255))
if scores:
    theRecord = font.render(str(scores[-1][0]), True, (255, 255, 255))
    theRecordHolderName = font.render(str(scores[-1][1]), True, (255, 255, 255))
timeText = font.render("Time", True, (255, 255, 255))
printTheNewRecord = fontOver.render("New Record!", True, (66, 80, 30))
beginning = time.time()



class Playfield:

    @staticmethod
    def getLandScape():
        return [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]


    def __init__(self):
        self.landscape = self.getLandScape()





    def checkForLineReduction(self):
        global clearLines, score, scoreText, zeros
        toBringDown = 0

        for i in range(0, len(self.landscape) - clearLines):
            clear = 0
            for ida, k in enumerate(self.landscape[19 - i]):
                if k == -1:
                    clear += 1
                    if clear == 10:
                        clearLines = 19 - i
                        toIncreaseBy = 1
                        score = int(score)
                        if toBringDown != 0:
                            for l in range(1, toBringDown + 1):
                                self.landscape[19 - i + l] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
                                toIncreaseBy = toIncreaseBy *l
                                score += toIncreaseBy*10
                            score = str(score)
                            zeros = 6 - len(score)
                            for i in range(1, zeros + 1):
                                score = "0" + score
                            scoreText = font.render(str(score), True, (255, 255, 255))
                            return
                if ida == len(self.landscape[i]) - 1 and clear == 0:
                    #print("The reason for removal: ")
                    #print(self.landscape[19 - i])
                    self.landscape[19 - i] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
                    toBringDown += 1
                    clearLines += 1
                elif toBringDown != 0 and ida == 9:
                    #print("Should be working on ", self.landscape[19 - i])
                    #print(self.landscape[19 - i - toBringDown])
                    self.landscape[19 - i + toBringDown] = self.landscape[19 - i]



listOfButtons = [pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'cyan_tetromino.jpg')),
                                         (tetrominoWidth, tetrominoHeight)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'yellow_tetromino.jpg')),
                                         (tetrominoWidth, tetrominoHeight)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'purple_tetromino.jpg')),
                                         (tetrominoWidth, tetrominoHeight)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'green_tetromino.jpg')),
                                         (tetrominoWidth, tetrominoHeight)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'blue_tetromino.jpg')),
                                         (tetrominoWidth, tetrominoHeight)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'red_tetromino.jpg')),
                                         (tetrominoWidth, tetrominoHeight)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'orange_tetromino.jpg')),
                                         (tetrominoWidth, tetrominoHeight))]


playfield = Playfield()


class Forms(Enum):
    Line = "line"
    L = "L"
    J = "J"
    sq = "sq"
    Z = "Z"
    k = "k"
    WASD = "WASD"


class Piece:
    instances = []

    @staticmethod
    def getShape(num: int):

        shapes = [[[4, 0], [4, 1], [4, 2], [4, 3]], [[3, 0], [3, 1], [4, 1], [5, 1]], [[5, 0], [3, 1], [4, 1], [5, 1]], [[4, 0], [5, 0], [4, 1], [5, 1]],[[4, 0], [5, 0], [4, 1], [3, 1]],[[3, 0], [4, 0], [4, 1], [5, 1]], [[4, 0], [3, 1], [4, 1], [5, 1]]]
        return shapes[num]

    def __init__(self, colour: int, shape:int):
        self.colour = colour
        self.shape = shape
        self.alive = True
        self.instances.append(self)
        self.facing = 0
        if shape == 0:
            self.coordinates = [[4, 0], [4, 1], [4, 2], [4, 3]]
            self.form = Forms.Line
        elif shape == 1:
            self.coordinates = [ [3, 0], [3, 1], [4, 1], [5, 1]]   # L
            self.form = Forms.L
        elif shape == 2:
            self.coordinates = [ [5, 0], [3, 1], [4, 1], [5, 1]]    #J
            self.form = Forms.J
        elif shape == 3:
            self.coordinates = [ [4,0], [5, 0], [4, 1], [5, 1]]
            self.form = Forms.sq
        elif shape == 4:
            self.coordinates = [ [4, 0], [5, 0], [4, 1], [3, 1]]    #ZZZZZZZZZZZZ
            self.form = Forms.k                                #ZZZZZZZZZZ
        elif shape == 5:
            self.coordinates = [[3, 0], [4, 0], [4, 1], [5, 1]]  #ZZZZZZZZ
            self.form = Forms.Z                                 #      ZZZZZZZZZ
        elif shape == 6:
            self.coordinates = [[4, 0], [3, 1], [4, 1], [5, 1]]
            self.form = Forms.WASD


def toLandscape(shape):
    global clearLines
    for i in shape.coordinates:
        if clearLines >= i[1]:
            clearLines = i[1] - 1
        playfield.landscape[i[1]][i[0]] = shape.colour


def check():
    global gameOn, playfield, endGame, shouldCreateNewPiece
    for u in playfield.landscape[0]:
        if u != -1:
            endGame = True
            shouldCreateNewPiece = False
            return
    shouldCreateNewPiece = True
    playfield.checkForLineReduction()


def controlTheShape(shape:Piece, direction:int):
    global shouldCreateNewPiece
    try:
        if shapesCreating:
            if direction == 0:
                for idx, i in enumerate(shape.coordinates):
                    if i[1] == 19 or playfield.landscape[i[1] + 1][i[0]] != -1:
                        toLandscape(shape)
                        check()
                        return
                    elif idx == 3:
                        shape.coordinates[0][1] += 1
                        shape.coordinates[1][1] += 1
                        shape.coordinates[2][1] += 1
                        shape.coordinates[3][1] += 1
            elif direction == 1:
                for i in shape.coordinates:
                    if i[0] == 0 or playfield.landscape[i[1]][i[0] - 1] != -1:
                        return
                shape.coordinates[0][0] -= 1
                shape.coordinates[1][0] -= 1
                shape.coordinates[2][0] -= 1
                shape.coordinates[3][0] -= 1
            elif direction == 2:
                for i in shape.coordinates:
                    if i[0] == 9 or playfield.landscape[i[1]][i[0] + 1] != -1:
                        return
                shape.coordinates[0][0] += 1
                shape.coordinates[1][0] += 1
                shape.coordinates[2][0] += 1
                shape.coordinates[3][0] += 1
            elif direction == 3:
                shape.coordinates.sort()
                if shape.form == Forms.WASD:
                    if shape.facing == 0 and playfield.landscape[shape.coordinates[0][1] + 1][shape.coordinates[0][0] + 1] == -1\
                        and -1 < shape.coordinates[0][0] + 1<10 and -1< shape.coordinates[0][1] + 1 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 1, shape.coordinates[0][1] + 1]
                        shape.facing = 1
                    elif shape.facing == 1 and playfield.landscape[shape.coordinates[0][1] + 1][shape.coordinates[0][0] - 1] == -1\
                        and -1 < shape.coordinates[0][0] - 1<10 and -1< shape.coordinates[0][1] + 1 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] - 1, shape.coordinates[0][1] + 1]
                        shape.facing = 2
                    elif shape.facing == 2 and playfield.landscape[shape.coordinates[-1][1] - 1][shape.coordinates[-1][0] - 1] == -1\
                        and -1 < shape.coordinates[-1][0] - 1<10 and -1< shape.coordinates[-1][1] - 1 < 20:
                        shape.coordinates[-1] = [shape.coordinates[-1][0] - 1, shape.coordinates[-1][1] - 1]
                        shape.facing = 3
                    elif shape.facing == 3 and playfield.landscape[shape.coordinates[-1][1] - 1][shape.coordinates[-1][0] + 1] == -1\
                        and -1 < shape.coordinates[-1][0] + 1<10 and -1< shape.coordinates[-1][1] - 1 < 20:
                        shape.coordinates[-1] = [shape.coordinates[-1][0] + 1, shape.coordinates[-1][1] - 1]
                        shape.facing = 0
                elif shape.form == Forms.L:
                    if shape.facing == 0 and playfield.landscape[shape.coordinates[0][1]][shape.coordinates[0][0] + 2] == -1 and  playfield.landscape[shape.coordinates[1][1] -1][shape.coordinates[1][0] + 1] == -1 and playfield.landscape[shape.coordinates[3][1] + 1][shape.coordinates[3][0] - 1] == -1\
                            and -1 < shape.coordinates[0][0] + 2 < 10 and -1 <shape.coordinates[0][1] < 20\
                            and -1 < shape.coordinates[1][0] + 1 < 10 and -1 < shape.coordinates[1][1] - 1 < 20\
                            and -1 < shape.coordinates[3][0] - 1 < 10 and -1 < shape.coordinates[3][1] + 1 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 2, shape.coordinates[0][1]]
                        shape.coordinates[1] = [shape.coordinates[1][0] + 1, shape.coordinates[1][1] - 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 1, shape.coordinates[3][1] + 1]
                        shape.facing = 1
                    elif shape.facing == 1 and playfield.landscape[shape.coordinates[0][1] + 1][shape.coordinates[0][0] + 1] == -1 and  playfield.landscape[shape.coordinates[2][1] -1][shape.coordinates[2][0] - 1] == -1 and playfield.landscape[shape.coordinates[3][1]][shape.coordinates[3][0] + 2] == -1\
                            and -1 < shape.coordinates[0][0] + 1 < 10 and -1 <  shape.coordinates[0][1] + 1 < 20\
                            and -1 < shape.coordinates[2][0] - 1 < 10 and -1 < shape.coordinates[2][1] - 1 < 20\
                            and -1 < shape.coordinates[3][0] < 10 and -1 < shape.coordinates[3][1] + 2 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 1, shape.coordinates[0][1] + 1]
                        shape.coordinates[2] = [shape.coordinates[2][0] - 1, shape.coordinates[2][1] - 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] , shape.coordinates[3][1] + 2]
                        shape.facing = 2
                    elif shape.facing == 2 and playfield.landscape[shape.coordinates[0][1] - 1][shape.coordinates[0][0] + 1] == -1 and  playfield.landscape[shape.coordinates[2][1] + 1][shape.coordinates[2][0] - 1] == -1 and playfield.landscape[shape.coordinates[3][1]][shape.coordinates[3][0] - 2] == -1\
                        and -1 < shape.coordinates[0][0] + 1< 10 and -1 <shape.coordinates[0][1] - 1 < 20\
                        and -1 < shape.coordinates[2][0] - 1< 10 and -1 <shape.coordinates[2][1] + 1 < 20\
                        and -1 < shape.coordinates[3][0] - 2< 10 and -1 < shape.coordinates[3][1] < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 1, shape.coordinates[0][1] - 1]
                        shape.coordinates[2] = [shape.coordinates[2][0] - 1, shape.coordinates[2][1] + 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 2, shape.coordinates[3][1]]
                        shape.facing = 3
                    elif shape.facing == 3 and playfield.landscape[shape.coordinates[0][1] - 2][shape.coordinates[0][0]] == -1 and  playfield.landscape[shape.coordinates[1][1] + 1][shape.coordinates[1][0] + 1] == -1 and playfield.landscape[shape.coordinates[3][1] - 1][shape.coordinates[3][0] - 1] == -1\
                        and -1 < shape.coordinates[0][0]< 10 and -1 <shape.coordinates[0][1] - 2 < 20\
                        and -1 < shape.coordinates[1][0] + 1< 10and -1 <shape.coordinates[1][1] + 1< 20\
                        and -1 < shape.coordinates[3][0] - 1< 10 and -1 < shape.coordinates[3][1] - 1< 20:
                        shape.coordinates[0] = [shape.coordinates[0][0], shape.coordinates[0][1] - 2]
                        shape.coordinates[1] = [shape.coordinates[1][0] + 1, shape.coordinates[1][1] + 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 1, shape.coordinates[3][1] - 1]
                        shape.facing = 0
                elif shape.form == Forms.J:
                    if shape.facing == 0 and playfield.landscape[shape.coordinates[0][1] - 1][shape.coordinates[0][0] + 1] == -1 and  playfield.landscape[shape.coordinates[2][1] + 2][shape.coordinates[2][0]] == -1 and playfield.landscape[shape.coordinates[3][1] + 1][shape.coordinates[3][0] - 1] == -1\
                        and -1 < shape.coordinates[0][0] + 1 < 10 and -1< shape.coordinates[0][1] - 1 < 20\
                        and -1 < shape.coordinates[2][0] < 10 and -1 < shape.coordinates[2][1] + 2 < 20\
                    and -1 < shape.coordinates[3][0] - 1 < 10 and -1<  shape.coordinates[3][1] + 1 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 1, shape.coordinates[0][1] - 1]
                        shape.coordinates[2] = [shape.coordinates[2][0]    , shape.coordinates[2][1] + 2]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 1, shape.coordinates[3][1] + 1]
                        shape.facing = 1
                    elif shape.facing == 1 and playfield.landscape[shape.coordinates[0][1] + 1][shape.coordinates[0][0] + 1] == -1 and  playfield.landscape[shape.coordinates[2][1] -1][shape.coordinates[2][0] - 1] == -1 and playfield.landscape[shape.coordinates[3][1]][shape.coordinates[3][0] - 2] == -1\
                        and -1 < shape.coordinates[0][0] + 1<10 and -1< shape.coordinates[0][1] + 1 < 20\
                        and -1 < shape.coordinates[2][0] - 1<10 and -1<  shape.coordinates[2][1] - 1 <20\
                        and -1 < shape.coordinates[3][0] - 2<10 and -1<  shape.coordinates[3][1] < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 1, shape.coordinates[0][1] + 1]
                        shape.coordinates[2] = [shape.coordinates[2][0] - 1, shape.coordinates[2][1] - 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 2, shape.coordinates[3][1]]
                        shape.facing = 2
                    elif shape.facing == 2 and playfield.landscape[shape.coordinates[0][1] - 1][shape.coordinates[0][0] + 1] == -1 and  playfield.landscape[shape.coordinates[1][1] - 2][shape.coordinates[1][0]] == -1 and playfield.landscape[shape.coordinates[3][1] + 1][shape.coordinates[3][0] - 1] == -1\
                        and -1 < shape.coordinates[0][0] + 1<10 and -1< shape.coordinates[0][1] - 1 < 20\
                        and -1 < shape.coordinates[1][0]    <10 and -1< shape.coordinates[1][1] - 2 < 20\
                        and -1 < shape.coordinates[3][0] - 1<10 and -1<  shape.coordinates[3][1] + 1 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 1, shape.coordinates[0][1] - 1]
                        shape.coordinates[1] = [shape.coordinates[1][0],     shape.coordinates[1][1] - 2]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 1, shape.coordinates[3][1] + 1]
                        shape.facing = 3
                    elif shape.facing == 3 and playfield.landscape[shape.coordinates[0][1]][shape.coordinates[0][0] + 2] == -1 and  playfield.landscape[shape.coordinates[1][1] + 1][shape.coordinates[1][0] + 1] == -1 and playfield.landscape[shape.coordinates[3][1] - 1][shape.coordinates[3][0] - 1] == -1\
                        and -1 < shape.coordinates[0][0] + 2<10 and -1<  shape.coordinates[0][1] < 20\
                        and -1 < shape.coordinates[1][0] + 1<10 and -1<  shape.coordinates[1][1] + 1 < 20\
                        and -1 < shape.coordinates[3][0] - 1<10 and -1<  shape.coordinates[3][1] - 1 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 2, shape.coordinates[0][1]]
                        shape.coordinates[1] = [shape.coordinates[1][0] + 1, shape.coordinates[1][1] + 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 1, shape.coordinates[3][1] - 1]
                        shape.facing = 0
                elif shape.form == Forms.Z:
                    if shape.facing == 0 and playfield.landscape[shape.coordinates[0][1]][shape.coordinates[0][0] + 2] == -1 and  playfield.landscape[shape.coordinates[1][1] + 1][shape.coordinates[1][0]] == -1\
                        and -1 < shape.coordinates[0][0] + 2<10 and -1< shape.coordinates[0][1] < 20\
                        and -1 < shape.coordinates[1][0]<10 and -1< shape.coordinates[1][1] + 2 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 2, shape.coordinates[0][1]]
                        shape.coordinates[1] = [shape.coordinates[1][0],     shape.coordinates[1][1] + 2]
                        shape.facing = 1
                    elif shape.facing == 1 and playfield.landscape[shape.coordinates[1][1] - 2][shape.coordinates[1][0]] == -1 and  playfield.landscape[shape.coordinates[2][1]][shape.coordinates[2][0]-2] == -1\
                        and -1 < shape.coordinates[1][0]<10 and -1<  shape.coordinates[1][1]-2 < 20\
                        and -1 < shape.coordinates[2][0] -2<10 and -1< shape.coordinates[2][1] < 20:
                        shape.coordinates[1] = [shape.coordinates[1][0], shape.coordinates[1][1]-2]
                        shape.coordinates[2] = [ shape.coordinates[2][0] -2 , shape.coordinates[2][1]]
                        shape.facing = 0
                elif shape.form == Forms.k:
                    if shape.facing == 0 and playfield.landscape[shape.coordinates[1][1] + 2][shape.coordinates[1][0] ] == -1 and  playfield.landscape[shape.coordinates[3][1]][shape.coordinates[3][0] + 1] == -1\
                        and -1 < shape.coordinates[1][0] < 10 and -1< shape.coordinates[1][1] + 2 < 20\
                        and -1 < shape.coordinates[3][0] - 2 < 10 and -1 < shape.coordinates[3][1] < 20:
                        shape.coordinates[1] = [shape.coordinates[1][0],        shape.coordinates[1][1] + 2]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 2,     shape.coordinates[3][1] ]
                        shape.facing = 1
                    elif shape.facing == 1 and playfield.landscape[shape.coordinates[0][1] + 2][shape.coordinates[0][0]] == -1 and  playfield.landscape[shape.coordinates[3][1]][shape.coordinates[3][0]-2] == -1\
                        and -1 < shape.coordinates[0][0] + 2<10 and -1< shape.coordinates[0][1] < 20\
                        and -1 < shape.coordinates[3][0]<10 and -1< shape.coordinates[3][1] -2 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 2, shape.coordinates[0][1]]
                        shape.coordinates[3] = [shape.coordinates[3][0],shape.coordinates[3][1] -2]
                        shape.facing = 0
                elif shape.form == Forms.Line:
                    if shape.facing == 0 and playfield.landscape[shape.coordinates[0][1] + 1][shape.coordinates[0][0] + 1] == -1 and  playfield.landscape[shape.coordinates[2][1] - 1][shape.coordinates[2][0] - 1] == -1 and playfield.landscape[shape.coordinates[3][1] - 2][shape.coordinates[3][0] - 2] == -1\
                        and -1 < shape.coordinates[0][0] + 1<10 and -1<  shape.coordinates[0][1] + 1 < 20\
                        and -1 < shape.coordinates[2][0] - 1<10 and -1<  shape.coordinates[2][1] - 1 < 20\
                        and -1 < shape.coordinates[3][0] - 2<10 and -1<  shape.coordinates[3][1] - 2 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 1, shape.coordinates[0][1] + 1]
                        shape.coordinates[2] = [shape.coordinates[2][0] - 1, shape.coordinates[2][1] - 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 2, shape.coordinates[3][1] - 2]
                        shape.facing = 1
                    elif shape.facing == 0 and playfield.landscape[shape.coordinates[0][1] + 1][shape.coordinates[0][0] - 1] == -1 and  playfield.landscape[shape.coordinates[2][1] - 1][shape.coordinates[2][0] + 1] == -1 and playfield.landscape[shape.coordinates[3][1] - 2][shape.coordinates[3][0] + 2] == -1\
                        and -1 < shape.coordinates[0][0] - 1<10 and -1<  shape.coordinates[0][1] + 1 < 20\
                        and -1 < shape.coordinates[2][0] + 1<10 and -1< shape.coordinates[2][1] - 1 < 20\
                        and -1 < shape.coordinates[3][0] + 2<10 and -1< shape.coordinates[3][1] - 2 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] - 1, shape.coordinates[0][1] + 1]
                        shape.coordinates[2] = [shape.coordinates[2][0] + 1, shape.coordinates[2][1] - 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] + 2, shape.coordinates[3][1] - 2]
                        shape.facing = 1
                    elif shape.facing == 1 and playfield.landscape[shape.coordinates[0][1] + 2][shape.coordinates[0][0] + 2] == -1 and  playfield.landscape[shape.coordinates[1][1] + 1][shape.coordinates[1][0] + 1] == -1 and playfield.landscape[shape.coordinates[3][1] - 1][shape.coordinates[3][0] - 1] == -1 \
                        and -1 < shape.coordinates[0][0] + 2<10 and -1<  shape.coordinates[0][1] + 2 < 20\
                        and -1 < shape.coordinates[1][0] + 1<10 and -1<  shape.coordinates[1][1] + 1 < 20\
                        and -1 < shape.coordinates[3][0] - 1<10 and -1<  shape.coordinates[3][1] - 1 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 2, shape.coordinates[0][1] + 2]
                        shape.coordinates[1] = [shape.coordinates[1][0] + 1, shape.coordinates[1][1] + 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 1, shape.coordinates[3][1] - 1]
                        shape.facing = 0
                    elif shape.facing == 1 and playfield.landscape[shape.coordinates[0][1] - 1][shape.coordinates[0][0] + 1] == -1 and  playfield.landscape[shape.coordinates[1][1] + 1][shape.coordinates[1][0] - 1] == -1 and playfield.landscape[shape.coordinates[3][1] + 2][shape.coordinates[3][0] - 2] == -1 \
                        and -1 < shape.coordinates[0][0] + 1<10 and -1<  shape.coordinates[0][1] - 1 < 20\
                        and -1 < shape.coordinates[2][0] - 1<10 and -1<  shape.coordinates[2][1] + 1 < 20\
                        and -1 < shape.coordinates[3][0] - 2<10 and -1<  shape.coordinates[3][1] + 2 < 20:
                        shape.coordinates[0] = [shape.coordinates[0][0] + 1, shape.coordinates[0][1] - 1]
                        shape.coordinates[2] = [shape.coordinates[2][0] - 1, shape.coordinates[2][1] + 1]
                        shape.coordinates[3] = [shape.coordinates[3][0] - 2, shape.coordinates[3][1] + 2]
                        shape.facing = 0
    except IndexError:
        pass



def Timing_Thread():
    global timer, text, endGame
    initially = time.time()
    waiting = 1
    theList = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    order = -1
    while allowed:
        currently = time.time()
        if not endGame:
            timer = int(currently - beginning)
            text = font.render(str(datetime.timedelta(seconds=timer)), True, (255, 255, 255))
            if shapesCreating:
                controlTheShape(shapesCreating[shapesCounter], 0)
        if currently >= initially + 60:
            if order != 8:
                order += 1
            initially = time.time()
            waiting = theList[order]
        time.sleep(waiting)


counter = 0
timeis = time.time()
timewill = 0
clock = pygame.time.Clock()
bpRight = 0
rightPressed = 0
bpLeft = 0
bpDown = 0
leftPressed = 0
downPressed = 0
chosen = [random.randint(0,6), random.randint(0,6)]


def draw_window():
    global playfield, text, scoreText, zeros, endGame
    Display.fill(white)
    pygame.draw.rect(Display, (100, 200, 100), pygame.Rect(400, 0, 200, 800))
    a = -1
    for i in playfield.landscape:
        a += 1
        b = -1
        for j in i:
            b += 1
            if j != -1:
                Display.blit(listOfButtons[j], (b*40,  a*40))
    if shapesCreating:
        for ind, i in enumerate( shapesCreating[shapesCounter].coordinates):
            Display.blit(listOfButtons[shapesCreating[shapesCounter].colour], (i[0] * 40, i[1] * 40))
            if toDrawNext:
                Display.blit(listOfButtons[chosen[0]], (320+toDrawNext[ind][0] * 40, 40 +toDrawNext[ind][1]*40))
    Display.blit(timeText, (435, 250))
    Display.blit(text, (455, 300))

    Display.blit(scoreWord, (435, 355))
    Display.blit(scoreText, (455, 400))

    Display.blit(recordWord, (435, 450))

    if theNewRecord:
        Display.blit(printTheNewRecord, (200, 200))

    if scores:
        Display.blit(theRecordHolderName, (455, 500), )
        Display.blit(theRecord, (455, 550))

    if endGame:
        nname = fontOver.render(str(name), True, (66, 80, 30))
        Display.blit(gameOver, (150, 100))
        Display.blit(yourName, (200, 400))
        Display.blit(nname, (200, 500))

    pygame.display.update()


start_new_thread(Timing_Thread, ())




while gameOn:
    clock.tick(60)
    timewill = time.time()
    counter += 1
    if timewill >= timeis + 1:
        counter = 0
        timeis = timewill
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        elif endGame:
            if not scores or int(score) > int(scores[-1][0]):
                theNewRecord = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    toInput = str(score) + ':' + name + ':' + str(timer) + '\n'
                    with open(r"C:\Users\44749\PycharmProjects\Tetris\records.txt", 'a') as f:
                        f.write(toInput)
                    f.close()
                    if score > scores[-1][0]:
                        theRecordHolderName = font.render(name, True, (255, 255, 255))
                        theRecord = score
                    scores.append([score, name])
                    scores.sort()
                    shouldCreateNewPiece = True
                    playfield = Playfield()
                    name, score = "", "000000"
                    scoreText = font.render(str(score), True, (255, 255, 255))
                    beginning = time.time()
                    endGame = False
                    theNewRecord = False
                elif event.key == pygame.K_BACKSPACE:
                    if len(name) != 0:
                        name = name[:-1]
                else:
                    name += str(event.unicode)
        else:
            if event.type == pygame.KEYDOWN:
                if shapesCreating:
                    if event.key == pygame.K_UP:
                        controlTheShape(shapesCreating[shapesCounter], 3)
    if not endGame:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            bpRight = time.time()
            if bpRight >= rightPressed + 0.1:
                rightPressed = time.time()
                controlTheShape(shapesCreating[shapesCounter], 2)
        if keys_pressed[pygame.K_LEFT]:
            bpLeft = time.time()
            if bpLeft >= leftPressed + 0.1:
                leftPressed = time.time()
                controlTheShape(shapesCreating[shapesCounter], 1)
        if keys_pressed[pygame.K_DOWN]:
            bpDown = time.time()
            if bpDown >= downPressed + 0.1:
                downPressed = time.time()
                controlTheShape(shapesCreating[shapesCounter], 0)
        if shouldCreateNewPiece:
            shapesCounter += 1
            shapesCreating[shapesCounter] = Piece(chosen[0], chosen[1])
            chosen = [random.randint(0,6), random.randint(0,6)]
            toDrawNext = Piece.getShape(chosen[1])
            shouldCreateNewPiece = False
    draw_window()