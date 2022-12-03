from Person import *

class Place:
    ''' Information about Place class

    Static variables:

    __adjacency_dict # not used (only used in initialization)
        dict(str: Place)

    __place_list # not used (only used in initialization)
        list of Place objects

    empty
        string

    quarantine
        bool


    Attributes:

    __name
        string
    
    __population_list
        list of People objects

    __dimension
        list of two positive integers

    __field
        2nd dimensional list of strings and Person objects, based on __dimension
        The components are initialized with Place.empty '''
    __adjacency_dict = {} # not used (only used in initialization)
    __place_list = [] # not used (only used in initialization)

    empty = '_'
    quarantine = False
    
    def __init__(self, name: str, capacity: int, dimension: list, control_lv: int, adjacents = []):
        ''' Initialize self,

        Place, str, int, list of two positive integers, int, list of Places -> None '''
        self.__name = name
        self.__capacity = capacity # not used (only used in initialization)
        self.__control_lv = control_lv # not used (only used in initialization)
        self.__population_list = []
        
        self.__dimension = dimension # [x,y] : list
        self.__field = [ [ self.empty for x in range(dimension[0]) ] for y in range(dimension[1]) ]
##        for row in self.__field: print(row)
        
        Place.__adjacency_dict[name] = adjacents # list of strings
        for place in adjacents:
            Place.__adjacency_dict[str(place)].append(name) # dictionary value : sets instead of list? on behalf of no repeating items

        Place.__place_list += [self] # add to '__place_list'

    def __repr__(self):
        ''' Returns the representation of this Place object

        Place -> str '''
        return f"Place('{self.__name}', {self.__capacity}, {self.__dimension}, {self.__control_lv})"

    def __str__(self):
        ''' Returns the string form of this Place object

        Place -> str '''
        return f"{self.__name}"

    @classmethod
    def get_adjacency_dict(cls): # not used
        ''' Getter of static variable __adjacency_dict

        Place -> dict(Place: list of Places) '''
        return cls.__adjacency_dict

    @classmethod
    def get_place_list(cls): # not used
        ''' Getter of static variable __place_list

        Place -> list of Places '''
        return cls.__place_list

    @property # write an explanation of what @property decorator is and where I learned
    def dimension(self):
        ''' Getter of attribute dimension by property decorator

        Place -> list of two positive integers '''
        return self.__dimension

    @property
    def field(self):
        ''' Getter of attribute field by property decorator

        Place -> list of list of strings and Place objects '''
        return self.__field

    @field.setter
    def field(self, value: list):
        ''' Setter of attribute field by property decorator

        Place, list of list of strings and Person objects -> None '''
        self.__field = value
        return None

    @property
    def population_list(self):
        ''' Getter of attribute population_list by property decorator

        Place -> list of Person objects '''
        return self.__population_list

    @population_list.setter
    def population_list(self, value: list):
        ''' Setter of attribute population_list by property decorator

        Place, list of Person objects -> None '''
        self.__population_list = value
        return None
