from lib import *
from os import system
from turtle import *
from time import sleep


n = 270
## Initialize Person instances
population = [ Person(ID_num, 0, 0, 0) for ID_num in range(n) ]

corona = Epid(0.3)
population[0].status = corona

## Initialize Place instances
square1 = Place('square1', 10, [30, 30], 0, [])
square2 = Place('square2', 10, [10, 10], 0, ['square1'])

##square1_dimension = square1.dimension
##for person in population[:10]:
##    x = randint(0, square1_dimension[0] - 1)
##    y = randint(0, square1_dimension[1] - 1)
##    square1.field[x][y] = person

assign(population, square1)
## print_field(square1)

## CMD graphic
##for _ in range(30):
##    system('cls')
##    square1.field = update_position_in_place(population[:n], square1)
##    print_field(square1)
##    system('timeout 1')

## Turtle module graphic
penup()
hideturtle()
goto(-500,-350)
tracer(False)
screen = Screen()
screen.setup(1.0, 1.0, startx = None, starty = None)
for day in range(200):
    square1.field = update_position_in_place(population[:n], square1)
##    write(str_field_id(square1), font = ('Arial', 5, 'normal'))
    write(str_field_infect(square1) + f"Day {day+1}", font = ('Arial', 7, 'normal'))
    #sleep(0.1)
    clear()
##    for person in population[:n]:
##        if is_infected(person): print(person)
    print()
    spread_epid(population[:n])
