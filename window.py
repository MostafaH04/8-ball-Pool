from enum import Enum
from menu import Menu
from table import Table
import pygame

class States(Enum):
    MENU = 0
    SINGLEPLAYER = 1
    MULTIPLAYER = 2
    ONLINE = 3
    SETTINGS = 4

class Window():
    def __init__(self, width = 1280, height = 720):
        self.size = (width, height)
        self.root = self._createRoot()

        self.currentMenu = self._startMenu()
        self.objects = []

        self.currentState = None
        self.running = True
        self._startedGame = False

    def checkHover(self, mousePos):
        for currObject in self.objects:
            if self.currentState == States.MENU:
                pressedBtn = currObject.checkHover(mousePos)
                
                if pressedBtn == 0:
                    pass
                elif pressedBtn == 1:
                    self.switchState(States.SINGLEPLAYER)
                elif pressedBtn == 2:
                    self.switchState(States.MULTIPLAYER)
                elif pressedBtn == 3:
                    self.switchState(States.ONLINE)
                elif pressedBtn == 4:
                    self.switchState(States.SETTINGS)
                
            else:
                currObject.checkHover(mousePos)

    def drawObjects(self):
        self.root.fill((50,50,255))
        for currObject in self.objects:
            currObject.drawObject()

    def switchState(self, newState):
        if self.currentState != newState:
            self._clearObjects()
        
            if newState == States.MENU:
                self._addObject(self.currentMenu)

            elif newState == States.SINGLEPLAYER:
                self._createTable()
            
            elif newState == States.MULTIPLAYER:
                pass
            
            elif newState == States.ONLINE:
                switchState(States.MENU)
            
            elif newState == States.SETTINGS:
                pass

            # add logic for new states

            self.currentState = newState        

    def _createTable(self):
        self._clearObjects()
        self.table = Table(self.root, (15*self.size[0]/16, 15*self.size[1]/16), self.size)
        
        self._addObject(self.table)

    def _destroyTable(self):
        self.table = None

    def _removeObject(self, currObject):
        while currObject in self.objects:
            self.objects.remove(currObject)
    
    def _clearObjects(self):
        self.objects = []
        self._destroyTable()

    def _addObject(self, currObject):
        self.objects.append(currObject)

    def _startMenu(self):
        currentMenu = Menu(self.root)

        return currentMenu

    def _createRoot(self, flags = None):
        if flags:
            return pygame.display.set_mode(self.size, flags)
        else:
            return pygame.display.set_mode(self.size)