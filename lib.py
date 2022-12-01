from random import randint
from random import choices
from Place import *

## ----------main()-----------

def init_assign(population: list, place: Place, init = False):
    dimension = place.dimension
    place.population_list += population

    # The first person is always placed in the very middle
    x = dimension[0]//2
    y = dimension[1]//2
    place.field[y][x] = population[0]
    population[0].place = [place, [x, y]]
    
    for person in population[1:]:
        while True: # do over until it chooses empty coordinate
            x = randint(0, dimension[0] - 1)
            y = randint(0, dimension[1] - 1)
            if place.field[y][x] == Place.empty: break
            
        # Place instance
        place.field[y][x] = person

        # Person instance
        person.place = [place, [x, y]]
    return None

def assign(population: list, place: Place, init = False):
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
            if in_quarantine(person): # for people showing symptom in quarantine
                continue # let them in quarantine

        trial = 0
        while True:
            x = person.place[1][0]
            y = person.place[1][1]
            dx = randint(-4,4) # predetermine what direction to move
            dy = randint(-4,4)

            if (0 < x+dx) and (x+dx < dim_x) and (0 < y+dy) and (y+dy < dim_y):
                if not person_exists(field, [x+dx, y+dy]): # if it succeeded finding the next possible coordinate
                    break

            trial += 1
            if trial == 32: # if 32 trials are all failed, consider it as stuck
                dx, dy = 0, 0 # let it stay there
                break
                
        # Place instance
        field[y][x] , field[y+dy][x+dx] = field[y+dy][x+dx] , field[y][x] # move forward

        # Person instance
        person.place[1][0] += dx
        person.place[1][1] += dy
    
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

def to_be_recovered(person: Person):
    status = person.status
    if status.recovery_days <= status.days: # if it's time to be cured
        return True
    return False

def update_person_status(population: list, quarantine):
    new_recovered = 0
    
    for person in population:
        if is_infected(person): # for those infected
            person.status.add_days() # add 1 to elapsed days
            if symptom_found(person): # for infected people showing symptoms]
                
                if not in_quarantine(person): # but not in quarantine
                    if quarantine: # only if quarantine is required
                        go_quarantine(person) # assign quarantine to person's place
                        continue # go on for the next person

                if to_be_recovered(person): # for people to be recovered (in quarantine)
                    person.status = Epid.immuned # assign Epid.immuned
                    if quarantine: # only if quarantinen is required
                        free_quarantine(person)
                    new_recovered += 1
                    continue # go on for the next person
                    
    return new_recovered                

def get_case_list(population: list):
    return [ person for person in population if is_infected(person) ] # sets of persons infected

def update_new_case(case_list: list): # update new cases based on input case list
    result = {
        'new_case_num': 0,
        'infectious_num': len(case_list),
        'quarantine_num': 0
    }
    
    for infected_person in case_list: # iterate all the infected
        if in_quarantine(infected_person):# infected people in quarantine do not spread disease
            result['quarantine_num'] += 1
            continue # so go on for the next person
        xy = infected_person.place[1]
        close_list = close_persons(infected_person.place[0].field, xy) # load a list of close Persons

        cpc = infected_person.status.cpc
        for close_person in close_list: # determine if close persons get infected
            if is_susceptible(close_person): # if the close person isn't infected yet(still susceptible)
                infection = choices( [True, False], [cpc, 1 - cpc] )[0] # infection by the probability of cpc
                if infection:
                    result['new_case_num'] += 1
                    close_person.status = infected_person.status.spread() # update new cases
    return result

def close_persons(field: list, xy: list):
    field = field
    x , y = xy
    result = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
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

def spread_epid(population, quarantine):
    case_list = get_case_list(population)
    result = update_new_case(case_list) # dictionary: 'new_case_num', 'infectious_num', 'quarantine_num'
    new_recovered_num = update_person_status(population, quarantine) # after all daily activity, go on for the next day

    result['new_recovered_num'] = new_recovered_num
    return result # return the daily result
    
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
