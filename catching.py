# 2023-01-09
# catching.py
# Hello Kitty catching game
# Emma Zhang

# setup
# while True:
import turtle
import random
import time
import pygame
from pygame import mixer

# intialize pygame
pygame.init()

# background music
mixer.music.load('fun-background-music.mp3') 
mixer.music.play(-1)

# sound effects
collectSound = pygame.mixer.Sound('collectcoin-6075.wav')
deathSound = pygame.mixer.Sound('mariodeath.mp3')
failSound = pygame.mixer.Sound('fail.mp3')

screen = turtle.Screen()
screen.tracer(0)
screen.setup(760, 750, 0, 0)
t = turtle.Turtle()
t.speed(0)
t.penup()
t.seth(0)

HELLOKITTYIMG = "hello-kitty.gif"
screen.addshape(HELLOKITTYIMG)
t.shape(HELLOKITTYIMG)
writeText = turtle.Turtle()

# set constants
BG = "hello-kitty-bg.png"
screen.bgpic(BG)
HELLOKITTYWIDTH = 70
HELLOKITTYHEIGHT = 64
HELLOKITTYSPEED = 50

BOWIMG = "bow.gif"
screen.addshape(BOWIMG)
BOWWIDTH = 45
BOWSPEED = 0.2

SCREENWIDTH = screen.window_width()
SCREENHEIGHT = screen.window_height()
GROUNDHEIGHT = -306

button = turtle.Turtle()
button1 = turtle.Turtle()

# set variables
playing = True
score = 0
lives = 3
paused = False

# define functions
def reset() :
    global lives
    global score
    global paused
    global bowX
    global bowY
    global bows
    # setup
    t.penup()
    t.seth(0)
    t.goto(0, GROUNDHEIGHT + HELLOKITTYHEIGHT / 2)
    writeText.penup()
    writeText.hideturtle()
    button.penup()
    button.hideturtle()
    button1.penup()
    button1.hideturtle()

    # create bows
    bows = []
    for x in range(3) :
        bowX = int(random.randint(int(-SCREENWIDTH / 2) + BOWWIDTH, int(SCREENWIDTH / 2) - BOWWIDTH))
        bowY = SCREENHEIGHT / 2 + random.randint(45, 200)
        bow = turtle.Turtle()
        bow.hideturtle()
        bow.penup()
        bow.shape(BOWIMG)
        bow.seth(270)
        bow.goto(bowX, bowY)
        bow.speed(random.randint(1, 6))
        bows.append(bow)

    # set variables
    score = 0
    lives = 3
    paused = False

def A() :
    if (t.xcor() > -SCREENWIDTH / 2 + (HELLOKITTYWIDTH / 2)) and lives > 0:
        t.forward(-HELLOKITTYSPEED)
def D() :
    if (t.xcor() < SCREENWIDTH / 2 - (HELLOKITTYWIDTH / 2)) and lives > 0:
        t.forward(HELLOKITTYSPEED)

def rect(width, length, colour, turtle) :
    turtle.begin_fill()
    turtle.fillcolor(colour)
    turtle.pencolor(colour)
    for i in range(2) :
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(length)
        turtle.right(90)
    turtle.end_fill()

def updateScoreAndLives() :
    writeText.clear()
    writeText.penup()
    global lives
    if lives > 0 :
        writeText.pencolor("#D0348A")
        writeText.hideturtle()
        writeText.goto(-SCREENWIDTH / 2 + SCREENWIDTH / 10, SCREENHEIGHT / 2 - SCREENHEIGHT / 10)
        writeText.write("Score: " + str(score), font=("Arial", 15, "bold"))
        writeText.goto(-SCREENWIDTH / 2 + SCREENWIDTH / 10, SCREENHEIGHT / 2 - SCREENHEIGHT / 10 - 25)
        writeText.write("Lives: " + str(lives), font=("Arial", 15, "bold"))
    else :
        writeText.goto(-130, 130)
        rect(260, 100, "#E22A64", writeText)
        writeText.goto(-120, 120)
        rect(240, 80, "#FFB7CE", writeText)
        writeText.pencolor("#E22A64")
        writeText.goto(0, 80)
        writeText.write("You got " + str(score) + " bow(s).", align="center", font=("Arial", 15, "bold"))
        writeText.goto(0, 54)
        if score < 5 :
            writeText.write("Try again!", align="center", font=("Arial", 15, "bold"))
        else :
            writeText.write("Good Job!", align="center", font=("Arial", 15, "bold"))

def buttonClick(x, y) :
    if lives < 1 :
        global paused
        paused = False
        if x > -130 and x < -5 and y < 10 and y > -40:
            button.reset()
            button1.reset()
            bow.clear()
            reset()
        elif x > 1 and x < 130 and y < 10 and y > -40 :
            screen.bye()

def makeButton() :
    global bows
    for bow in bows :
        bow.hideturtle()
        bow.clear()
    if lives < 1 :
        button.hideturtle()
        button.penup()
        button.goto(-130, 10)
        rect(125, 30, "#FFB7CE", button)
        button.goto(-69, -11)
        button.pencolor("#E22A64")
        button.write("Play Again", align='center')

        button1.hideturtle()
        button1.penup()
        button1.goto(130, 10)
        rect(-125, 30, "#FFB7CE", button1)
        button1.goto(69, -11)
        button1.pencolor("#E22A64")
        button1.write("Exit Game", align='center')

def pause() :
    global paused
    paused = True
    pausing()

def pausing() :
    if paused: screen.ontimer(pausing, 250)

# check for key pressed
screen.listen()
screen.onkeypress(A, 'a')
screen.onkeypress(D, 'd')

# start game
reset()

# main loop
while playing: 
    screen.update()
    updateScoreAndLives()
    # update bow positions
    for bow in bows :
        bow.penup()
        bowX = random.randint(int(-SCREENWIDTH / 2), int(SCREENWIDTH / 2))
        bowY = SCREENHEIGHT / 2 + random.randint(45, 200)
        bow.sety(bow.ycor() - BOWSPEED)
        bow.showturtle()
        # update scores
        if (bow.ycor() < GROUNDHEIGHT) :
            if lives > 0 :
                bow.goto(bowX, bowY)
                failSound.play()
                lives -= 1
                updateScoreAndLives()
            if lives < 1 :
                bow.clear()
                bow.hideturtle()
                makeButton()
                deathSound.play()
                pause()
                turtle.onscreenclick(buttonClick, 1)
                turtle.listen()
                bows.clear()
            else :
                bow.showturtle()
        elif (bow.ycor() < (GROUNDHEIGHT + HELLOKITTYHEIGHT)) and (abs(bow.xcor() - t.xcor()) < (HELLOKITTYWIDTH-10 + BOWWIDTH) / 2):
            bow.goto(bowX, bowY)
            score += 1
            collectSound.play()
            updateScoreAndLives()
    
screen.mainloop()