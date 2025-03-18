from turtle import Turtle
import random

colors = ["red", "yellow", "black", "green", "orange", "pink", "gray","olive", "cyan", "purple" "lime"]

class CarManager(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        xpos = random.randint(100, 290)
        ypos = random.randint(-280, 290)
        coloridx = random.randint(0, len(colors))
        self.color(colors[coloridx])
        self.penup()
        self.shapesize(1,3)
        self.goto(xpos, ypos)
        self.move_speed = 0.3

    def move(self):
        new_x = self.xcor()-10
        self.goto(new_x, self.ycor())

    def level_up(self):
        self.move_speed *= 0.9


