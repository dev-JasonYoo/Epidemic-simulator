from random import choices

class Epid:
    immuned = True # If it's set as False, there is no immunization
    susceptible = False
    
    def __init__(self, cpc, incubation_days = 7, recovery_days = 14, days = 0, symptomatic = True):
        self.__cpc = cpc # number of cases per contact
        self.__incubation_days = incubation_days
        self.__recovery_days = recovery_days
        self.__days = days
        self.__symptomatic = symptomatic
        return None

    def __repr__(self):
        return f"Epid({self.__cpc}, {self.__incubation_days}, {self.__recovery_days}, {self.__days}, {self.__symptomatic})"

    def __str__(self):
        return f"Epid({self.__cpc}, {self.__incubation_days}, {self.__recovery_days}, {self.__days}, {self.__symptomatic})"

    @property
    def cpc(self):
        return self.__cpc

    @property
    def incubation_days(self):
        return self.__incubation_days

    @property
    def recovery_days(self):
        return self.__recovery_days

    @property
    def days(self):
        return self.__days

    @days.setter
    def days(self, value):
        self.__days = value

    def add_days(self):
        self.__days += 1
        return None

    @property
    def symptomatic(self):
        return self.__symptomatic

    def spread(self): # returns Epid object with same attributes but 0 for elapsed days
        return eval(f"Epid({self.__cpc}, {self.__incubation_days}, {self.__recovery_days}, 0, {self.__symptomatic})")

