# from turtle import Turtle, Screen
#
# tim = Turtle()
#
# tim.shape("turtle")
# tim.color("red")
#
# for _ in range(4):
#     tim.forward(100)
#     tim.left(90)
#
#
#
# screen = Screen()
# screen.exitonclick()
import random
import turtle as t
tim = t.Turtle()
tim.shape("turtle")
tim.color("red")
tim.pensize(1)
tim.speed("fastest")
t.colormode(255)

colors = ["dark cyan", "red", "blue", "green", "yellow", "peru", "orange red", "salmon"]

def random_color():
    r = random.randint(0,255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # tim.color((r, g, b))
    return (r, g, b)


def direction():
    dir = [0,90,180,270]
    return random.choice(dir)

# for _ in range(100):
#     ang = direction()
#     tim.color(random_color())
#
#     tim.forward(30)
#     tim.setheading(ang)

for _ in range(100):
    tim.color(random_color())
    tim.circle(100)
    tim.left(3.6)





screen = t.Screen()
screen.exitonclick()