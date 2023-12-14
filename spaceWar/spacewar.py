import random
import time
import pygame

import turtle

pygame.init()
turtle.speed(0) # Set turtle speed to the fastest

enemy_image = "./resource/images/enemy.gif"
ally_image = "./resource/images/ally.gif"
fire_image = "./resource/images/fire.gif"
background_image = "./resource/images/starfield.gif"
highest_score = './resource/highest.txt'

with open(highest_score, 'r') as f:
    score = f.read()
    score = int(score)

turtle.addshape(enemy_image)
turtle.addshape(ally_image)
turtle.addshape(fire_image)
turtle.addshape(background_image)

turtle.bgcolor("black") # Set background color to black
turtle.bgpic("./resource/images/starfield.gif") #600x600
turtle.setundobuffer(1) # Saves memory
turtle.ht() # Hide turtle
turtle.tracer(0) # Turn off screen updates
turtle.title("SpaceWar") # Set title to SpaceWar

fire_sound = pygame.mixer.Sound('./resource/musics/blaster.mp3')
explosion = pygame.mixer.Sound('./resource/musics/explosive.mp3') 
leaf = pygame.mixer.Sound('./resource/musics/leaf.mp3')
explosion.set_volume(0.5)
fire_sound.set_volume(0.5)



class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0) # Set speed to 0
        self.penup() # Don't draw when moving
        self.color(color) 
        self.fd(0) # Move forward 0 pixels
        self.goto(startx, starty) # Go to startx and starty
        self.speed = 1 # Set speed to 1
    
    def move(self):
        self.fd(self.speed)
        # Check for border
        if self.xcor() > 290 :
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290 :
            self.setx(-290)
            self.rt(60)
        if self.ycor() < -290 :
            self.sety(-290)
            self.rt(60)
        if self.ycor() > 290 :
            self.sety(290)
            self.rt(60)
    
    def is_collision(self,other):
        # check collision with ally or enemy for the missile/player
        if((self.xcor() - other.xcor() <=20)) and \
        ((self.ycor() - other.ycor() <=20)) and \
        ((self.xcor() - other.xcor() >=-20)) and \
        ((self.ycor() - other.ycor() >=-20)):
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=1.2, stretch_len=1.8, outline=None)
        self.speed = 2

    def turn_left(self):
        self.lt(45) 
    def turn_right(self):
        self.rt(80)
    def accelerator(self):
        self.speed  +=1
    def decelerator(self):
        self.speed  -=1  

    
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        spriteshape = enemy_image
        Sprite.__init__(self, spriteshape , color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360)) # Set random heading between 0 and 360

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        spriteshape = ally_image
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0,360)) # Set random heading between 0 and 360
    
    def move(self):
        Sprite.move(self)
       

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        spriteshape = fire_image
        Sprite.__init__(self, spriteshape, color, startx, starty)

        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)
    
    def fire(self):
        fire_sound.play()
        if self.status == "ready":
            self.setheading(player.heading())
            self.goto(player.xcor(), player.ycor())
            self.status = "shoot"
    
    def move(self):

        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "shoot":
            self.fd(self.speed)
        # Border check
        if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0 # Frame counter

    def explode(self,startx,starty):
        self.goto(startx,starty)
        self.setheading(random.randint(0,360)) # Set random heading between 0 and 360
        self.frame = 1
    
    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, -1000)

class Game():
    def __init__(self):
        self.score = 0
        self.state = "Playing"
        self.live = 3
        self.pen = turtle.Turtle()

        
    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("White")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()


    def show_status(self):
        self.pen.undo()
        self.pen.clear()
        game.draw_border()

        msg = "Score: %s" %(self.score) 
        highest = "Highest: %s" %(score)
        life_status = "Life: %s/3" %(self.live)
        self.pen.penup()
        self.pen.goto(-290, 310)

        self.pen.write(msg, font=("Arial", 14, "normal"))
        self.pen.goto(200, 310)
        self.pen.write(life_status, font=("Arial", 14, "normal"))
        self.pen.goto(-70, 310)
        self.pen.write(highest, font=("Arial", 14, "normal"))
        self.pen.ht()







game = Game()
game.draw_border()
game.show_status()

player = Player("triangle", "white", 0, 0)
missile = Missile("triangle", "yellow", 0, 0)

# keyboard binding
turtle.onkey(player.turn_left,"Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerator,"Up")
turtle.onkey(player.decelerator,"Down")
turtle.onkey(missile.fire,"space")
turtle.listen()

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0))


enemies = []
num = 10
for i in range(num):
    enemies.append(Enemy("circle", "red", -100, 0))

num = 20
allies = []
for i in range(num):
    allies.append(Ally("square", "blue", 100, 0))



while True:
    # if q is pressed, exit the game
    turtle.update()
    time.sleep(0.02) # Pause for 0.02 seconds
    player.move()
    #enemy.move()
    missile.move()

    for enemy in enemies:
        enemy.move()
   
        # Check for collision
        if player.is_collision(enemy):
            
            #play sound
            explosion.play()            
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            #game.score -= 50
            game.live -= 1
            game.pen.clear()
            game.show_status()
            game.draw_border()

               
                
  

            
        if missile.is_collision(enemy):
            #play sound
            explosion.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready" # Reset missile
            game.score += 100
            game.show_status()
            # Do the explosion
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())
                #particle.setheading(random.randint(0,360))



    for ally in allies:
        ally.move()
        if missile.is_collision(ally):
            #play sound
            leaf.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
    
    for particle in particles:
        particle.move()

    if game.live == 0:
        game.pen.goto(-100, 0)
        game.pen.write("Game Over", font=("Arial", 14, "normal"))
        missile.speed = 0
        for enemy in enemies:
            enemy.speed = 0
        for ally in allies:
            ally.speed = 0
        player.speed = 0

        if game.score > score:
            # write score in screen
            game.pen.goto(-100, -30)
            game.pen.write("New Highest Score: %s" %(game.score), font=("Arial", 14, "normal"))
            # write score in file
            with open(highest_score, 'w') as f:
                f.write(str(game.score))
                f.close()
                score = game.score


