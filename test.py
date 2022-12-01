from lib import *
from turtle import *
from time import *
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from functools import partial
import numpy as np

n=270
n0 = 3
corona = repr(Epid(0.1, incubation_days = 4))

def test(quarantine = True):
    population = [ Person(ID_num, 0, 0, 0) for ID_num in range(n) ]

    # assign initial cases
    for idx in range(n0):
        population[idx].status = eval(corona)

    # initialize places and assign people to them
    square1 = Place('square1', 10, [30, 30], 0, [])
    init_assign(population, square1, init = True)
    
    day = 0
    susceptible = [n - n0] # S
    infectious = [n0] # I
    recovered = [0] # R
    while True:
        day += 1
        square1.field = update_position_in_place(population[:n], square1)
        result = spread_epid(population[:n], quarantine)

        # result: new_case_num, infectious_num, quarantine_num, new_recovered_num        
        susceptible.append(susceptible[-1] - result['new_case_num'])
        infectious.append(infectious[-1] + result['new_case_num'] - result['new_recovered_num'])
        recovered.append(recovered[-1] + result['new_recovered_num'])
        print(f'Day {day}: S{susceptible[-1]} I{infectious[-1]} R{recovered[-1]}')

        # determine if epidemic went extinct
        if result['new_case_num'] == 0:
            if result['infectious_num'] == 0:
                if result['quarantine_num'] == 0:
                    break

    result = {
        'S': susceptible,
        'I': infectious,
        'R': recovered,
    }
    return result

def animate(result):
    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1,2,1)
    ax1.axis(ymin = -5, ymax = 275)
    ax2 = fig.add_subplot(1,2,2)
    ax2.axis(ymin = -5, ymax = 275)
    
    x = []
    S, I, R = [], [], []    

    def update(result, frame):
        x.append(frame)
        S.append(result['S'][frame])
        I.append(result['I'][frame])
        R.append(result['R'][frame])
        
        ax1.clear()
        ax2.clear()
        
        ax1.bar(x, S, color = 'gray')
        ax1.bar(x, I, bottom = np.array(S), color = 'red')
        ax1.bar(x, R, bottom = np.array(S) + np.array(I), color = 'blue')

        ax2.plot(S, color = 'gray')
        ax2.plot(I, color = 'red')
        ax2.plot(R, color = 'blue')
        
    def animate_helper(result):
        ani = animation.FuncAnimation(
            fig,
            partial(update, result),
            frames = list(range(len(result['S']))),
            interval = 100,
            repeat = False
        )
        plt.show()

    animate_helper(result)

    
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


result = test(False)
animate(result)
