from lib import *
from os import system
from turtle import *
from time import sleep
from matplotlib import pyplot as plt

n=270
n0 = 3
corona = repr(Epid(0.3, incubation_days = 2))

def test(quarantine = True):
    population = [ Person(ID_num, 0, 0, 0) for ID_num in range(n) ]

    # assign initial cases
    for idx in range(n0):
        population[idx].status = eval(corona)

    # initialize places and assign people to them
    square1 = Place('square1', 10, [30, 30], 0, [])
    init_assign(population, square1, init = True)
    
    day = 0
    susceptible = n - n0 # S
    infectious = n0 # I
    recovered = 0 # R
    while True:
        day += 1
        square1.field = update_position_in_place(population[:n], square1)
        result = spread_epid(population[:n], quarantine)

        # result: new_case_num, infectious_num, quarantine_num, new_recovered_num        
        susceptible -= result['new_case_num']
        infectious += result['new_case_num'] - result['new_recovered_num']
        recovered += result['new_recovered_num']
        print(f'Day {day}: S{susceptible} I{infectious} R{recovered}')

        # determine if epidemic went extinct
        if result['new_case_num'] == 0:
            if result['infectious_num'] == 0:
                if result['quarantine_num'] == 0:
                    break

    return [person.status for person in population].count(True) # number of total cases

def test_visible(quarantine = True):
    import turtle as t
    population = [ Person(ID_num, 0, 0, 0) for ID_num in range(n) ]

    for idx in range(n0):
        population[idx].status = eval(corona)

    square1 = Place('square1', 10, [30, 30], 0, [])
    init_assign(population, square1)

    # ---- turtle ----
    try:
        t.penup()
    except:
        t.penup()
    t.hideturtle()
    t.goto(-500,-350)
    t.tracer(False)
    t.screen = Screen()
    t.screen.setup(1.0, 1.0, startx = None, starty = None)
    # ---- turtle ----

    day = 0
    while True:
        day += 1
        print('Day ', day)
        square1.field = update_position_in_place(population[:n], square1)

        # ---- turtle ----
        t.write(str_field_infect(square1) + f"Day {day+1}", font = ('Arial', 7, 'normal'))
        sleep(0.05)
        # ---- turtle ----
        
        result = spread_epid(population[:n], quarantine)
        if result['new_case_num'] == 0:
            if result['infectious_num'] == 0:
                if result['quarantine_num'] == 0:
                    break # this means that the epidemic went extinct
        t.clear()
    t.bye()

    return [person.status for person in population].count(True), f"Day {day}"

def histogram(result_list: list):
    keys = [x for x in range(0,271,10)]
    result_list = list(map(lambda x: x//10 * 10, result_list))
    histogram = dict.fromkeys(keys, 0)
    for result in result_list:
        histogram[result] += 1    
    return histogram
