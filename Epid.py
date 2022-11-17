from random import choices

class Epid:
    def __init__(self, cpc, incubation_days = 7, days = 0, symptomatic = True):
        self.__cpc = cpc # number of cases per contact
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

    def determine_infect(self, *factors):        
        return choice([True, False], [self.cpc, 1-self.cpc])
