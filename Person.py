from Epid import *

class Person:
    def __init__(self, ID_num, name, age, place):
        self.__ID_num = ID_num
        self.__name = name
        self.__age = age
        self.__place= place
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

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        self.__place = value

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
        return None
