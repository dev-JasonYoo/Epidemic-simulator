from lib import *
from os import system
from turtle import *
from time import sleep

def test(quarantine = True):   
    n = 270
    population = [ Person(ID_num, 0, 0, 0) for ID_num in range(n) ]

    corona = Epid(0.3)
    population[0].status = corona

    square1 = Place('square1', 10, [30, 30], 0, [])
    assign(population, square1)

    while True:
        square1.field = update_position_in_place(population[:n], square1)
        result = spread_epid(population[:n])
        if result['new_case_num'] == 0:
            if result['infectious_num'] == 0:
                if result['quarantine_num'] == 0:
                    break # this means that the epidemic went extinct
    return [person.status for person in population].count(True)

def test_visible(quarantine = True):
    import turtle as t
    n = 270
    population = [ Person(ID_num, 0, 0, 0) for ID_num in range(n) ]

    corona = Epid(0.3)
    population[0].status = corona

    square1 = Place('square1', 10, [30, 30], 0, [])
    assign(population, square1)

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

    day = 1
    while True:
        day += 1
        square1.field = update_position_in_place(population[:n], square1)

        # ---- turtle ----
        t.write(str_field_infect(square1) + f"Day {day+1}", font = ('Arial', 7, 'normal'))
        sleep(0.2)
        # ---- turtle ----
        
        result = spread_epid(population[:n])
        if result['new_case_num'] == 0:
            if result['infectious_num'] == 0:
                if result['quarantine_num'] == 0:
                    break # this means that the epidemic went extinct
        t.clear()

    t.bye()
    return [person.status for person in population].count(True), f"Day {day}"
