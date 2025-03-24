import time
from turtle import Turtle, Screen
from player import Player
from car import Car
from scoreboard import ScoreBoard
from car_manager import CarManager

screen = Screen()
screen.setup(600,600)
screen.bgcolor("white")
screen.title("turtle crossing game")
screen.tracer(0)

player = Player()
car_manager = CarManager()

screen.listen()
screen.onkey(player.move, "Up")

carlist = []
for i in range(0, 0):
    print("i:", i)
    carlist.append(Car())

game_is_on = True
scoreBoard = ScoreBoard()
scoreBoard.print_level()

while game_is_on:
    # time.sleep(car.move_speed)
    time.sleep(0.1)
    screen.update()
    car_manager.creat_cars()
    car_manager.move_cars()

    #Detect collision with car
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            break

    #Detecct successful crossing
    if player.is_at_finish_file():
        scoreBoard.level_up()
        player.goto_start()
        car_manager.level_up()

scoreBoard.game_over()

screen.exitonclick()
