# import colorgram
# colors = colorgram.extract('image.jpg', 30)
#
# rgb_colors = []
#
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     rgb_colors.append((r, g, b))
#
# print(rgb_colors)
color_list = [(245, 243, 238), (246, 242, 244), (202, 164, 110), (240, 245, 241), (236, 239, 243), (149, 75, 50), (222, 201, 136), (53, 93, 123), (170, 154, 41), (138, 31, 20), (134, 163, 184), (197, 92, 73), (47, 121, 86), (73, 43, 35), (145, 178, 149), (14, 98, 70), (232, 176, 165), (160, 142, 158), (54, 45, 50), (101, 75, 77), (183, 205, 171), (36, 60, 74), (19, 86, 89), (82, 148, 129), (147, 17, 19), (27, 68, 102), (12, 70, 64), (107, 127, 153), (176, 192, 208), (168, 99, 102)]

import random
import turtle as t
tim = t.Turtle()
tim.shape("turtle")
tim.pensize(1)
tim.penup()
tim.hideturtle()
tim.speed("fastest")
t.colormode(255)

# tim.color("black", random.choice(color_list))
# tim.begin_fill()
# tim.circle(10)
# tim.end_fill()


posy = 0
for _ in range(10):
    posx = 0
    tim.sety(posy)
    posy += 50
    for _ in range(10):


        tim.setx(posx)
        tim.dot(20, random.choice(color_list))
        posx+=50





screen = t.Screen()
screen.exitonclick()
