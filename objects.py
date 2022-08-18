from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, name, surface):
        self.name = name
        self.surface = surface

    @abstractmethod
    def drawObject(self):
        pass

    @abstractmethod
    def checkHover(self, mousePos):
        pass

    def __str__(self):
        print(f"Object: {self.name}")
    

