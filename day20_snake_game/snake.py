from turtle import Turtle

class Snake:
    def __init__(self):
        self.segments=[]
        self.starting_position = [(0,0),(-20,0),(-40,0)]

        for n in range(0, 3):
            self.segments.append(Turtle("square"))
            self.segments[n].penup()
            self.segments[n].color("white")
            self.segments[n].goto(self.starting_position[n])

    def move(self):
        for n in range (len(self.segments)-1, 0, -1):
            self.segments[n].goto(self.segments[n - 1].xcor(), self.segments[n - 1].ycor())

        self.segments[0].forward(20)
        self.segments[0].left(90)



