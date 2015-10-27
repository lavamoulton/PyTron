import sys, pygame
from pygame.locals import *
 
#initial variables
CLOCK = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
GRIDWIDTH = 40
GRIDHEIGHT = 40
BOXWIDTH = WINDOWWIDTH/GRIDWIDTH
BOXHEIGHT = WINDOWHEIGHT/GRIDHEIGHT
 
#color constants
BGCOLOR = (0, 0, 0)
GRIDLINECOLOR = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (192, 192, 192)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
 
def main():
        #initializes the game
        pygame.init()
        global FPSCLOCK, GRIDDISPLAY
        global GAMEFONT, BUTTONFONT, HELPFONT
        GAMEFONT = pygame.font.SysFont("monospace", 50)
        BUTTONFONT = pygame.font.SysFont("monospace", WINDOWWIDTH/20)
        HELPFONT = pygame.font.SysFont("monospace", 14)
        FPSCLOCK = pygame.time.Clock()
        GRIDDISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption("PyTron!")
        buttonList = createButtons()
 
        #creates potential players and stores them in a list
        playerList = []
       
        AI = Cycle(GRIDWIDTH-3, GRIDHEIGHT-3, "left")
        playerList.append(AI)
        Player1 = Cycle(2, 2, "right")
        playerList.append(Player1)
        Player2 = Cycle(2, GRIDHEIGHT-3, "up")
        playerList.append(Player2)
        Player3 = Cycle(GRIDWIDTH-3, 2, "down")
        playerList.append(Player3)
 
        gameStatus = "Menu"
        bStatus = False
        numPlayers = 1
 
        #create the grid array to track walls
        gameGrid = genGrid()
 
        '''main game loop'''
        while True:
                GRIDDISPLAY.fill(BGCOLOR)
                resetButtons(buttonList)
                if gameStatus == "Menu":
                        mainMenu(buttonList)
                elif gameStatus == "Help":
                        displayHelp(buttonList)
                elif gameStatus == "Playing":
                        gameGrid, bStatus = playGame(gameGrid, playerList, numPlayers)
                elif gameStatus == "Paused":
                        pauseGame(buttonList)
 
                #check events
                for event in pygame.event.get():
                        if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                        elif event.type == MOUSEBUTTONDOWN:
                                posX, posY = event.pos
                                for button in buttonList:
                                        if button.checkClick(posX, posY):
                                                if button.info == "Help":
                                                        gameStatus = "Help"
                                                elif button.info == "1":
                                                        numPlayers = 1
                                                        gameStatus = "Playing"
                                                elif button.info == "2":
                                                        numPlayers = 2
                                                        gameStatus = "Playing"
                                                elif button.info == "3":
                                                        numPlayers = 3
                                                        gameStatus = "Playing"
                                                elif button.info == "Back":
                                                        gameStatus = "Menu"
                                                elif button.info == "Continue":
                                                        gameStatus = "Playing"
                                                elif button.info == "Reset":
                                                        gameGrid, playerList = resetGame(gameGrid, playerList)
                                                        gameStatus = "Menu"
                                                        bStatus = False
                                                        
                        elif event.type == KEYDOWN and gameStatus == "Playing":
                                if event.key == K_UP:
                                        Player1.setDirection('up')
                                elif event.key == K_DOWN:
                                        Player1.setDirection('down')
                                elif event.key == K_RIGHT:
                                        Player1.setDirection('right')
                                elif event.key == K_LEFT:
                                        Player1.setDirection('left')
                                elif event.key == K_SPACE:
                                        gameStatus = "Paused"
                                        
                pygame.display.update()
                if bStatus:
                        pygame.time.wait(3000)
                        gameStatus = "Paused"
                FPSCLOCK.tick(CLOCK)
 
'''-------------------------------------
classes and methods for handling the cycles'''
 
