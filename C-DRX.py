import random as rd
import numpy as np

class C_DRX:
    cycleLength = [10, 20, 50, 100]
    onPeriods = [3, 5, 10]
    offsets = [0, 0.5, 1, 2.5, 5]
    
    p1 = [0, 0, 0.6, 0.4]
    p2 = [0.6, 0.4, 0, 0]
    p3 = [0, 0, 0.3, 0.7]
    
    @classmethod
    def cdrxConfig(cls, nameSlice):
        if 'eMBB' in nameSlice:
            cL = np.random.choice(cls.cycleLength, p=cls.p1)
            on = cls.onPeriods[0]
            off = np.random.choice(cls.offsets)