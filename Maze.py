import sys, pygame, time, math, heapq
from enum import Enum


RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
class Estado(Enum):
        BLOQUEADO = 1
        LIVRE = 2
        CHECADO = 3

class Button:
    def __init__(self, x, y, rect, parent = None):
        self.state = Estado.LIVRE
        self.rect = rect
        self.pos = x,y

        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        
        self.color = 255, 255, 255
    
    def __eq__(self, other):
        return self.pos == other.pos
    def __lt__(self, other):
        return self.f < other.f
    def __gt__(self, other):
        return self.f > other.f
    def __repr__(self):
      return ("{} - g:{} h: {} f: {}").format(self.pos, self.g, self.h, self.f) #f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"
    
    def getPos(self):
        return self.pos
        
    def changeColor(self, color = (255,255,255)):
        pygame.draw.rect(screen, color, self.rect)
        self.state = Estado.BLOQUEADO
        #pygame.display.flip()
    def Checar(self, color):
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
            if(button is not None and button.state == Estado.LIVRE):
                ret.append(button)
        
        return ret
        
def returnPath(curNode):
    path = []
    current = curNode
    while (current is not None):
        #print("return path ")
        path.append(current.pos)
        current.changeColor()#Checar((255, 255, 255))
        pygame.display.flip()
        current = current.parent
    return path[::-1]

def astar(maze, start, end, allow_diagonal_movement = False):
    
    #criar nodos comeco e fim
    
    startNode = start#Button(None, start.pos, start.rect, None)
    startNode.g = startNode.h = startNode.f = 0
    endNode = end#Button(None, end.pos, end.rect, None)
    endNode.g = endNode.h = endNode.f = 0
    
    #lista aberta e fechada
    openList = []
    closedList = []


    #heaofy listas e adicionar startNode
    heapq.heapify(openList)
    heapq.heappush(openList, startNode)

    #Adding Stop condition
    outerIterations = 0
    maxIteratons = (len(maze.buttons[0])*len(maze.buttons[1]) // 2)

    #que quadrados procurar
    adjacentSquares = ( (0, -1), (0, 1), (-1, 0), (1, 0),)
    #TODO se permitir diagonal AQUI
    currentNode = startNode
    # Loop until you find the end
    
    while len(openList) > 0:
        #print(openList)
        #print(len(openList))
        
        #outerIterations += 1

        if(outerIterations > maxIteratons):
            print("Muitas iteracoes")
            return returnPath(currentNode)


        #get current node
        currentNode = heapq.heappop(openList)
        closedList.append(currentNode)

        # Found the goal
        if(currentNode == endNode):
            print("currentNode == endNode")
            return returnPath(currentNode)
        
        # gerar children
        
        #children = []
        """

        for newPosition in adjacentSquares:

            #getNodePos
            nodePosition = (currentNode.pos[0] + newPosition[0], currentNode.pos[1] + newPosition[1])

            #esta dentro do maze
            #if nodePosition[0] > (len(maze.buttons) - 1) or nodePosition[0] < 0 or nodePosition[1] > (len(maze.buttons[len(maze.buttons)-1]) -1) or nodePosition[1] < 0:
            #    continue

            # Make sure walkable terrain
            if maze.getButtonVect((nodePosition[0],nodePosition[1])) is not None:
                continue

            #criar novo Node
            newNode = maze.getButtonVect((nodePosition[0], nodePosition[1]))
            newNode.parent = currentNode

            children.append(newNode)
            
        """
        
        #print(currentNode.pos)
        i = currentNode.pos[0]
        j = currentNode.pos[1]
        children = maze.getNeighbours(i, j)
        
        #print("childre = ",  children)

        #loop pelas crianças
        for child in children:
            child.Checar((0,0,255))
            pygame.display.flip()
            
            
            time.sleep(0.01)
            #child esta na lista dos "fechados"
            if(len( [closedChild for closedChild in closedList if closedChild == child] ) > 0):#n sei o q acontecew aqui
                continue
            

            #criar f,g e h
            child.g = currentNode.g + 1
            child.h = ((child.pos[0] - endNode.pos[0])**2 ) + ((child.pos[1] - endNode.pos[1])**2)
            child.f = child.g + child.h

            #child esta na lista aberta
            if len([openNode for openNode in openList if child.pos == openNode.pos and child.g > openNode.g]) > 0:
                continue

            #child.path()
            #add child to open list
            print("child: ")
            print(child)
            child.parent = currentNode
            child.Checar((0,255,0))
            heapq.heappush(openList, child)

        

    print("nao achei caminoh")
    return None

    



        
    

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

for x in range(math.floor(width/(fullSize))):
    buttons.append([])
    for y in range(math.floor(height/(fullSize))):
        rect = pygame.Rect(x*(block_size+margin) + math.ceil(fullSize/2) ,y*(block_size+margin) + math.ceil(fullSize/2), block_size, block_size)
        buttons[x].append(Button(x,y,rect))
        pygame.draw.rect(screen, color, rect)


pygame.display.flip()
ev = pygame.event.get()
board = Board(buttons)
#board.run()
#board.printAll()

def pathFinder(comecos = (40,40)):
    comeco = comecos
    print(comecos)
    final = 47,47
    board.getButtonVect(comeco).Checar((255,0,0))
    board.getButtonVect(final).Checar((255,0,0))    
    atual = comeco
    #while(1):
    neight = board.getNeighbours(atual[0],atual[1])    
    for nei in neight:
        pygame.display.flip()        
        if(nei.state == Estado.LIVRE):
            pathFinder(nei.getPos())
            nei.Checar((0,255,255))
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
                #pathFinder()       
                caminho = astar(board, board.getButtonVect((2, 2)), board.getButtonVect((47,44)))
                #for but in caminho:
                #    but.changeColor()
        if(pygame.mouse.get_pressed()[0] == 1):
            print("Mouse clicked!")  
            a = board.getButtonByPixel(event.pos)
            if(a is not None):
                a.changeColor(RED)
           
    

