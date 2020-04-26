import pygame
from math import *
from random import randint
from scipy.integrate import quad

# some variables

_x = 200
_y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (_x,_y)

width = 1050
height = 600
par = 1

# some parameters you can modify
a = 800 # width of the well
hbarOverM = 1
cn = [0]
N = 20 # number of cn's we calculate
time = 0 # starting time
deltaT = 2000 # time that pass between every frame
size = 100000

#--------- colors ------------------------------------------#
black = (0,0,0)
white = (255,255,255)
yellow = (220,220,20)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#-------- functions ----------------------------------------#
# this function draw the line of a function on the screen
def drawGraph(screen, yHeight, function, deltaX, time, txt, color):
    pygame.draw.line(screen, white, (0,yHeight),(width,yHeight))
    pygame.draw.line(screen, white, (100,yHeight),(100,0))
    pygame.draw.line(screen, white, (a+100,yHeight),(a+100,0))
    n = int(width/deltaX)
    for i in range(n):
        pygame.draw.circle(screen, color, (int(deltaX*i), int(yHeight+function(deltaX*i,time))), 1, 1)
    font = pygame.font.SysFont("Liberation Serif", 20)
    text = font.render(txt, True, white)
    screen.blit(text,(20,yHeight-50))

# this is the function we decide at time 0
def f0(x):
    if x<0: return 0
    if x>a: return 0
    # here you can modify your initial function
    # if you change it the wave will probably go crazy
    # also modify the size parameter to get a height that
    # is not small but neither super-high
    return sqrt(30/(a**5))*x*(a-x)

# this calculate psi n of x
def psiN(n,x):
    return sqrt(2/a)*sin((n*pi*x)/a)

# this function find the cn's for our starting function
def cnFinder(N):
    for i in range(1,N+1):
        # quad is an integrate
        cn.append( quad(lambda x: psiN(i,x)*f0(x),0,a)[0] )
cnFinder(N)

# this calculate the probability
def f1(x,t):
    if x<100: return 0
    if x>100+a: return 0
    x-=100
    r = complex(0,0)
    for i in range(1,N+1):
        r += cn[i]*sqrt(2/a)*sin((i*pi*x)/a)*e**(complex(0,-t*((i*i*pi*pi*hbarOverM)/(2*a*a))))
    r = complex(r.real,-r.imag)*complex(r.real,r.imag)
    #print(r)
    return -size*par*r.real

# this calculate the real part of the wave function
def f2(x,t):
    if x<100: return 0
    if x>100+a: return 0
    x-=100
    r = complex(0,0)
    for i in range(N):
        r += cn[i]*sqrt(2/a)*sin((i*pi*x)/a)*e**(complex(0,-t*((i*i*pi*pi*hbarOverM)/(2*a*a))))
    return -sqrt(size*100*par)*r.real

# this calculate the imaginary part of the wave function
def f3(x,t):
    if x<100: return 0
    if x>100+a: return 0
    x-=100
    r = complex(0,0)
    for i in range(N):
        r += cn[i]*sqrt(2/a)*sin((i*pi*x)/a)*e**(complex(0,-t*((i*i*pi*pi*hbarOverM)/(2*a*a))))
    return -sqrt(size*100*par)*r.imag

# this update the game
def updateGame(screen, time):
    drawGraph(screen, 400, f1, 5.0, time, "Wave1", red)
    drawGraph(screen, 400, f2, 2.0, time, "Wave1", green)
    drawGraph(screen, 400, f3, 2.0, time, "Wave1", blue)
    font = pygame.font.SysFont("Liberation Serif", 20)
    text = font.render("Resolution: x"+str(1/par), True, white)
    screen.blit(text,(width-350,height-30))

#----------- main -------------------------------------------#
pygame.init()

screen = pygame.display.set_mode( (width, height) )
fpsClock = pygame.time.Clock()

running = True

while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                par *= 1.5
            if event.key == pygame.K_s:
                par /= 1.5

    updateGame(screen, time)
    pygame.display.update()
    time += deltaT
    fpsClock.tick(90)

pygame.quit()
