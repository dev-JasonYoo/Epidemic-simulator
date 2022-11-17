from lib import *
from os import system
from turtle import *
from time import sleep

## Initialize Person instances
population = [ Person(ID_num, 0, 0, 0) for ID_num in range(100) ]

corona = Epid(0.05)
population[0].status = corona

## Initialize Place instances
square1 = Place('square1', 10, [10, 10], 0, [])
square2 = Place('square2', 10, [10, 10], 0, ['square1'])

##square1_dimension = square1.dimension
##for person in population[:10]:
##    x = randint(0, square1_dimension[0] - 1)
##    y = randint(0, square1_dimension[1] - 1)
##    square1.field[x][y] = person

n = 10

assign(population[:n], square1)
print_field(square1)

## CMD graphic
##for _ in range(30):
##    system('cls')
##    square1.field = update_position_in_place(population[:n], square1)
##    print_field(square1)
##    system('timeout 1')

## Turtle module graphic
penup()
hideturtle()
goto(-200,-200)
tracer(False)
screen = Screen()
screen.setup(1.0, 1.0, startx = None, starty = None)
for _ in range(30):
    square1.field = update_position_in_place(population[:n], square1)
##    write(str_field_id(square1), font = ('Arial', 15, 'normal'))
    write(str_field_infect(square1), font = ('Arial', 15, 'normal'))
    sleep(1)
    clear()

print(person_exists(square1.field, [0,0]))
