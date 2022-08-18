from objects import Object
from pygame import mouse, draw, Rect, font, time
from math import sin, cos, atan, pi

class Ball(Object):
    def __init__(self, surface, color, number, position, solid = False, radius = 30):
        super().__init__(f"ball_{number}_{color}_{solid}",surface)
        
        self.fricCoeff = 10000
        self.mass = 1
        self.grav = 9.8

        self.color = color
        self.position = position
        self.radius = radius
        self.solid = solid
        
        self.textContent = str(number)
        textFont = font.Font(None, 23)
        self.text = textFont.render(self.textContent, True, (0,0,0))
        self.textRect = self.text.get_rect()

        self.selected = False
        self.hovered = False

        self.vx = 0
        self.vy = 0

        self.flatCollide = False
        self.sideCollide = False
    
    def drawObject(self):
        if self.selected or self.hovered:
            draw.circle(self.surface, (100,100,100), self.position, self.radius+2)

        draw.circle(self.surface, self.color, self.position, self.radius)

        if not self.solid:
            draw.circle(self.surface, (255,255,255), self.position, 5*self.radius/8)
        
        self.textRect.center = self.position
        self.surface.blit(self.text, self.textRect)

    def checkHover(self, mousePos):
        radiusToCenter = (mousePos[0]-self.position[0])**2 + (mousePos[1]-self.position[1])**2
        
        self.hovered = radiusToCenter <= self.radius**2
        return self.hovered

    def checkHoleCollision(self, coords):
        distance = self._calcDist(self.position, coords)
        if distance <= 3*self.radius/2:
            return True
        return False

    def checkBallCollision(self, ball2):
        distance = self._calcDist(self.position, ball2.position)
        if distance <= self.radius + ball2.radius:
            
            if distance < self.radius + ball2.radius:
                overlapDiff = (self.radius + ball2.radius - distance)/2
                theta = self._calcAngle(ball2)
                
                overlapDiffX = overlapDiff * sin(theta)
                overlapDiffY = overlapDiff * cos(theta)

                self.position = (self.position[0] + overlapDiffX, self.position[1] + overlapDiffY)
                ball2.position = (ball2.position[0] - overlapDiffX, ball2.position[1] - overlapDiffY)
            
            return True
            
        self._collide(ball2)
        return False
    
    def checkFlatWallCollision(self):
        if (self.position[1]+self.radius >= 697 or self.position[1]-self.radius <= 22):
            if (self.position[1]+self.radius > 697):
                self.position = (self.position[0], 697-self.radius-5)
            elif (self.position[1]-self.radius < 22):
                self.position = (self.position[0], 22+self.radius+5)

            if not self.flatCollide:
                self.flatCollide = True
                self.vy = -self.vy

            return True

        self.flatCollide = False
        return False
    
    def checkSideWallCollision(self):
        if (self.position[0]+self.radius >= 1240 or self.position[0]-self.radius <= 40):
            if (self.position[0]+self.radius > 1240):
                self.position = (1240-self.radius-5, self.position[1])
            elif (self.position[0]-self.radius < 40):
                self.position = (40+self.radius+5, self.position[1])              
            
            if not self.sideCollide:
                self.sideCollide = True
                self.vx = -self.vx                
            
            return True
        
        self.sideCollide = False
        return False

    def updatePosition(self, dt):
        if self.vx != 0:
            xSign = self.vx/abs(self.vx)
        else:
            xSign = 0
        
        if self.vy != 0:
            ySign = self.vy/abs(self.vy)
        else:
            ySign = 0

        # tanx = vy / vx
        # x = arctan(vy/vx)
        # cosx = fricAccX / fricAcc
        # sinx = fricAccY / fricAcc
        if self.vx == 0 and self.vy == 0:
            theta = 0
        elif self.vx == 0 and self.vy != 0:
            theta = pi/2
        else:
            theta = atan(abs(self.vy/self.vx))

        fricAcc = self.grav * self.fricCoeff
        fricAccX = fricAcc * cos(theta) * -xSign
        fricAccY = fricAcc * sin(theta) * -ySign

        posX = self.position[0] + self.vx*dt
        self.vx = self.vx + fricAccX*dt**2

        posY = self.position[1] + self.vy*dt
        self.vy = self.vy + fricAccY*dt**2

        self.position = (posX,posY)   


    def _calcDist(self, pos1, pos2):
        diffx = (pos1[0] - pos2[0])**2
        diffy = (pos1[1] - pos2[1])**2

        return (diffx+diffy) ** (1/2)
    
    def _calcAngle(self, ball2):
        diffX = self.position[0] - ball2.position[0]
        diffY = self.position[1] - ball2.position[1]

        if diffX == 0:
            if diffY >= 0:
                theta = pi/2
            else:
                theta = -pi/2
        else:
            theta = atan(diffY/diffX)
        
        return theta
    
    def _rotateToAxis(self, a, b, theta):
        # https://www.youtube.com/watch?v=guWIF87CmBg (8:38)
        outA = a*cos(theta) + b*sin(theta)
        outB = a*-sin(theta) + b*cos(theta)

        return outA, outB
    
    def _collide(self, ball):
        v1x = self.vx
        v1y = self.vy
        
        v2x = ball.vx
        v2y = ball.vy

        theta = self._calcAngle(ball)
        
        v1x, v1y = self._rotateToAxis(v1x, v1y, theta)
        v2x, v2y = self._rotateToAxis(v2x, v2y, theta)

        self.vy, self.vx = self._rotateToAxis(v1y, v2x, theta)
        ball.vy, ball.vx = self._rotateToAxis(v2y, v1x, theta)


        


        
