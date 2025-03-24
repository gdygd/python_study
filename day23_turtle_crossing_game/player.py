from turtle import Turtle



STARTING_POSITION = (0,-280)
FINISH_LINE_Y = 280

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.color("black")
        self.shape("turtle")
        self.setheading(90)
        self.penup()
        self.goto_start()
        self.y_move = 10

    def move(self):
        new_y = self.ycor() + self.y_move
        self.goto(self.xcor(), new_y)

    def is_at_finish_file(self):
        if self.ycor() > FINISH_LINE_Y:
            return True
        return False

    def goto_start(self):
        self.goto(STARTING_POSITION)
