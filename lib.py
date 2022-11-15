from random import randint
from Place import *

## ----------main()-----------

def assign(population: list, place: Place):
    dimension = place.dimension
    place.population_list = population
    for person in population:
        # Place instance
        x = randint(0, dimension[0] - 1)
        y = randint(0, dimension[1] - 1)
        place.field[y][x] = person

        # Person instance
        person.place = [place, [x, y]]
    return None
    
    
def update_position_in_place(population: list, place: Place):
    field = place.field
    dim_x = place.dimension[0]
    dim_y = place.dimension[1]
    for person in population:
        x = person.place[1][0]
        y = person.place[1][1]
        dx = randint(-1,1) # predetermine what direction to move
        dy = randint(-1,1)
##        print(x, y, " -> ", dx, dy)

        if x+dx < dim_x and y+dy < dim_y:
            if not field[y+dy][x+dx] != "_": # If no one is there
                # Place instance
##                print(field[y][x] , field[y+dy][x+dx])
                field[y][x] , field[y+dy][x+dx] = field[y+dy][x+dx] , field[y][x] # move forward
##                print(field[y][x] , field[y+dy][x+dx])

                # Person instance
                person.place[1][0] += dx
                person.place[1][1] += dy
        else: # If a person bumps into wall
            pass # Just leave him or her there
    
    return field

## -----------visualize------------

def print_field(place: Place):
    result = ""
    for row in place.field:
        for col in row:
##            if col: print(col.ID_num, "\t", end = '') # Minimize the number of print() calling
##            else: print(col, "\t", end = '')
            if not col == "_": result += str(col.ID_num) + "\t" # Better efficiency
            else: result += str(col) + "\t"
        result += "\n"
    print(result)
    return None

def str_field(place: Place):
    result = ""
    for row in place.field:
        for col in row:
##            if col: print(col.ID_num, "\t", end = '') # Minimize the number of print() calling
##            else: print(col, "\t", end = '')
            if not col == "_": result += str(col.ID_num) + "\t" # Better efficiency
            else: result += str(col) + "\t"
        result += "\n"*2
    return result


## -----------file output----------
