import pygame, sys, math
from pygame.locals import *
import random

pygame.init()

# set the window size and window title in pixels
size = [1080, 1080]
until = size[0]
most = int(until*4/5)
gameWindow = pygame.display.set_mode(size)
pygame.display.set_caption('Pond')

clock = pygame.time.Clock()
pi = 3.14159

# set up the colors
bright = (200, 200, 100)
darkest =(51, 102, 0)
murky = (0, 51, 0)
darkYellow = (150, 150, 44)

# Add bkg color
gameWindow.fill(murky)


class Speck : 

    def __init__(self, theX, theY) :
        self.myX = theX 
        self.myY = theY 
        self.myCoords = (self.myX, self.myY)
    
    # --- So that the specks don't leave the screen --- # 
    def wrap(self) :
        if self.myX < 0 :
            self.myX = size[0]
        elif self.myX > size[0] :
            self.myX = 0
        if self.myY < 0 :
            self.myY = size[1]
        elif self.myY > size[1] :
            self.myY = 0

    # --- Draw the specks! --- #
    def draw(self, theCoords, theColor, theRadius, theFill) :
        pygame.draw.circle(gameWindow, theColor, theCoords, theRadius, theFill) 
   
    # --- To get those good good delta-x's and delta-y's --- #
    def difference(self, m, s) :
        delta = m - s
        if delta == 0 :
            delta = 0.1
        return delta

    # --- This method is the ambient movement --- #
    def woggle(self, mouseX, mouseY, param, damp) :
        self.wrap()
        dx = self.difference(mouseX+10, self.myX)
        dy = self.difference(mouseY+10, self.myY)
        r = param 
        a_y = -5*damp 
        a_x = -5*damp                 
        v_x = 0                         
        v_y = 0  
        v_x += a_x/4 + random.randint(-50,50)/100  - 3*damp/5
        v_y += a_y/4 + random.randint(-50,50)/100 - 2*damp/5
        self.myX += int(v_x * math.cos(pi/4 + v_x) + 0.03*dy/math.sqrt(abs(dy*dy)) )         # 2*accel_x + self.myX
        self.myY += int(v_y* math.sin(pi/4 + v_y) + 0.01*dx/(math.sqrt(abs(dx*dx))) )
        return (self.myX, self.myY)

    # --- The specks don't like the cursor, but they are curious --- #
    def repel(self, mouseX, mouseY, damp) :
        dx = self.difference(mouseX+10, self.myX)           
        dy = self.difference(mouseY+10, self.myY)
        r = 80
        norm = math.sqrt((dx)**2 + (dy)**2)
        if norm== 0 :
            norm = 1
        a_y = -80/norm * damp
        a_x = -80/norm * damp
        v_x = 0
        v_y = 0
        v_x += 3.5*a_x 
        v_y += 3.5*a_y 
        if norm <= 2*r :
            self.myX += int((v_x)* math.atan(3*pi/4 + v_x) * 0.3*dy/math.sqrt(abs(dy)) )
            self.myY += int((v_y)* math.atan(pi/2 + v_y) * 0.4*dx/math.sqrt(abs(dx)) ) 
        return (self.myX, self.myY)
            
         
# ---  Keeping track of the fore-, back-, and backest-ground specks --- #
fgSpecks = list()
bkgSpecks = list()
bkgBkgSpecks = list()
for i in range(0,most) :
    s = Speck(random.randint(0,until), random.randint(0,until))
    t = Speck(random.randint(0,until), random.randint(0,until))
    u = Speck(random.randint(0,until), random.randint(0,until))
    fgSpecks.append(s)
    bkgSpecks.append(t)
    bkgBkgSpecks.append(u)

# ---  Run the game loop --- # 
while True:
    gameWindow.fill(murky)
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
    # --- Keep drawing specks! --- #
    for speck in bkgBkgSpecks :
        speck.draw(speck.woggle(mx, my, 570, 0.5), darkest, 2,2)
    for speck in bkgSpecks :
        speck.draw(speck.woggle(mx, my, 150, 0.75), darkYellow, 2,2)
    for speck in fgSpecks :
        speck.draw(speck.woggle(mx,my, 450, 1), bright, 5,4)
        speck.draw(speck.repel(mx,my,0.75), bright, 5,4)

    pygame.display.update()

    clock.tick(60)



