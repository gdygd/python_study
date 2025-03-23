from turtle import Turtle
import random

# colors = ["red", "yellow", "royal blue", "green", "green yellow", "coral", "salmon","dark turquoise", "gold", "dark violet" "brown"]
colors = ["red", "yellow", "green", "blue", "orange", "purple"]

class Car(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        xpos = random.randint(100, 290)
        ypos = random.randint(-280, 290)
        coloridx = random.randint(0, len(colors)-1)
        self.color(colors[coloridx])
        self.penup()
        self.shapesize(1,3)
        self.goto(xpos, ypos)
        self.move_speed = 0.3

    def move(self):
        new_x = self.xcor() - 10
        ypos = self.ycor()
        if self.xcor() < -290:
            new_x = random.randint(100, 290)
            ypos = random.randint(-280, 290)
            coloridx = random.randint(0, len(colors) - 1)
            self.color(colors[coloridx])

        self.goto(new_x, ypos)


    def level_up(self):
        self.move_speed *= 0.9


