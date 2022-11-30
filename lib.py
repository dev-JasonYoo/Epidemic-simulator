from random import randint
from Place import *

## ----------main()-----------

def assign(population: list, place: Place):
    dimension = place.dimension
    place.population_list += population
    for person in population:
        while True: # do over until it chooses empty coordinate
            x = randint(0, dimension[0] - 1)
            y = randint(0, dimension[1] - 1)
            if place.field[y][x] == Place.empty: break
            
        # Place instance
        place.field[y][x] = person

        # Person instance
        person.place = [place, [x, y]]
    return None
    
    
def update_position_in_place(population: list, place: Place):
    field = place.field
    dim_x = place.dimension[0]
    dim_y = place.dimension[1]
    for person in population:
        if symptom_found(person):
            if not in_quarantine(person): # for people showing symptom but not in quarantine
                go_quarantine(person) # assign quarantine to person's place
                continue # go on for the next person
            else: # for people who are already in quarantine
                continue # go on for the next person
        x = person.place[1][0]
        y = person.place[1][1]
        dx = randint(-1,1) # predetermine what direction to move
        dy = randint(-1,1)
##        print(x, y, " -> ", dx, dy)

        if (0 < x+dx) and (x+dx < dim_x) and (0 < y+dy) and (y+dy < dim_y):
            if not person_exists(field, [x+dx, y+dy]): # If no one is there
                # Place instance
##                print(field[y][x] , field[y+dy][x+dx])
                field[y][x] , field[y+dy][x+dx] = field[y+dy][x+dx] , field[y][x] # move forward
##                print(field[y][x] , field[y+dy][x+dx])

                # Person instance
                person.place[1][0] += dx
                person.place[1][1] += dy
        else: # If a person bumps into wall
            pass # Just leave it there
    
    return field

def go_quarantine(person: Person):
    # Place instance
    place = person.place[0]
    x,y = person.place[1]
    place.field[y][x] = Place.empty

    # Person instance
    person.place = Place.quarantine

    return None

def free_quarantine(person: Person):
    # free from quarantine: return the immuned person to a random place
    place = choices(Place.get_place_list())
    assign([person], place[0])
    return None

def symptom_found(person: Person):
    if is_infected(person):
        status = person.status
        if status.symptomatic: # if one is infected to symptomatic one
            if status.incubation_days <= status.days: # and if symptoms became apparent
                return True 
    return False # if not infected, or infected to asymptomatic one

def update_person_status(population: list):
    for person in population:
        if is_infected(person): # for those infected
            person.status.add_days() # add 1 to elapsed days
            if person.status.days >= person.status.recovery_days: # if it's time to be cured
                person.status = Epid.immuned # assign Epid.immuned
                free_quarantine(person)

def get_case_list(population: list):
    return [ person for person in population if is_infected(person) ] # sets of persons infected

def update_new_case(case_list: list): # update new cases based on input case list
    for infected_person in case_list: # iterate all the infected
        if in_quarantine(infected_person):# infected people in quarantine do not spread disease
            continue # so go on for the next person
        xy = infected_person.place[1]
        close_list = close_persons(infected_person.place[0].field, xy) # load a list of close Persons

        #print(infected_person)
        cpc = infected_person.status.cpc
        for close_person in close_list: # determine if close persons get infected
            if is_susceptible(close_person): # if the close person isn't infected yet(still susceptible)
                infection = choices( [True, False], [cpc, 1 - cpc] )[0] # infection by the probability of cpc
                if infection:
                    close_person.status = infected_person.status.spread() # update new cases
    #print()
    return None

def close_persons(field: list, xy: list):
    field = field
    x , y = xy
    result = []
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            if 0 <= (x+dx) and 0 <= (y+dy): # to prevent negative number index (ex: [-1]) 
                if person_exists(field, [x+dx , y+dy]):
                    result.append(field[y+dy][x+dx])
    return result

def person_exists(field: list, xy: list):
    try:
        if field[xy[1]][xy[0]] == Place.empty: # field[y][x]
            return False # if it's empty, 
        else: return True
    except IndexError: # if it's out of index
        return False # it can be considered as empty as well
##        print(field)
##        print(xy)
##        raise IndexError

def spread_epid(population):
    case_list = get_case_list(population)
    update_new_case(case_list)
    update_person_status(population) # after all daily activity, go on for the next day
    return None
    
def is_infected(person: Person):
    return isinstance(person.status, Epid)

def is_susceptible(person: Person):
    if person.status == Epid.susceptible:
        return True
    return False

def in_quarantine(person: Person):
    if person.place == Place.quarantine:
        return True
    return False

## -----------visualize------------

def print_field(place: Place):
    result = ""
    for row in place.field:
        for person in row:
##            if person: print(person.ID_num, "\t", end = '') # Minimize the number of print() calling
##            else: print(person, "\t", end = '')
            if not person == "_": result += str(person.ID_num) + "\t" # Better efficiency
            else: result += str(person) + "\t"
        result += "\n"
    print(result)
    return None

def str_field_id(place: Place):
    result = ""
    for row in place.field:
        for person in row:
##            if person: print(person.ID_num, "\t", end = '') # Minimize the number of print() calling
##            else: print(person, "\t", end = '')
            if not person == Place.empty: result += str(person.ID_num) + "\t" # Better efficiency
            else: result += str(person) + "\t"
        result += "\n"*2
    return result

# 6 demonstrates the right ratio.
# "\t" is as long as 12 to 13
n = 6
tab = " " * n
def str_field_infect(place: Place):
    x,y = place.dimension
    result = ""
    for row in place.field:
        for person in row:
            if not person == Place.empty: # if there is person
                if is_infected(person): # if infeced
                    result += ("\u25A0" + tab)
                elif not is_susceptible(person): # if already cured
                    result += ("\u2594" + tab)
                else: # if suceptible
                    result += ("\u25B4"+ tab)
            else: result += "  " + tab
        result += "|" + "\n"*2 + "|"
    return "- "*int(3.8*x) + "\n" + "|" + result[:-2] + "- "*int(3.8*x)

## -----------file output----------
