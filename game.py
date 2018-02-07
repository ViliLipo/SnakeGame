import pygame
import random
import queue
import time




class Apple:
    color = (255,8,0)
    location = pygame.Rect
    size = 20
    exists = False
    def draw(self, pygame, screen):
        pygame.draw.rect(screen, self.color, self.location)

    '''
    Excecutes all of the actions required of an apple during a gametick
    '''
    def Action(self, pygame, screen , screenSizeX, screenSizeY, newRect, grow, score, table ):
        #Spawning
        if not self.exists:
            self.location = pygame.Rect(random.randint(20,screenSizeX-20),
                                     random.randint(20,screenSizeY-20), self.size, self.size)
            while table.checkCollision(self.location):
                   self.location = pygame.Rect(random.randint(20,screenSizeX -20),
                                     random.randint(20,screenSizeY -20), self.size, self.size)
            self.exists = True
        else:
            # Eating
            if self.location.colliderect(newRect):
                grow += 4
                score = score + 10
                #print("Score = ", score)
                self.exists = False
        #Rendering
        self.draw(pygame, screen)
        return grow, score

class Snake:
    color = ( 8, 255, 8)
    def __init__(self, pygame, x, y):
        self.headX = y
        self.headY = x
        self.head = pygame.Rect(x,y, 5, 20)
        self.location = queue.Queue()
        self.location.put(self.head)
        self.grow = 2 #2
        self.direction = 1
        self.oldDirection = 1
        self.directionBuffer = 1
        self.turning = 0
        self.score = 0

    def draw( self, pygame, screen):
        que2 = queue.Queue()
        while not self.location.empty():
            loc = self.location.get()
            pygame.draw.rect(screen, self.color, loc)
            que2.put(loc)
        self.location = que2

    '''
    Excecutes all of the actions required of the snake during a game tick
    '''
    def Action(self, pygame, screen, screenSizeX, screenSizeY, table, pygame_key_input, apple ):
        self.direction = self.determineDirection(pygame_key_input)
        self.headX,self.headY = self.determineLocation(self.direction, self.oldDirection, self.headX, self.headY)
        self.oldDirection = self.direction
        if self.direction == 1 or self.direction == -1 :
            self.head = pygame.Rect(self.headX,self.headY, 5, 20)
        else :
            self.head = pygame.Rect(self.headX,self.headY, 20, 5)
        self.grow, self.score = apple.Action(pygame, screen, screenSizeX, screenSizeY, self.head, self.grow, self.score, table)
        self.location.put(self.head)
        # if we do not grow the tail is removed
        if  self.grow <= 0:
            toremove = self.location.get()
            table.removeRectangle(toremove)
        if self.grow > 0:
            self.grow -= 1
        self.draw(pygame, screen)

    '''
    Determines the direction of the snake based on keyboard input and the snakes old direction
    Does not allow 180 turns
    '''
    def determineDirection(self, pressed):
        value = self.oldDirection
        if pressed[pygame.K_UP] and not self.oldDirection == 2:
            value = -2
        elif pressed[pygame.K_DOWN] and not self.oldDirection == -2 :
            value = 2
        elif pressed[pygame.K_LEFT] and not self.oldDirection == 1 :
            value = -1
        elif pressed[pygame.K_RIGHT] and not self.oldDirection == -1:
            value =  1
        if self.turning > 0:
            self.turning -= 1
            self.directionBuffer = value
            return self.oldDirection
        else:
            if value != self.oldDirection:
                self.turning = 3
            return value


    '''
    Determines the location of the snakes head based on its direction.
    Does not let the snake to eat itself during turns
    '''
    def determineLocation(self, direction, olddir, x, y):
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

'''
Datastructure where information about the snakes location is stored
for checking collision in a constant O(1) time in relation to the snakes length.

'''
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




'''
Pauser is a simple utility for allowing pause action.
Resume action needs a distinct keypress.
'''
class Pauser:
    isPaused = False
    escLifted = True
    def Action(self,pygame_key_input, screen, font, pygame):
        #print("pauser.Action")
        if not pygame_key_input[pygame.K_ESCAPE]:
            self.escLifted = True
        if pygame_key_input[pygame.K_ESCAPE] and not self.isPaused and self.escLifted :
            #print("trying to pause")
            self.isPaused = True
            self.escLifted = False
            pausedLabel = font.render("Paused", 1, (255,255,255))
            pauseLabelLocX = screenSizeX() - 200
            screen.blit(pausedLabel, (pauseLabelLocX, 30))
            pygame.display.flip()
        elif pygame_key_input[pygame.K_ESCAPE] and self.isPaused and self.escLifted :
            #print("trying to resume")
            self.isPaused = False
            self.escLifted = False
        return self.isPaused


