from objects import Object
from pygame import mouse, draw, Rect, font

class Button(Object):
    def __init__(self, text, surface, position, dimensions, color = (220,220,220)):
        super().__init__(text+"_btn", surface)
        self.position = position
        self.dimensions = dimensions
        self.colour = color
        self.originalColour = color
        
        self.textContent = text
        textFont = font.Font(None, 26)
        self.text = textFont.render(self.textContent, True, (0,0,0))
        self.textRect = self.text.get_rect()
        self.textRect.center = self.position

        rectPosition = (position[0]-dimensions[0]//2, position[1]-dimensions[1]//2)
        self.rect = Rect(rectPosition, dimensions)

    def checkHover(self, mousePos):
        return self.rect.collidepoint(mousePos[0],mousePos[1])

    def drawObject(self):
        draw.rect(self.surface, self.colour, self.rect)

        self.surface.blit(self.text, self.textRect)
