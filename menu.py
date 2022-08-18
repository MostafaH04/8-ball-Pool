from objects import Object
from pygame import draw, event, MOUSEBUTTONDOWN
from button import Button

class Menu(Object):
    def __init__(self, surface, bgcolor = (180, 180, 180)):
        super().__init__("menu", surface)
        self.bgColour = bgcolor

        self.surfaceDimensions = self.surface.get_size()
        self.dimensions = (600, 600)
        self.buttons = self._createButtons()

    def checkHover(self, mousePos):
        hoveredBtn = None
        for i in range(len(self.buttons)):
            if self.buttons[i].checkHover(mousePos):
                self.buttons[i].colour = (250, 250, 250)
                hoveredBtn = i+1

                for currEvent in event.get():
                    if currEvent.type == MOUSEBUTTONDOWN:
                        return hoveredBtn

            else:
                self.buttons[i].colour = self.buttons[i].originalColour
        
        return 0

    def drawObject(self):
        self._drawBackground()
        self._drawButtons()
        
    def _drawBackground(self):
        centerW, centerH = self.surfaceDimensions[0]//2, self.surfaceDimensions[1]//2
        width, height = self.dimensions

        draw.rect(self.surface, self.bgColour, ((centerW - width//2, centerH - height//2), (width, height)))

    def _createButtons(self):
        buttonsArea = (self.dimensions[0]-300, self.dimensions[1]-200)
        buttonHeightSpan = buttonsArea[1]//4

        buttonDimensions = (buttonsArea[0], 4*buttonHeightSpan//5)
        spacing = (buttonHeightSpan - 4*buttonHeightSpan//5)

        centerW, top = self.surfaceDimensions[0]//2, self.surfaceDimensions[1]//2 - buttonsArea[1]//2 + 80

        #Single Player
        btnPosition = [centerW, top + (buttonDimensions[1]//2)]
        singlePlayerBtn = Button("Single Player", self.surface, btnPosition, buttonDimensions)

        #Local Multiplayer
        btnPosition[1] += buttonDimensions[1] + spacing
        localBtn = Button("Local Multiplayer", self.surface, btnPosition, buttonDimensions)

        #Coming Soon
        btnPosition[1] += buttonDimensions[1] + spacing
        multiplayerBtn = Button("Coming Soon", self.surface, btnPosition, buttonDimensions)

        #Settings
        btnPosition[1] += buttonDimensions[1] + spacing
        settingsBtn = Button("Settings", self.surface, btnPosition, buttonDimensions)

        return [singlePlayerBtn, localBtn, multiplayerBtn, settingsBtn]
    
    def _drawButtons(self):
        for button in self.buttons:
            button.drawObject()