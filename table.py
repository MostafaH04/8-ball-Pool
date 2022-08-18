from objects import Object
from ball import Ball
from pygame import time, mouse, draw, Rect
from random import randint

class Table(Object):
    def __init__(self, surface, dimensions, screenSize):
        super().__init__("table", surface)
        self.dimensions = dimensions
        self.size = screenSize
        
        self.balls = self._setupBalls()

        self.dt = 0.001
        self.timeStart = None
        self.accum = 0

        self.inProgress = False
        
        self.holeLocations = []

        
    def drawObject(self):
        # draw table
        self._drawTable()

        # draw balls
        self._drawBalls()

    def checkHover(self, mousePos):
        for ball in self.balls:
            ball.checkHover(mousePos)

    def _setupBalls(self):
        ballList = []
        radius = 20
        startW = self.size[0]*3/8
        startH = self.size[1]/2

        startShootW = self.size[0]*6/8

        whiteBall = Ball(self.surface, (255,255,255), ' ', (startShootW,startH), randint(0,1), radius)
        whiteBall.vx = -500
        
        ballList.append(whiteBall)

        for i in range(5):
            for j in range(i+1):
                currBall = Ball(self.surface, (255,255,255), ' ', (startW-i*2*(radius+5),startH+j*2*(radius+5)-i*(radius+5)), randint(0,1), radius)
                ballList.append(currBall)

        return ballList

    def _drawTable(self):
        # base (green)

        left = (self.size[0]-self.dimensions[0])//2
        top = (self.size[1]-self.dimensions[1])//2
        
        width = self.dimensions[0]
        height = self.dimensions[1]

        draw.rect(self.surface, (41, 158, 41), (left,top,width,height), border_radius = 25)

        #holes
        draw.circle(self.surface, (0,0,0), (left+10, top+10), 40)
        draw.circle(self.surface, (0,0,0), (left+width//2, top+10), 40)
        draw.circle(self.surface, (0,0,0), (left+width-10, top+10), 40)
        
        draw.circle(self.surface, (0,0,0), (left+10, top+height-10), 40)
        draw.circle(self.surface, (0,0,0), (left+width//2, top+height-10), 40)
        draw.circle(self.surface, (0,0,0), (left+width-10, top+height-10), 40)

        self.holeLocations = [(left+10, top+10),(left+width//2, top+10),(left+width-10, top+10),
        (left+10, top+height-10), (left+width//2, top+height-10), (left+width-10, top+height-10)
        ]
        
        #corners 
        # top left: (40, 22)
        # bottom left: (40, 697)
        # bottom right: (1240, 697)
        # top right: (1240, 22)

    def _drawBalls(self):
        # white ball
        # stripes
        # solids

        if self.timeStart == None:
            self.timeStart = time.get_ticks()/1000

        currTime = time.get_ticks()/1000
        timeStep = currTime - self.timeStart
        if (timeStep > 0.25):
            timeStep = 0.25

        self.timeStart = currTime

        self.accum += timeStep
        
        while (self.accum >= self.dt):
            counter = 0
            for i in range(len(self.balls)):
                self.balls[i-counter].updatePosition(self.dt)

                for coords in self.holeLocations:
                    if self.balls[i-counter].checkHoleCollision(coords):
                        self.balls.pop(i)
                        counter += 1
                
                if len(self.balls) == 0:
                    break
                
                self.balls[i-counter].checkSideWallCollision()
                self.balls[i-counter].checkFlatWallCollision()
                
                for j in range(i-counter+1,len(self.balls)):
                    self.balls[i-counter].checkBallCollision(self.balls[j])

            self.accum -= self.dt                

        for ball in self.balls:
            ball.drawObject()
        
        self._checkProgress()
    
    def _checkProgress(self):
        self.inProgress = False
        for ball in self.balls:
            if ball.vx != 0 or ball.vy != 0:
                self.inProgress = True
                #return True 
        return self.inProgress
            