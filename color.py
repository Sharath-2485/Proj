from turtle import *
bgcolor('black')
speed(0)
pencolor('yellow')
def draw(x):
    right(10)
    for i in range(90):
        forward(x)
        right(100)
        forward(x)
x=120
for i in range(8):
    for j in range(36):
        draw(x)
    x-=10
hideturtle()
done()
                