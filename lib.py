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
            if not person_exists(field, [x+dx, y+dy]): # If no one is there
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

def gen_new_case_list(population: list, place: Place):
    close_list = close_persons()
    pass

def spread_epid():
    pass

def close_persons(field: list, xy: list):
    field = field
    x , y = xy
    result = []
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            if person_exists(field, [x+dx , y+dy]):
                result.append(field[x+dx , y+dy])
    return result

def person_exists(field: list, xy: list):
    if field[xy[1]][xy[0]] == Place.empty: # field[y][x]
        return False
    else: return True
    

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

def str_field_id(place: Place):
    result = ""
    for row in place.field:
        for col in row:
##            if col: print(col.ID_num, "\t", end = '') # Minimize the number of print() calling
##            else: print(col, "\t", end = '')
            if not col == Place.empty: result += str(col.ID_num) + "\t" # Better efficiency
            else: result += str(col) + "\t"
        result += "\n"*2
    return result

def str_field_infect(place: Place):
    x,y = place.dimension
    result = ""
    for row in place.field:
        for col in row:
            if not col == Place.empty:
                result += "\u25A0" if col.status else "\u25A1"+ "\t"
            else: result += "  " + "\t"
        result += "|" + "\n"*2 + "|"
    return "- "*7*x + "\n" + result+ "\n" + "- "*7*x


## -----------file output----------
