from Epid import *

class Person:
    ''' Information about Person class

    Attributes:

    __ID_num
        int

    __place
        bool or Place

    __status
        bool or Epid
    '''
    def __init__(self, ID_num: int, name: str, age: int, place):
        ''' Initialize self,

        Person, int, str, int, Place -> None '''
        self.__ID_num = ID_num
        self.__name = name # not used (used only in initialization)
        self.__age = age # not used (used only in initialization)
        self.__place= place
        self.__status = Epid.susceptible

    def __repr__(self):
        ''' Returns the representation of this Person object

        Person -> str '''
        return f"Person({self.__ID_num}, {self.__name}, {self.__age}, {self.__place})"

    def __str__(self):
        ''' Returns the string form of this Person object

        Person -> str '''
        return f"Person({self.__ID_num}, {self.__name}, {self.__age}, {self.__place})"

    @property
    def ID_num(self):
        ''' Getter method of attribute ID_num by property decorator

        Person -> int '''
        return self.__ID_num

    @property
    def place(self):
        ''' Getter method of attribute place by property decorator

        Person -> bool or Place '''
        return self.__place

    @place.setter
    def place(self, value):
        ''' Setter method of attribute place by property decorator

        Person, bool or Place -> None '''
        self.__place = value
        return None

    @property
    def status(self):
        ''' Getter method of attribute status by property decorator

        Person -> bool or Epid '''
        return self.__status

    @status.setter
    def status(self, value):
        ''' Setter method of attribute status by property decorator

        Person, bool or Epid -> None '''
        self.__status = value
        return None
