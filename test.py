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

    for day in range(200):
        square1.field = update_position_in_place(population[:n], square1)
        spread_epid(population[:n])
    return [person.status for person in population].count(True)
