from turtle import Turtle, Screen
import random

screen = Screen()

screen.setup(500,400)

user_bet=screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enger a color:")
print(user_bet)

colors = ["red","orange","yellow","green","blue","purple"]

# tim = Turtle(shape="turtle")
# tim.penup()
# tim.goto(x=-230, y=-100)

is_rece_on = False

tims = []
ypos = -100
for n in range(0, 6):
    tims.append(Turtle(shape="turtle"))
    tims[n].penup()
    tims[n].color(colors[n])
    tims[n].goto(x=-230, y=ypos)
    ypos+=40

if user_bet:
    is_rece_on = True

while is_rece_on:

    for turtle in tims:
        if turtle.xcor() > 230:
            is_rece_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is winner")
            else:
                print(f"You've lost! The {winning_color} turtle is winner")


        rand_dist = random.randint(0, 10)
        turtle.forward(rand_dist)


screen.exitonclick()