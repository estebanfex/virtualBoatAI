#  Copyright (C) 2021 Universidad Politécnica de Cataluña and Esteban Chacón
  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>


import turtle as t
import os
import numpy as np
from PIL import Image
from random import seed
from random import randint

#Images
currentDir = os.path.abspath(os.getcwd())+"/"
imageSail = "myBoat"
iSail = Image.open(currentDir + imageSail + ".gif")

imageRef = "myBoat"
iRef = Image.open(currentDir + imageRef + ".gif")

#defines
moveLeft  = 1
moveRight = 2

#constants
move_speed = 10
turn_speed = 2

sailTurn_speed = 1
sail_min_angle = 45
sail_max_angle = 135

relative_Wind_dir = 270

helmTurn_speed = 1
helm_min_angle = 45
helm_max_angle = 135

actionReward = .01
envReward    = 0.001
doneReward   = 200

class Boat():

    def __init__(self):
        self.done = 0
        self.reward = 0
 
        # Setup Background
        self.win = t.Screen()
        self.win.title('SailBoat')
        self.win.bgcolor('lightblue')
        self.win.setup(width=1300, height=1000)
        self.win.tracer(0)

        #wind
        self.wind = t.Turtle()
        self.wind.shape('arrow')
        self.wind.color('blue')
        self.wind.pensize(10)

        #Wind reference arrow
        self.windR = t.Turtle()
        self.windR.shape('arrow')
        self.windR.color('blue')
        self.windR.pensize(5)
        self.windR.penup()
        self.windR.goto(455, 400)
        self.windR.pendown()
        self.windR.right(90)
        self.windR.forward(50)

        #Sail arrow
        self.sail = t.Turtle()
        self.sail.shape('arrow')
        self.sail.color('green')
        self.sail.pensize(5)

        #Helm arrow
        self.helm = t.Turtle()
        self.helm.shape('arrow')
        self.helm.color('sienna')
        self.helm.pensize(5)

        #Destination point
        self.dst = t.Turtle()
        self.dst.shape('circle')
        self.dst.color('light slate gray')
        self.dst.pensize(5)
        
        self.resetObjectsAngles()
        self.resetEnvElements()

        # Score board
        self.score = t.Turtle()
        self.score.speed(0)
        self.score.color('black')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 420)
        self.update_score_txt()

        self.configHumanControl()

    def resetObjectsAngles(self):
        self.sailBoatAngle = randint(0,359)
        self.windAngle = randint(0,359)
        self.aparentBoatAngle = self.sailBoatAngle + relative_Wind_dir - self.windAngle
        self.sailAngle = randint(sail_min_angle,sail_max_angle)
        self.sailPrevAngle = self.sailAngle
        self.helmAngle = randint(helm_min_angle,helm_max_angle)
        
        self.dst_angle = randint(0,359) #200
        self.dst_distance = 400
    
    def resetEnvElements(self):
        #boat
        self.out = iSail.rotate(self.sailBoatAngle)
        self.out.save(currentDir + imageSail + "2.gif")
        self.win.addshape(currentDir + imageSail + "2.gif")
        self.sailBoat = t.Turtle()
        self.sailBoat.shape(currentDir + imageSail + "2.gif")

        #wind
        self.wind.penup()
        if self.windAngle > 180:
            self.wind.goto(-100,250)
        else:
            self.wind.goto(-100,-250)
        self.wind.pendown()
        self.wind.left(self.windAngle)
        self.wind.forward(100)
        
        #reference boat
        self.out = iRef.rotate(self.aparentBoatAngle)
        self.out.save(currentDir + imageRef + "3.gif")
        self.win.addshape(currentDir + imageRef + "3.gif")
        self.sailBoatR = t.Turtle()
        self.sailBoatR.shape(currentDir + imageRef + "3.gif")

        #Sail arrow
        self.sail.setheading(0)
        self.sail.penup()
        self.sail.goto(455, 200)
        self.sail.pendown()
        self.sail.right(self.sailAngle)
        self.sail.forward(65)
        
        #Helm arrow
        self.helm.setheading(0)
        self.helm.penup()
        self.helm.goto(455, 50)
        self.helm.pendown()
        self.helm.right(self.helmAngle)
        self.helm.forward(50)

        #Destination point
        self.dst.setheading(0)
        self.dst.penup()
        self.dst.goto(-120, 0)
        self.dst.pendown()
        self.dst.left(self.dst_angle)
        self.dst.forward(self.dst_distance)
        
        # Boat position
        self.sailBoat.penup()
        self.sailBoat.speed(0)
        self.sailBoat.goto(-120, 0)
        self.sailBoat.left(self.sailBoatAngle)

        # Ref Boat position
        self.sailBoatR.penup()
        self.sailBoatR.goto(450,200)
    
    def resetArrows(self):
        self.wind.undo()
        self.wind.undo()
        self.sail.undo()
        self.sail.undo()
        self.helm.undo()
        self.helm.undo()
        self.dst.undo()
        self.dst.undo()
    def update_score_txt(self):
        self.score.clear()
        self.score.write("Wind: {}  Boat: {}  Sail: {}  Helm: {}  Dest: {}km, {}°".format(self.windAngle, self.sailBoatAngle, self.sailAngle, self.helmAngle, self.dst_distance, self.dst_angle), align='center', font=('Courier', 24, 'normal'))
 
    def configHumanControl(self):
        self.win.onkey(self.sail_forward,   'Up')
        self.win.onkey(self.sail_backward,  'Down')
        self.win.onkey(self.sail_left,      'Left')
        self.win.onkey(self.sail_right,     'Right')
        self.win.onkey(self.sail_AngleUp,   'a')
        self.win.onkey(self.sail_AngleDown, 'd')
        self.win.onkey(self.helm_AngleUp,   'z')
        self.win.onkey(self.helm_AngleDown, 'c')
        self.win.listen()

 #Boat movement
    def update_angle(self):
        if self.sailBoatAngle > 359:
            self.sailBoatAngle -= 360
        elif self.sailBoatAngle < 0:
            self.sailBoatAngle +=360
            
        self.aparentBoatAngle = self.sailBoatAngle + relative_Wind_dir - self.windAngle
        if self.aparentBoatAngle > 359:
            self.aparentBoatAngle -= 360
        elif self.aparentBoatAngle < 0:
            self.aparentBoatAngle +=360
            
    def sail_image_rotation(self):
        self.update_angle()
            
        out = iSail.rotate(self.sailBoatAngle)
        out.save(currentDir + imageSail + "2.gif")
        self.win.addshape(currentDir + imageSail + "2.gif")
        self.sailBoat.shape(currentDir + imageSail + "2.gif")
        
        out = iRef.rotate(self.aparentBoatAngle)
        out.save(currentDir + imageRef + "3.gif")
        self.win.addshape(currentDir + imageRef + "3.gif")
        self.sailBoatR.shape(currentDir + imageRef + "3.gif")
    
    def sail_left(self):
        self.sailBoat.left(turn_speed)
        self.sailBoatAngle += turn_speed

        self.sail_image_rotation()
        self.update_score_txt()
            
    def sail_right(self):
        self.sailBoat.right(turn_speed)
        self.sailBoatAngle -= turn_speed
        
        self.sail_image_rotation()
        self.update_score_txt()

    def sail_forward(self):
        self.sailBoat.forward(move_speed)

    def sail_backward(self):
        self.sailBoat.backward(move_speed)

    def sail_AngleUp(self):
        self.sailAngle += sailTurn_speed
        if self.sailAngle >= sail_min_angle and self.sailAngle <= sail_max_angle:
            self.sail.clear()
            self.sail.penup()
            self.sail.goto(455, 200)
            self.sail.pendown()
            self.sail.right(sailTurn_speed)
            self.sail.forward(65)
        self.update_score_txt()
        
    def sail_AngleDown(self):
        self.sailAngle -= sailTurn_speed
        if self.sailAngle >= sail_min_angle and self.sailAngle <= sail_max_angle:
            self.sail.clear()
            self.sail.penup()
            self.sail.goto(455, 200)
            self.sail.pendown()
            self.sail.left(sailTurn_speed)
            self.sail.forward(65)
        self.update_score_txt()

    def helm_AngleUp(self):
        self.helmAngle += helmTurn_speed
        if self.helmAngle >= helm_min_angle and self.helmAngle <= helm_max_angle:
            self.helm.clear()
            self.helm.penup()
            self.helm.goto(455, 50)
            self.helm.pendown()
            self.helm.right(helmTurn_speed)
            self.helm.forward(50)
