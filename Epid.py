from random import choices

class Epid:
    ''' Information about Epid class

    Attributes:

    immuned
        bool

    susceptible
        bool

    cpc
        float

    incubation_days
        int

    recover_days
        int

    days
        int

    symptomatic
        bool

    asymptomatic_variant
        bool or float '''
    immuned = True # If it's set as False, there is no immunization
    susceptible = False
    
    def __init__(self, cpc, incubation_days = 5, recovery_days = 14, days = 0, symptomatic = True, asymptomatic_variant = False):
        ''' Initialize self,

        Epid, int, int, int, int, bool, (bool or float) -> None '''
        self.__cpc = cpc # number of cases per contact
        self.__incubation_days = incubation_days
        self.__recovery_days = recovery_days
        self.__days = days
        self.__symptomatic = symptomatic
        if asymptomatic_variant == False or (type(asymptomatic_variant) == float and 0 <= asymptomatic_variant and asymptomatic_variant <= 1):
            self.__asymptomatic_variant = asymptomatic_variant # false or probability
        else:
            print("asymptomatic_variant parameter should be False or a value between 0 and 1")
            raise("ValueError")

    def __repr__(self):
        ''' Returns the representation of this Epid object

        Epid -> str '''
        return f"Epid({self.__cpc}, {self.__incubation_days}, {self.__recovery_days}, {self.__days}, {self.__symptomatic}, {self.__asymptomatic_variant})"

    def __str__(self):
        ''' Returns the string form of this Epid object

        Epid -> str '''
        return f"Epid({self.__cpc}, {self.__incubation_days}, {self.__recovery_days}, {self.__days}, {self.__symptomatic}, {self.__asymptomatic_variant})"

    @property
    def cpc(self):
        ''' Getter method of attribute cpc by property method

        Epid -> float '''
        return self.__cpc

    @property
    def incubation_days(self):
        ''' Getter method of attribute incubation_days by property method

        Epid -> int '''
        return self.__incubation_days

    @property
    def recovery_days(self):
        ''' Getter method of attribute recovery_days by property method

        Epid -> int '''
        return self.__recovery_days

    @property
    def days(self):
        ''' Getter method of attribute cpc by property method

        Epid -> float '''
        return self.__days

    def add_days(self):
        ''' Adds attribute days of this Epid object by 1

        Epid -> None '''
        self.__days += 1
        return None

    @property
    def symptomatic(self):
        ''' Getter method of attribute symptomatic by property method

        Epid -> bool '''
        return self.__symptomatic

    @property
    def asymptomatic_variant(self):
        ''' Getter method of attribute asymptomatic_variant by property method

        Epid -> bool or float '''
        return self.__asymptomatic_variant

    def spread(self): # returns Epid object with same attributes but 0 for elapsed days
        ''' Determines the transmission and asymptomatic mutant,
            based on cpc and asymptomatic_variant of this Epid instance
            and then returns Epid object

        Epid -> Epid '''
        if self.asymptomatic_variant:
            prob = self.asymptomatic_variant
            if choices([True, False], [prob, 1 - prob])[0]:
                print('variant!')
                # succeed to mutate
                return eval(f"Epid({self.__cpc}, {self.__incubation_days}, {self.__recovery_days}, 0, False, {self.__asymptomatic_variant})")
            # failed to mutate
            return eval(f"Epid({self.__cpc}, {self.__incubation_days}, {self.__recovery_days}, 0, True, {self.__asymptomatic_variant})")
        # no possibility for asymptomatic variant
        return eval(f"Epid({self.__cpc}, {self.__incubation_days}, {self.__recovery_days}, 0, {self.__symptomatic})")
