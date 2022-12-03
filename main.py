from lib import *
from turtle import *
from time import *
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib import patches as patches
from functools import partial
import numpy as np
from math import sqrt

n=270 # The number of population
n0 = 3 # The number of the initial cases
corona = repr(Epid(0.2, incubation_days = 4))

def test(quarantine = True):
    ''' gets a boolean value of the quarantine requirement
    returns the dictionary containing the development of the disease,
    based on the given initial settings

    bool -> dictionary<str: list<int>>'''
    population = [ Person(ID_num, 0, 0, 0) for ID_num in range(n) ]

    # assign initial cases
    for idx in range(n0):
        population[idx].status = eval(corona)

    # initialize places and assign people to them
    square1 = Place('square1', 10, [30, 30], 0, [])
    init_assign(population, square1)
    
    day = 0
    susceptible = [n - n0] # S
    infectious = [n0] # I
    recovered = [0] # R
    while True:
        day += 1
        square1.field = update_position_in_place(population[:n], square1)
        result = spread_epid(population[:n], quarantine)

        # result:
        #   new_case_num
        #   infectious_num
        #   quarantine_num
        #   new_recovered_num        
        susceptible.append(susceptible[-1] - result['new_case_num'])
        infectious.append(infectious[-1] + result['new_case_num'] - result['new_recovered_num'])
        recovered.append(recovered[-1] + result['new_recovered_num'])

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


def test_log(file_name: str, quarantine = True):
    ''' Gets a file_name for output file and a boolean value of the quarantine requirement
    functions in the same way with test() but saves log file as txt extension
    returns the dictionary containing the development of the disease,
    based on the given initial settings

    str, bool -> dictionary<str: list<int>> '''
    #file_name should end with '.txt'
    if not file_name[-3:] == '.txt':
        print("file_name should end with '.txt'")
        raise ValueError
    
    population = [ Person(ID_num, 0, 0, 0) for ID_num in range(n) ]

    # assign initial cases
    for idx in range(n0):
        population[idx].status = eval(corona)

    # initialize places and assign people to them
    square1 = Place('square1', 10, [30, 30], 0, [])
    init_assign(population, square1)
    
    day = 0
    susceptible = [n - n0] # S
    infectious = [n0] # I
    recovered = [0] # R
    with open(file_name, 'w') as f:
        f.write(f"n: {n}\nn0: {n0}\ncorona: {repr(corona)}\n")
        f.write(f"Place: {Place.get_place_list()}\n")
        if quarantine:
            f.write("Quarantine is required\n")
        else:
            f.write("Quarantine is not required\n")
        f.write("\n")
        
        while True:
            day += 1
            square1.field = update_position_in_place(population[:n], square1)
            result = spread_epid(population[:n], quarantine)

            # result: new_case_num, infectious_num, quarantine_num, new_recovered_num        
            susceptible.append(susceptible[-1] - result['new_case_num'])
            infectious.append(infectious[-1] + result['new_case_num'] - result['new_recovered_num'])
            recovered.append(recovered[-1] + result['new_recovered_num'])
            f.write(f'Day {day}:\tS{susceptible[-1]}\tI{infectious[-1]}\tR{recovered[-1]}\n')

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
        f.write(f"\nSusceptible:\n{result['S']}\n")
        f.write(f"Infectious:\n{result['I']}\n")
        f.write(f"Recovered:\n{result['R']}\n\n")

        f.write(f"{int(result['R'][-1] / n * 100)} percentage of population got infected.\n")
        f.write(f"The disease vanished in {day} days.")
    return result

    
def test_visible(quarantine = True):
    ''' Gets a boolean value of the quarantine requirement
    Functions in the same way as test() but demonstrates visualization as well
    returns the total number of people who have gone through the epidemic
    and the number of days elpased from the onset to the end of pandemic as a string

    bool -> int, str'''
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
        square1.field = update_position_in_place(population[:n], square1)

        # ---- turtle ----
        t.write(str_field_infect(square1) + f"Day {day+1}", font = ('Arial', 7, 'normal'))
        sleep(0.4)
        # ---- turtle ----
        
        result = spread_epid(population[:n], quarantine)
        if result['new_case_num'] == 0:
            if result['infectious_num'] == 0:
                if result['quarantine_num'] == 0:
                    break # this means that the epidemic went extinct
        t.clear()
    t.bye()

    return [person.status for person in population].count(True), f"Day {day}"


# -------- Live update plot --------


