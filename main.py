import pygame   
from pygame.locals import *
from window import Window
from window import States

pygame.init()

currentWindow = Window()
currentWindow.switchState(States.MENU)
prevMousePos = pygame.mouse.get_pos()

fpsClock = pygame.time.Clock()

while True:
    currMousePos = pygame.mouse.get_pos()
    if currMousePos != prevMousePos:
        currentWindow.checkHover(currMousePos)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                currentWindow.switchState(States.MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(currMousePos)
        elif event.type == pygame.QUIT:
            currentWindow.running = False
            pygame.quit()

    if currentWindow.running == False:
        break

    currentWindow.drawObjects()

    pygame.display.update()
    fpsClock.tick()