class Cycle(object):
        '''Represents a cycle within the game'''
        def __init__(self, posX, posY, direction):
                self.posX = posX
                self.posY = posY
                self.direction = direction
                self.dead = False
 
        '''draws a simple rectangle for the cycle'''
        def drawCycle(self):
                if not self.dead:
                        pygame.draw.rect(GRIDDISPLAY, BLUE, ((self.posX*BOXWIDTH+1), (self.posY*BOXHEIGHT+1), (BOXWIDTH-1), (BOXHEIGHT-1)))
 
        '''creates the wall behind the cycle and updates the position depending on the direction it is traveling'''
        def updateCycle(self, grid):
                if not self.dead:
                        #adds a wall to the previous location of the cycle
                        grid[self.posX][self.posY] = True
               
                        #moves the cycle by one unit
                        if self.direction == "right":
                                self.posX = self.posX+1
                        elif self.direction == "left":
                                self.posX = self.posX-1
                        elif self.direction == "up":
                                self.posY = self.posY-1
                        elif self.direction == "down":
                                self.posY = self.posY+1
 
                return grid
 
        '''sets the direction the cycle is going, cannot do a 180'''
        def setDirection(self, direction):
                if direction == 'up' and self.direction != 'down':
                        self.direction = direction
                elif direction == 'down' and self.direction != 'up':
                        self.direction = direction
                elif direction == 'right' and self.direction != 'left':
                        self.direction = direction
                elif direction == 'left' and self.direction != 'right':
                        self.direction = direction
 
        '''checks if a cycle hits the perimeter or a wall'''
        def checkCollision(self, grid):
                if self.posX < 1 or self.posX > GRIDWIDTH - 2:
                        self.killCycle(grid)
                elif self.posY < 1 or self.posY > GRIDHEIGHT - 2:
                        self.killCycle(grid)
                elif grid[self.posX][self.posY]:
                        self.killCycle(grid)
 
        '''sets the cycle to dead and destroys the surrounding walls'''
        def killCycle(self, grid):
                self.dead = True
                self.killWalls(grid)
 
        def reviveCycle(self):
                self.dead = False
 
        '''displays a game over message if the cycle in question is dead'''
        def isDead(self):
                if self.dead:
                        deadText = GAMEFONT.render("Game Over!", 1, (255, 255, 255))
                        centerText = deadText.get_rect()
                        centerText.centerx = GRIDDISPLAY.get_rect().centerx
                        centerText.centery = GRIDDISPLAY.get_rect().centery
                        GRIDDISPLAY.blit(deadText, centerText)
                        return True
                return False
 
        '''destroys all adjacent walls to the cycle when it dies'''
        def killWalls(self, grid):
                if self.posX != GRIDWIDTH-1:
                        grid[self.posX+1][self.posY] = False
                grid[self.posX-1][self.posY] = False
                if self.posY != GRIDHEIGHT-1:
                        grid[self.posX][self.posY+1] = False
                grid[self.posX][self.posY-1] = False
                grid[self.posX][self.posY] = False
 
        def resetPos(self, posX, posY, direction):
                self.posX = posX
                self.posY = posY
                self.direction = direction
               
'''--------------------------------------'''
 
'''--------------------------------------
Methods for creating and handling the grid itself'''
 
def drawGrid():
        '''draws a number of GRIDLINECOLOR lines based on window and grid dimensions'''
        for x in range(0, WINDOWWIDTH, BOXWIDTH):
                for y in range(0, WINDOWHEIGHT, BOXHEIGHT):
                        pygame.draw.line(GRIDDISPLAY, GRIDLINECOLOR, (x, 0), (x, WINDOWHEIGHT))
                        pygame.draw.line(GRIDDISPLAY, GRIDLINECOLOR, (0, y), (WINDOWWIDTH, y))
 
def genGrid():
        '''creates a 2D array representing the grid in the game to keep track of walls'''
        grid = []
        for x in range(0, GRIDWIDTH):
                grid.append([])
                for y in range (0, GRIDHEIGHT):
                        grid[x].append(False)
 
        return grid
 
def updateGrid(grid):
        '''draws the updated grid with all walls, and a border of gray as a boundary wall'''
        for x in range(0, GRIDWIDTH):
                for y in range (0, GRIDHEIGHT):
                        if x==0 or x==GRIDWIDTH-1 or y==0 or y==GRIDHEIGHT-1:
                                pygame.draw.rect(GRIDDISPLAY, GRAY, ((x*BOXWIDTH+1), (y*BOXHEIGHT+1), BOXWIDTH-1, BOXHEIGHT-1))
                        elif grid[x][y] == True:
                                pygame.draw.rect(GRIDDISPLAY, RED, ((x*BOXWIDTH+1), (y*BOXHEIGHT+1), BOXWIDTH-1, BOXHEIGHT-1))
'''---------------------------------------'''
'''---------------------------------------
Gameplay methods'''
 
