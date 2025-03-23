import time
from turtle import Turtle, Screen
from player import Player
from car import Car
from scoreboard import ScoreBoard

screen = Screen()
screen.setup(600,600)
screen.bgcolor("white")
screen.title("turtle crossing game")
screen.tracer(0)



player = Player()

screen.listen()
screen.onkey(player.move, "Up")
# car = Car()

carlist = []
for i in range(0, 10):
    print("i:", i)
    carlist.append(Car())


game_is_on = True
scoreBoard = ScoreBoard()
scoreBoard.print_level()
while game_is_on:
    # time.sleep(car.move_speed)
    time.sleep(0.2)
    screen.update()
    # car.move()
    for car in carlist:
        if car.distance(player) < 10:
            game_is_on = False
            break
        car.move()

    if player.ycor() > 280:
        scoreBoard.level_up()
        player.reset_pos()
        print("reset")





screen.exitonclick()
