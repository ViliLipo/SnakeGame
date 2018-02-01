import pygame
import random
import queue
import time




class Apple:
    color = (255,8,0)
    location = pygame.Rect
    size = 20
    def draw(self, pygame, screen):
        pygame.draw.rect(screen, self.color, self.location)



class Snake:
    color = ( 8, 255, 8)
    location =  queue.Queue()
    direction = 1
    def draw( self, pygame, screen):
        que2 = queue.Queue()
        while not self.location.empty():
            loc = self.location.get()
            pygame.draw.rect(screen, self.color, loc)
            que2.put(loc)
        self.location = que2

class Map:
    sizeX = 800
    sizeY = 800
    data = ""
    def makedata(self, x, y):
        self.sizeX = x
        self.sizeY = y
        self.data = [[0 for i in range(x)] for j in range(y)]

    def checkCollision(self, rect):
        i = rect.x
        j = rect.y
        count = 0
        #print("x =" + str(i))
        #print("height = "  +str(rect.height))
        #print("width = " + str(rect.width))
        while( j < rect.y + rect.height) and (j < self.sizeY):
            #print("j = " +str(j))
            while i < rect.x + rect.width  and i < self.sizeX:
                #print("i = " + str(i))
                count = count + 1
                if self.data[j][i] == 1:
                   # print("hit")
                    return True
                i = i+ 1
            i = rect.x
            j = j +1
        #print("count = " ,str(count))
        return False

    def addRectangle(self, rect):
        i = rect.x
        j = rect.y
        while j < rect.y + rect.height and j < self.sizeY:
            while i < rect.x + rect.width  and i < self.sizeX:
                self.data[j][i] = 1
                i = i + 1
            i = rect.x
            j = j + 1

    def removeRectangle(self, rect) :
        i = rect.x
        j = rect.y
        while j < rect.y + rect.height and j < self.sizeY:
            while i < rect.x + rect.width and i < self.sizeX:
                self.data[j][i] = 0
                i = i + 1
            i = rect.x
            j = j + 1




def determineDirection(pressed, olddir):
        if pressed[pygame.K_UP] and not olddir ==2:
            return -2
        elif pressed[pygame.K_DOWN] and not olddir == -2 :
            return 2
        elif pressed[pygame.K_LEFT] and not olddir == 1 :
            return -1
        elif pressed[pygame.K_RIGHT] and not olddir == -1:
            return 1
        else :
            return olddir


def determineLocation(direction, olddir, x, y):
    if direction == -2:
        y -= 5
    if direction == 2:
        y += 5
    if direction == -1:
        x -= 5
    if direction == 1:
        x += 5
    if olddir == 1 and direction == 2:
        x -=15
        y +=15
    if olddir == 1 and direction == -2:
        x  -= 15
    if olddir == -1 and direction == 2:
        y += 15
    if olddir == -2 and direction == 1:
        x += 15
    if olddir == 2 and direction == 1:
        x += 15
        y -= 15
    if olddir == 2 and direction == -1:
        y -= 15
    if x < 0:
        x = screenSizeX() +x
    elif x > screenSizeX():
        x -= screenSizeX()
    if y < 0:
        y = screenSizeY() +y
    elif y > screenSizeY():
        y -=screenSizeY()

    return x, y

def screenSizeX():
    return 800

def screenSizeY():
    return 800


def main():
    start()

