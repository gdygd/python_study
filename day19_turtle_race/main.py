from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()

angle = 0

def move_forwards():
    tim.forward(18)

def move_backwards():
    tim.backward(18)

def rotate_right():
    global angle
    angle -= 5
    tim.setheading(angle)
def rotate_left():
    global angle
    angle += 5
    tim.setheading(angle)

def clear_drawing():
    tim.clear()

screen.listen()
screen.onkey(key="w", fun=move_forwards)
screen.onkey(key="s", fun=move_backwards)
screen.onkey(key="d", fun=rotate_right)
screen.onkey(key="a", fun=rotate_left)
screen.onkey(key="c", fun=clear_drawing)
screen.exitonclick()