'''
FpsCounter is a simple utility for caclulating and
rendering current fps to the game window
'''
class FpsCounter :
    tickcount = 1
    t1 = 0
    t2 = 0
    frametimesum = 0
    fps = 0
    def _init_(self):
        self.t1 = int(round(time.time() * 1000))

    def Action(self,pygame,screen, screenSizeX, screenSizeY, font ):
        # Measuring the frametime
        #print(self.tickcount)
        self.t2 = int( round(time.time() * 1000))
        frametime = self.t2 -self.t1
        #print("frametime: ", frametime)
        self.frametimesum += frametime
        self.t1 = self.t2
        # Displaying fps
        if self.tickcount >= 20:
            #print("frametimesum: ", self.frametimesum)
            avgframetime = self.frametimesum / 20
            self.frametimesum = 0
            self.fps = int(round(1000/avgframetime))
            self.tickcount = 0
        label2 = font.render(str(str(self.fps) + 'fps'), 1, (255,255,255))
        screen.blit(label2, (screenSizeX-120, screenSizeY-40))
        pygame.display.flip()
        self.tickcount += 1

def screenSizeX():
    return 800

def screenSizeY():
    return 800

def end_screen(pygame,screen, font, score):
    fscoretext = "Final score: " + str(score)
    flabel = font.render(fscoretext, 1, (255,255,255))
    creditsLabel1 = font.render("Game by Vili Lipo 2017", 1, (255,255,255))
    creditsLabel2 = font.render("runs on  PyGame, Press any key to quit", 1, (255,255,255))
    screen.blit(flabel,((screenSizeX()/2) -200, screenSizeY()/2))
    screen.blit(creditsLabel1, (20,screenSizeY()-200))
    screen.blit(creditsLabel2, (20,screenSizeY()-100))
    pygame.display.flip()
    done = False
    time.sleep(2)
    while not done:
        time.sleep(0.011)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        pressed = pygame.key.get_pressed()
        for val in pressed:
            if val == True:
                done = True

def main():
    start()

def start():
    pygame.init()
    screen = pygame.display.set_mode((screenSizeX(),screenSizeY()))
    pygame.display.set_caption("Le Snek")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 40)
    start_screen(pygame, screen, clock,  font)
    score = game(pygame, screen, clock, font)
    end_screen(pygame, screen, font, score)

def start_screen(pygame, screen, clock, font):
    message = "Press any button to start"
    label = font.render(message, 5, (255,255,255))
    screen.blit(label, (10,10))
    done = False
    pygame.display.flip()
    while not done:
        time.sleep(0.011)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        pressed = pygame.key.get_pressed()
        for val in pressed:
            if val == True:
                done = True

def game(pygame, screen, clock, font):
    #initializing
    done = False
    a = Apple()
    pauser = Pauser()
    fpsCounter = FpsCounter()
    #Creating the snek
    table = Map()
    x  = 30
    y = 30
    table.makedata(screenSizeX(), screenSizeY())
    s = Snake(pygame,x, y)
    # main loop
    while not done :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        clock.tick(60)
        pressed = pygame.key.get_pressed()
        # Pause functionality
        if pauser.Action(pygame_key_input=pressed, screen=screen, font=font, pygame=pygame):
            time.sleep(0.05)
            continue
        fpsCounter.Action(pygame, screen, screenSizeX(), screenSizeY(), font )
        screen.fill((0,0,0))
        # Spawning apple
        s.Action(pygame, screen, screenSizeX(), screenSizeY(), table, pressed, a)
        done = table.checkCollision(s.head)
        table.addRectangle(s.head)
        # Rendering the scoretext
        scoretext = "Score: " + str(s.score)
        label = font.render(scoretext, 1, (255,255,255))
        screen.blit(label, (10, 10))
    return s.score
    #print('Final score = ', s.score)


main()
