from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "bold")

class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("black")
        self.penup()
        self.hideturtle()
        self.level = 1

    def level_up(self):
        self.level += 1
        self.print_level()

    def print_level(self):
        self.clear()
        self.goto(-270, 240)
        # self.write(self.level, align="center", font=("Courier", 50, "normal"))
        self.write(f"Level : {self.level}", align="left", font=("Courier", 20, "bold"))

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", False, align=ALIGNMENT, font=FONT)