def animate(result):
    ''' gets the list representing a development of an epidemic(in the same form as test() returns)
    along with helper functions defined inside, demonstrates the live update plot day by day

    dict<str: list<int>> -> None '''
    fig = plt.figure(figsize=(15,5))
    fig.suptitle('Epidemic dynamics', fontsize = 20)
    
    ax1 = fig.add_subplot(1,2,1)
    ax1.axis(ymin = -5, ymax = n+5)
    ax1.set_xlabel('Days since onset', fontsize = 12)
    ax1.set_ylabel('Population')
    
    ax2 = fig.add_subplot(1,2,2)
    ax2.axis(ymin = -5, ymax = n+5)
    ax2.set_xlabel('Days since onset')
    ax2.set_ylabel('Population')
    
    x = []
    S, I, R = [], [], []    

    def update(result, frame):
        ''' gets the result dictionary and frame
        as a helper function of animate(), constructs the structure of plot and variables to get updates

        dict<str: list<int>>, int -> None '''
        x.append(frame)
        S.append(result['S'][frame])
        I.append(result['I'][frame])
        R.append(result['R'][frame])
        
        ax1.clear()
        ax2.clear()
        
        ax1.bar(x, S, color = 'gray')
        ax1.bar(x, I, bottom = np.array(S), color = 'red')
        ax1.bar(x, R, bottom = np.array(S) + np.array(I), color = 'blue')

        ax2.plot(S, color = 'gray', label = 'Susceptible')
        ax2.plot(I, color = 'red', label = 'Infectious')
        ax2.plot(R, color = 'blue', label = 'Recovered')
        ax2.legend(loc = 'upper right')

        return None
        
    def animate_helper(result):
        ''' gets the result dictionary
        as a helper function of animate(), organizes the live update plot

        dict<str: list<int>> -> None '''
        ani = animation.FuncAnimation(
            fig,
            partial(update, result),
            frames = list(range(len(result['S']))),
            interval = 100,
            repeat = False
        )
        plt.show()

    animate_helper(result)

    return None

# ---------- static plot ----------

def plot(result):
    ''' gets the result dictionary
    shows the corresponding plot of a bar graph and line graph

    dict<str: list<int>> -> None '''
    fig = plt.figure(figsize=(15,5))
    fig.suptitle('Epidemic dynamics', fontsize = 20)

    # set up frames
    ax1 = fig.add_subplot(1,2,1)
    ax1.axis(ymin = -5, ymax = n+5)
    ax1.set_xlabel('Days since onset', fontsize = 12)
    ax1.set_ylabel('Population')
    
    ax2 = fig.add_subplot(1,2,2)
    ax2.axis(ymin = -5, ymax = n+5)
    ax2.set_xlabel('Days since onset')
    ax2.set_ylabel('Population')

    # plot
    S = result['S']
    I = result['I']
    R = result['R']
    x = len(S)
    domain = list(range(x))
    
    ax1.bar(domain, S, color = 'gray')
    ax1.bar(domain, I, bottom = np.array(S), color = 'red')
    ax1.bar(domain, R, bottom = np.array(S) + np.array(I), color = 'blue')

    ax2.plot(domain, S, color = 'gray', label = 'Susceptible')
    ax2.plot(domain, I, color = 'red', label = 'Infectious')
    ax2.plot(domain, R, color = 'blue', label = 'Recovered')
    ax2.legend(loc = 'upper right')

    plt.show()

    return None


def multiple_plot(result_list):
    ''' gets a list of the result dictionary
    shows all the results combined in a single plot

    list<dict<str: list<int>>> -> None '''
    fig = plt.figure(figsize=(15,5))
    fig.suptitle('Epidemic dynamics', fontsize = 20)

    # set up frames
    ax2 = fig.add_subplot(1,1,1)
    ax2.axis(ymin = -5, ymax = n+5)
    ax2.set_xlabel('Days since onset')
    ax2.set_ylabel('Population')

    length = len(result_list)
    alpha = sqrt(1/length)
    for result in result_list:
        # plot
        S = result['S']
        I = result['I']
        R = result['R']
        x = len(S)
        domain = list(range(x))

        ax2.plot(domain, S, color = 'gray', label = 'Susceptible', alpha = alpha )
        ax2.plot(domain, I, color = 'red', label = 'Infectious', alpha = alpha)
        ax2.plot(domain, R, color = 'blue', label = 'Recovered', alpha = alpha)

    gray = patches.Patch(color='gray', label='Susceptible')
    red = patches.Patch(color='red', label='Infectious')
    blue = patches.Patch(color='blue', label='Recovered')
    ax2.legend(loc = 'upper right')
    plt.show()

    return None
