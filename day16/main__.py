# #import turtle
# import another_module
# from turtle import Turtle, Screen
#
# print(another_module.another_variable)
#
# timmy = Turtle()
# print(timmy)
# timmy.shape("turtle")
# timmy.color("blue")
# timmy.forward(100)
#
# my_screen = Screen()
# print(my_screen.canvheight)
# my_screen.exitonclick()

from prettytable import PrettyTable
table = PrettyTable()


table.add_column("Pokemon",
["Adelaide","Brisbane","Darwin","Hobart","Sydney","Melbourne","Perth"])
table.add_column("Type",
["Adelaide1","Brisbane2","Darwin","Hobart","Sydney","Melbourne","Perth"])

table.align = "l"

print(table)