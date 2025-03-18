import time
from turtle import Turtle, Screen
from player import Player
from car_manager import CarManager

screen = Screen()
screen.setup(600,600)
screen.bgcolor("white")
screen.title("turtle crossing game")
screen.tracer(0)



player = Player()

screen.listen()
screen.onkey(player.move, "Up")
car = CarManager()

game_is_on = True

while game_is_on:
    time.sleep(car.move_speed)
    screen.update()
    car.move()


screen.exitonclick()