def playGame(gameGrid, playerList, numPlayers):
       #creates background and gridlines
        GRIDDISPLAY.fill(BGCOLOR)
        drawGrid()
 
        #update game objects
        updateGrid(gameGrid)
        if numPlayers == 1:
                for cycle in playerList[0:2]:
                        cycle.drawCycle()
                        gameGrid = cycle.updateCycle(gameGrid)
                        cycle.checkCollision(gameGrid)
                        status = cycle.isDead()
                        if status:
                                break
        else:
                for cycle in playerList[1:numPlayers+1]:
                        cycle.drawCycle()
                        gameGrid = cycle.updateCycle(gameGrid)
                        cycle.checkCollision(gameGrid)
                        status = cycle.isDead()
                        if status:
                                break
 
        return gameGrid, status
 
def resetGame(gameGrid, playerList):
        gameGrid = genGrid()
        playerList[0].resetPos(GRIDWIDTH-3, GRIDHEIGHT-3, "left")
        playerList[1].resetPos(2, 2, "right")
        playerList[2].resetPos(2, GRIDHEIGHT-3, "up")
        playerList[3].resetPos(GRIDWIDTH-3, 2, "down")
 
        for cycle in playerList:
                cycle.reviveCycle()
 
        return gameGrid, playerList
 
def pauseGame(buttonList):
        pauseText = GAMEFONT.render("Paused", 1, WHITE)
        centerText = pauseText.get_rect()
        centerText.centerx = GRIDDISPLAY.get_rect().centerx
        centerText.centery = WINDOWHEIGHT * .25
        GRIDDISPLAY.blit(pauseText, centerText)
 
        for button in buttonList:
                if button.info == "Continue" or button.info == "Reset":
                        button.draw()
                        button.setClick()

def createPlayers(numPlayers):
        for i in range(0, numPlayers):
                Player1 = Cycle(2, 2, "right")
                playerList.append(Player1)
       
'''---------------------------------------'''
 
'''---------------------------------------
Button class and methods'''
class Button(object):
        '''creates initial button with the rect object and text stored'''
        def __init__(self, inRect, text, color):
                self.buttonRect = inRect
                self.buttonFont = BUTTONFONT.render(text, 1, WHITE)
                self.color = color
                self.info = text
                self.centerText = self.buttonFont.get_rect()
                self.centerText.centerx = self.buttonRect.centerx
                self.centerText.centery = self.buttonRect.centery
                self.click = False
 
        '''draws the outline and text of the button'''
        def draw(self):
                pygame.draw.rect(GRIDDISPLAY, self.color, self.buttonRect, 2)
                GRIDDISPLAY.blit(self.buttonFont, self.centerText)
 
        '''checks if a click is within the bounds of the button drawing'''
        def checkClick(self, posX, posY):
                if self.click:
                        if posX > self.buttonRect.left and posX < self.buttonRect.right:
                                if posY > self.buttonRect.top and posY < self.buttonRect.bottom:
                                        return True
                return False

        def resetClick(self):
                self.click = False

        def setClick(self):
                self.click = True

def resetButtons(buttonList):
        for button in buttonList:
                button.resetClick()
               
'''---------------------------------------'''
 
'''---------------------------------------
Main Menu and Help Menu methods'''
def mainMenu(buttonList):
        drawMenuText()
       
        for button in buttonList:
                if button.info != "Back" and button.info != "Continue" and button.info != "Reset":
                        button.draw()
                        button.setClick()
               
'''draws the text present in the main menu, besides the buttons'''
def drawMenuText():
        MENUFONT = GAMEFONT.render("PyTron!", 1, WHITE)
        centerText = MENUFONT.get_rect()
        centerText.centerx = GRIDDISPLAY.get_rect().centerx
        GRIDDISPLAY.blit(MENUFONT, centerText)
 
        PVP = GAMEFONT.render("Number of Players:", 1, WHITE)
        centerText = PVP.get_rect()
        centerText.centerx = GRIDDISPLAY.get_rect().centerx
        centerText.centery = WINDOWHEIGHT * 0.25
        GRIDDISPLAY.blit(PVP, centerText)
 
