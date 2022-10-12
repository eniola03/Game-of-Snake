#Creating this game to launch during lectures and tutorials, The game of Snake. (whilst simultaneously learning)
import pygame
import random
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) #the grid system

    def draw(self, surface, eyes=False):
        dist = self.w // self.rows #the distance of each cube from snake body
        i = self.pos[0] 
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dist + 1, j*dist + 1, dist - 2, dist - 2)) #protects the border so it draws 
        #inside the border 
        if eyes: #creating the eyes of the snake
            centre = dist//2 
            radius = 3 #radius of the eye
            eye_Middle = (i*dist + centre - radius, j * dist + 8)
            eye_Middle2 = (i*dist + dist - radius * 2, j * dist + 8)
            pygame.draw.circle(surface, (0,0,0), eye_Middle, radius)
            pygame.draw.circle(surface, (0,0,0), eye_Middle2, radius)



class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head) #how the body grows
        self.dirnx = 0
        self.dirny = 1 #a direction for x and a direction for y

    def move(self): #how we will track movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys: #will tell us whether a key was clicked or not 
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0 #so we dont move in two directions
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] 
                    #creates a dictionary that records position ansd what direction we turned
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0 
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1 
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
                #what this loop does is get the idx, and cube object 
                    #and for each pos were going to see if the pos is in our turn dict
                    #and if were on our last cube were going to remove it or else we'd change directions

            else:
                if c.dirnx == - 1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])

                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])

                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)

                elif c.dirny == - 1 and c.pos[1] <= 0:
                    c.pos = ( c.pos[0], c.rows - 1)

                else:
                    c.move(c.dirnx, c.dirny) 
            #what this does is check if we've hit the border/edge of the game and if we have it moves us a space into the game
            #and if were not were simply  moving
        

    def reset(self, pos): #this helps reset game for when one loses
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self): #where the consumption of the snack will add to the body, via the tail
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        #the if statements checks what direction the tail of the snake is moving in
        #so what it does is that if we move right after eating a cube it adds to the appropriate location in our snake body

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):#this adds eyes to the head of the body so you know what direction the snake is essentially going in
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawsGrid(w, rows, surface):
    #we want to create a grid and determine how big we want each square of the grid
    size_between = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) #draws vertical line
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y)) #draws horizontal line

def drawsWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawsGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, items):
    #generating the random snacks to grow the body
    positions = items.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), positions))) > 0: 
            #this prevents the snack from spawning on top of the snake body
            continue 
        else:
            break

    return (x,y)

def message_box(subject, content): #creates a msgbox on top of the screen, important!
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
    

def main():
    global width, rows, s, snack
    width = 500
    rows = 20 #must divide 500 evenly these are the columns
    win = pygame.display.set_mode((width, width)) #this sets the surface of the game
    s = snake((255, 0,0), (10,10)) #this is the colour (red, green, blue) we selected red and a starting position
    #mainloop
    snack = cube(randomSnack(rows, s), color=(0,255, 0)) #nts: cyan color code
    flag = True

    clock = pygame.time.Clock() #provides that we dont move faster than 10 frames per sec

    while flag:
        pygame.time.delay(50) # controls how fast as the number goes lower
        clock.tick(10) #controls how slow as the number goes lower
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('Unfortunately You Lost.', 'Play Again If You Dare...')
                s.reset((10,10))
                break

        drawsWindow(win)



main()