def start():
    #initializing
    pygame.init()
    screen = pygame.display.set_mode((screenSizeX(),screenSizeY()))
    pygame.display.set_caption("Le Snek")
    clock = pygame.time.Clock()
    done = False
    a = Apple()
    appleExist = False
    frametimesum =0
    avgframetime = 0
    fps = 0
    escLifted = False
    paused = False
    score = 0
    tickcount = 1;
    myfont = pygame.font.SysFont("monospace", 40)
    t1 = int( round(time.time() * 1000))
    #Creating the snek
    x  = 30
    y = 30
    direction = 1
    table = Map()
    table.makedata(screenSizeX(), screenSizeY())
    s = Snake()
    firstPiece = pygame.Rect(x,y, 5, 20)
    s.location.put(firstPiece)
    table.addRectangle(firstPiece)
    grow = 2 #2
    # main loop
    while not done :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pressed = pygame.key.get_pressed()
        # Pause functionality
        if not pressed[pygame.K_ESCAPE]:
            escLifted = True
        if pressed[pygame.K_ESCAPE] and not paused and escLifted :
            paused = True
            escLifted = False
            pausedLabel = myfont.render("Paused", 1, (255,255,255))
            pauseLabelLocX = screenSizeX() - 200
            screen.blit(pausedLabel, (pauseLabelLocX, 30))
            pygame.display.flip()
        elif pressed[pygame.K_ESCAPE] and paused and escLifted :
            paused = False
            escLifted = False
        if paused:
            time.sleep(0.2)
            continue
        # Determing the direction of the snake based on input
        olddir = direction
        direction = determineDirection(pressed, olddir)
        #print(direction)
        x , y = determineLocation(direction, olddir, x,y)
        #print(x , y)
        #print(olddir)
        rect = pygame.Rect
        if direction == 1 or direction == -1 :
            rect = pygame.Rect(x,y, 5, 20)
        else :
            rect = pygame.Rect(x,y, 20, 5)
        #pygame.draw.rect(screen, color, pygame.Rect(x,y, 20, 20))
        screen.fill((0,0,0))
        # Spawning apple
        if not appleExist:
            a.location = pygame.Rect(random.randint(20,screenSizeX()-20),
                                     random.randint(20,screenSizeY()-20), a.size, a.size)
            while table.checkCollision(a.location):
                   a.location = pygame.Rect(random.randint(20,screenSizeX()-20),
                                     random.randint(20,screenSizeY()-20), a.size, a.size)
            appleExist = True
        else:
            # Eating
            if a.location.colliderect(rect):
                grow += 4
                score = score + 10
                #print("Score = ", score)
                appleExist = False
        done = table.checkCollision(rect)
        s.location.put(rect)
        table.addRectangle(rect)
        s.draw(pygame, screen)
        a.draw(pygame, screen)
        # if we do not grow the tail is removed
        if  grow <= 0:
            toremove = s.location.get()
            table.removeRectangle(toremove)
        if grow > 0:
            grow -= 1
        # Rendering the scoretext
        scoretext = "Score: " + str(score)
        label = myfont.render(scoretext, 1, (255,255,255))
        screen.blit(label, (10, 10))
        # Measuring the frametime
        t2 = int( round(time.time() * 1000))
        frametime = t2 -t1
        frametimesum += frametime
        t1 = t2
        # Displaying fps
        if tickcount == 19:
            avgframetime = frametimesum / 20
            frametimesum = 0
            fps = int(round(1000/avgframetime))
        label2 = myfont.render(str(str(fps) + 'fps'), 1, (255,255,255))
        screen.blit(label2, (screenSizeX()-120, screenSizeY()-40))
        pygame.display.flip()
        clock.tick(60)
        if done:
            #screen.fill((0,0,0))
            fscoretext = "Final score: " + str(score)
            flabel = myfont.render(fscoretext, 1, (255,255,255))
            creditsLabel1 = myfont.render("Game by Vili Lipo 2017", 1, (255,255,255))
            creditsLabel2 = myfont.render("Uses PyGame", 1, (255,255,255))
            screen.blit(flabel,((screenSizeX()/2) -200, screenSizeY()/2))
            screen.blit(creditsLabel1, (20,screenSizeY()-200))
            screen.blit(creditsLabel2, (20,screenSizeY()-100))
            pygame.display.flip()
            time.sleep(5)
        tickcount = tickcount +1
        if tickcount == 20:
            tickcount = 0

    print('Final score = ', score)


main()
