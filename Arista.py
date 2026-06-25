from random import randint
#******************************************************************************
#Clase Arista
class Arista:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.id = str(source)+' -> '+str(target)

        self.weight = randint(1,50)

    def __str__(self):
        return str(self.id)

    def __lt__(self, otraArista):
        return self.weight < otraArista.weight
#******************************************************************************
