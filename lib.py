from random import randint

class Epid:
    def __init__(self, R0, incubation_days = 7, days = 0, symptomatic = True):
        self.__R0 = R0
        self.__incubation_days = incubation_days
        self.__days = days
        self.__symptomatic = symptomatic
        return None

    def __repr__(self):
        return f"Epid({self.__R0}, {self.__incubation_days}, {self.__days}, {self.__symptomatic})"

    def __str__(self):
        pass

    def get_incubation_days(self):
        return self.__incubation_days
    
    def get_days(self):
        return self.__days

    def add_days(self):
        self.__days += 1
        return None

    def get_symptomatic(self):
        return self.__symptomatic

class Person:
    def __init__(self, ID_num, name, age, place):
        self.__ID_num = ID_num
        self.__name = name
        self.__age = age
        self.__place = place
        self.__status = None
        return None

    def __repr__(self):
        return f"Person({self.__ID_num}, {self.__name}, {self.__age}, {self.__place})"

    @property
    def ID_num(self):
        return self.__ID_num

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def add_age(self):
        self.__age += 1
        return None
    
    def get_place(self):
        return self.__place

    def set_place(self, place):
        self.__place = place
        return None

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
        return None

class Place:
    __adjacency_dict = {}
    
    def __init__(self, name, capacity, dimension, control_lv, adjacents = []):
        self.__name = name
        self.__capacity = capacity
        
        self.__dimension = dimension # [x,y] : list
        self.__field = [ [ 0 for x in range(dimension[0]) ] for _ in range(dimension[1]) ]
##        for row in self.__field: print(row)
        
        self.__control_lv = control_lv
        
        Place.__adjacency_dict[name] = adjacents # list of strings
        for place in adjacents:
            Place.__adjacency_dict[str(place)].append(name) # dictionary value : sets instead of list? on behalf of no repeating items

        return None

    def __repr__(self):
        return f"Place('{self.__name}', {self.__capacity}, {self.__demension}, {self.__control_lv})"

    def __str__(self):
        return f"{self.__name}"

    @classmethod
    def get_adjacency_dict(cls):
        return Place.__adjacency_dict

    @property # write an explanation of what @property decorator is and where I learned
    def dimension(self):
        return self.__dimension

    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, x, y, person: Person):
        self.__field[y][x] = person

## ----------main()-----------

def assign(population: list, place: Place):
    dimension = place.dimension
    for person in population:
        x = randint(0, dimension[0] - 1)
        y = randint(0, dimension[1] - 1)
        place.field[y][x] = person
    return None
    
    
def update_position():
    pass

## -----------visualize------------

def print_field(place: Place):
    for row in place.field:
        for col in row:
            if col: print(col.ID_num, "\t", end = '')
            else: print(col, "\t", end = '')
        print()
    return None

