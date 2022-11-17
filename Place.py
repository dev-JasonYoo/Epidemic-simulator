from Person import *

class Place:
    __adjacency_dict = {}
    empty = '_'
    
    def __init__(self, name, capacity, dimension, control_lv, adjacents = []):
        self.__name = name
        self.__capacity = capacity
        self.__control_lv = control_lv
        self.__population_list = []
        
        self.__dimension = dimension # [x,y] : list
        self.__field = [ [ self.empty for x in range(dimension[0]) ] for y in range(dimension[1]) ]
##        for row in self.__field: print(row)
        
        Place.__adjacency_dict[name] = adjacents # list of strings
        for place in adjacents:
            Place.__adjacency_dict[str(place)].append(name) # dictionary value : sets instead of list? on behalf of no repeating items

        return None

    def __repr__(self):
        return f"Place('{self.__name}', {self.__capacity}, {self.__dimension}, {self.__control_lv})"

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

##    @field.setter
##    def field(self, x, y, person: Person):
##        self.__field[y][x] = person

    @field.setter
    def field(self, value: list):
        self.__field = value

    @property
    def population_list(self):
        return self.__population_list

    @population_list.setter
    def population_list(self, value: list):
        self.__population_list = value
