import sys, pygame, time, math
from enum import Enum
from threading import Thread

class Estado(Enum):
        BLOQUEADO = 1
        LIVRE = 2
        CHECADO = 3

class Button:
    def __init__(self, x, y, rect):
        self.state = Estado.LIVRE
        self.rect = rect
        self.pos = x,y
        
        self.color = 255, 255, 255

    def getPos(self):
        return self.pos
        
    def changeColor(self):
        pygame.draw.rect(screen, self.color, self.rect)
        self.state = Estado.BLOQUEADO
        #pygame.display.flip()
    def path(self, color):
        self.state = Estado.CHECADO
        pygame.draw.rect(screen, color, self.rect)

class Board:
    def __init__(self, buttons):        
        self.buttons = buttons

    def printAll(self):
        for line in self.buttons:
            for button in line:
                print(button.rect)
    
    def getButtonByPixel(self, pos):
        vet = getPosByPixel(pos)
        i = vet[0]
        j = vet [1]       
        if(i < 0 or i > 49 or j < 0 or j > 49):
            return
        return self.buttons[i][j]

    def getButtonVect(self, pos):
        i = pos[0] 
        j = pos [1] 
        if(i < 0 or i > 49 or j < 0 or j > 49):
            return 
        return self.buttons[i][j]

    def getNeighbours(self, i, j):
        but = [self.getButtonVect((i + 1,j))]
        but.append(self.getButtonVect((i - 1,j)))
        but.append(self.getButtonVect((i, j + 1)))
        but.append(self.getButtonVect((i, j - 1)))

        #but.append(self.getButtonVect((i + 1, j + 1)))
        #but.append(self.getButtonVect((i + 1, j - 1)))
        #but.append(self.getButtonVect((i - 1, j + 1)))
        #but.append(self.getButtonVect((i - 1, j - 1)))
        ret = []
        for button in but:
            if(button is not None):
                ret.append(button)
        
        return ret
        
        
        
    

pygame.init()


block_size = 15
margin = 2
fullSize = block_size + margin
gridSize = 50
width, height = 50*(fullSize), 50 * (fullSize)
size = width + block_size, height + block_size

screen = pygame.display.set_mode(size)
white = 111, 115, 120
screen.fill(white)

color = 0,0,0
buttons = []

def getPosByPixel(pos):
    linha = math.floor((pos[0] - fullSize/2)/fullSize)
    coluna = math.floor((pos[1] - fullSize/2)/fullSize)
    
    return linha,coluna

for x in range(math.floor(height/(fullSize))):
    buttons.append([])
    for y in range(math.floor(width/(fullSize))):
        rect = pygame.Rect(x*(block_size+margin) + math.ceil(fullSize/2) ,y*(block_size+margin) + math.ceil(fullSize/2), block_size, block_size)
        buttons[x].append(Button(x,y,rect))
        pygame.draw.rect(screen, color, rect)


pygame.display.flip()
ev = pygame.event.get()
board = Board(buttons)
#board.run()
board.printAll()

def pathFinder(comecos = (4,4)):
    comeco = comecos
    print(comecos)
    final = 47,47
    board.getButtonVect(comeco).path((255,0,0))
    board.getButtonVect(final).path((255,0,0))    
    atual = comeco
    #while(1):
    neight = board.getNeighbours(atual[0],atual[1])    
    for nei in neight:
        pygame.display.flip()        
        if(nei.state == Estado.LIVRE):
            pathFinder(nei.getPos())
            #nei.path((0,255,255))
        #if(nei.getPos()[0] == 30):
        #    break
    pygame.display.flip()
        
while(1):           
    # proceed events
    pygame.display.flip()
    ev = pygame.event.get()
    for event in ev:      
        #print(event)       
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                print("arrow pressed, exiting game")
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if(event.key == pygame.K_SPACE):
                print("barra de espaco")
                pathFinder()       
        if(pygame.mouse.get_pressed()[0] == 1):
            print("Mouse clicked!")  
            a = board.getButtonByPixel(event.pos)
            if(a is not None):
                a.changeColor()
           
    

