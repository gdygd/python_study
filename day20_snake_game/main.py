from turtle import Turtle, Screen
import time
from snake import Snake

screen = Screen()
screen.setup(600,600)
screen.bgcolor("black")
screen.title("My Snake Game")

starting_position = [(0,0),(-20,0),(-40,0)]

snakes = []

screen.tracer(0)

snake = Snake()


game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(0.1)

    snake.move()











screen.exitonclick()