#            self.sail_right()
        elif self.helmAngle < helm_min_angle:
            self.helmAngle = helm_min_angle
        elif self.helmAngle > helm_max_angle:
            self.helmAngle = helm_max_angle
        self.update_score_txt()
        
    def helm_AngleDown(self):
        self.helmAngle -= helmTurn_speed
        if self.helmAngle >= helm_min_angle and self.helmAngle <= helm_max_angle:
            self.helm.clear()
            self.helm.penup()
            self.helm.goto(455, 50)
            self.helm.pendown()
            self.helm.left(helmTurn_speed)
            self.helm.forward(50)
#            self.sail_left()
        elif self.helmAngle < helm_min_angle:
            self.helmAngle = helm_min_angle
        elif self.helmAngle > helm_max_angle:
            self.helmAngle = helm_max_angle
        self.update_score_txt()

    def run_frame(self):

        self.win.update()

        # Policy

        if self.sailBoatAngle in range(self.dst_angle-3,self.dst_angle+3):
            self.reward += doneReward
            self.done = True
        else:
            self.reward += (360 - abs(self.sailBoatAngle - self.dst_angle))*envReward
        
    # ------------------------ AI control ------------------------

    def reset(self):
        self.resetArrows()
        self.resetObjectsAngles()
        self.resetEnvElements()
        self.update_score_txt()
        
        #give more relevance to destination angle
        state = [self.sailBoatAngle*0.01, self.helmAngle*0.01, self.dst_angle]
        return state

    def step(self, action):

        self.reward = 0
        self.done = 0

        if action == moveLeft:
            self.sail_left()
            self.helm_AngleDown()
            self.reward -= actionReward

        if action == moveRight:
            self.sail_right()
            self.helm_AngleUp()
            self.reward -= actionReward

        self.run_frame()

        #give more relevance to destination angle
        state = [self.sailBoatAngle*0.01, self.helmAngle*0.01, self.dst_angle]
        return self.reward, state, self.done


# ------------------------ Human control ------------------------
#
env = Boat()
#
while True:
    env.run_frame()