'''creates 4 buttons: help, 1 players, 2 players, and 3 players and returns them in a list'''
def createButtons():
        buttonList = []

        TESTFONT = GAMEFONT.render("test", 1, WHITE)       
        centerText = TESTFONT.get_rect()
        centerText.centery = WINDOWHEIGHT * 0.75
        centerText.width = WINDOWWIDTH * .5
        centerText.centerx = WINDOWWIDTH * .5
        helpButton = Button(centerText, "Help", GRAY)
        buttonList.append(helpButton)
 
        centerText = pygame.Rect.copy(centerText)
        centerText.left = WINDOWWIDTH*.27
        centerText.width = WINDOWWIDTH*.12
        centerText.top = WINDOWHEIGHT*.5
        centerText.height = WINDOWHEIGHT*.1
        oneButton = Button(centerText, "1", GRAY)
        buttonList.append(oneButton)
 
        centerText = pygame.Rect.copy(centerText)
        centerText.left = WINDOWWIDTH*.44
        twoButton = Button(centerText, "2", GRAY)
        buttonList.append(twoButton)
 
        centerText = pygame.Rect.copy(centerText)
        centerText.left = WINDOWWIDTH*.6
        threeButton = Button(centerText, "3", GRAY)
        buttonList.append(threeButton)
 
        centerText = pygame.Rect.copy(centerText)
        centerText.width = WINDOWWIDTH * .25
        centerText.centerx = GRIDDISPLAY.get_rect().centerx
        centerText.centery = WINDOWHEIGHT * .8
        backButton = Button(centerText, "Back", GRAY)
        buttonList.append(backButton)
 
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = WINDOWHEIGHT*.75
        centerText.centerx = WINDOWWIDTH*.5
        pauseButton = Button(centerText, "Continue", GRAY)
        buttonList.append(pauseButton)
 
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = WINDOWHEIGHT*.88
        centerText.centerx = WINDOWWIDTH*.5
        resetButton = Button(centerText, "Reset", GRAY)
        buttonList.append(resetButton)
        return buttonList
 
'''displays a help menu with the controls for the potential 3 players and a back button to go to the main menu'''
def displayHelp(buttonList):
        p1Font = HELPFONT.render("Player 1 Controls:", 1, WHITE)
        p1Left = HELPFONT.render("Left: Left Arrow Key", 1, WHITE)
        p1Right = HELPFONT.render("Right: Right Arrow Key", 1, WHITE)
        p1Up = HELPFONT.render("Up: Up Arrow Key", 1, WHITE)
        p1Down = HELPFONT.render("Down: Down Arrow Key", 1, WHITE)
 
        centerText = p1Font.get_rect()
        centerText.centerx = WINDOWWIDTH * .2
        centerText.centery = WINDOWHEIGHT * .1
        GRIDDISPLAY.blit(p1Font, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.15)
        GRIDDISPLAY.blit(p1Left, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p1Right, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p1Up, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p1Down, centerText)
 
        p2Font = HELPFONT.render("Player 2 Controls:", 1, WHITE)
        p2Left = HELPFONT.render("Left: A", 1, WHITE)
        p2Right = HELPFONT.render("Right: D", 1, WHITE)
        p2Up = HELPFONT.render("Up: W", 1, WHITE)
        p2Down = HELPFONT.render("Down: S", 1, WHITE)
 
        centerText = pygame.Rect.copy(centerText)
        centerText = p2Font.get_rect()
        centerText.centerx = WINDOWWIDTH * .5
        centerText.centery = WINDOWHEIGHT * .1
        GRIDDISPLAY.blit(p2Font, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.15)
        GRIDDISPLAY.blit(p2Left, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p2Right, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p2Up, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p2Down, centerText)
 
        pygame.draw.line(GRIDDISPLAY, WHITE, (centerText.left-10, WINDOWHEIGHT*.08), (centerText.left-10, WINDOWHEIGHT*.60))
        pygame.draw.line(GRIDDISPLAY, WHITE, (WINDOWWIDTH*.66, WINDOWHEIGHT*.08), (WINDOWWIDTH*.66, WINDOWHEIGHT*.60))
 
        p3Font = HELPFONT.render("Player 3 Controls:", 1, WHITE)
        p3Left = HELPFONT.render("Left: J", 1, WHITE)
        p3Right = HELPFONT.render("Right: L", 1, WHITE)
        p3Up = HELPFONT.render("Up: I", 1, WHITE)
        p3Down = HELPFONT.render("Down: K", 1, WHITE)
 
        centerText = pygame.Rect.copy(centerText)
        centerText = p3Font.get_rect()
        centerText.centerx = WINDOWWIDTH * .8
        centerText.centery = WINDOWHEIGHT * .1
        GRIDDISPLAY.blit(p3Font, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.15)
        GRIDDISPLAY.blit(p3Left, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p3Right, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p3Up, centerText)
        centerText = pygame.Rect.copy(centerText)
        centerText.centery = centerText.centery+(WINDOWHEIGHT*.1)
        GRIDDISPLAY.blit(p3Down, centerText)
 
        for button in buttonList:
                if button.info == "Back":
                        button.draw()
                        button.setClick()
 
'''----------------------------------------'''
 
main()
