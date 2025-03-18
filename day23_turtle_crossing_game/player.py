from turtle import Turtle

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.color("black")
        self.shape("turtle")
        self.setheading(90)
        self.penup()
        self.goto(self.xcor(), -280)
        self.y_move = 10

    def move(self):
        print("move..")
        new_y = self.ycor() + self.y_move
        self.goto(self.xcor(), new_y)