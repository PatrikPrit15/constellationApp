import pandas as pd
import tkinter as tk
import random
import math

class Constellation:
    def __init__(self, constellationPD):
        self.code = constellationPD['IAU code']
        self.nameLAT = constellationPD['Latin name']
        self.nameEN = constellationPD['English name']
        self.area = constellationPD['Constellation area in %']
        self.mainstar = constellationPD['Principal star']
        RAstr = constellationPD['RA']
        self.RA = float(RAstr[0:2])+float(RAstr[3:5])/60
        DECstr = constellationPD['Dec']
        self.DEC = float(DECstr[1:3])+float(DECstr[5:7])/60
        self.DEC = -self.DEC if DECstr[0] == '-' else self.DEC