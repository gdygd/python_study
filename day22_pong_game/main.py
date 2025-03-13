from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
import time

screen = Screen()
screen.setup(800,600)
screen.bgcolor("black")
screen.title("My Pong Game")

screen.tracer(0)

r_paddle = Paddle(350,0)
l_paddle = Paddle(-350,0)
ball = Ball()

screen.listen()
screen.onkey(r_paddle.go_up,"Up")
screen.onkey(r_paddle.go_down,"Down")
screen.onkey(l_paddle.go_up,"w")
screen.onkey(l_paddle.go_down,"s")




game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    ball.move()

    #Detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        # needs to bounce
        ball.bounce_y()

    # Detecdt collision with r_paddle
    if 320 <= ball.xcor() <= 321:
        if r_paddle.distance(ball) < 50:
            ball.bounce_x()

    # Detecdt collision with l_paddle
    if -321 <= ball.xcor() <= -320:
        if l_paddle.distance(ball) < 50:
            ball.bounce_x()

    # Detect game over
    if ball.xcor()>360 or ball.xcor() < -360:
        game_is_on=False










screen.exitonclick()