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



class Game:
    def __init__(self):
        constellationsPD = pd.read_csv('constellations.csv', delimiter=';')
        self.constellations = [Constellation(constellationsPD.loc[i]) for i in range(len(constellationsPD))] 

        self.root = tk.Tk()
        self.root.title('Astro Game')
        self.root.geometry('600x500')
        

        self.map_coords = [0.1,0.1,0.9,0.9]
        self.canvas = tk.Canvas(self.root, bg='blue')
        self.canvas.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.label = tk.Label(self.root, text='Click on constellation:')
        self.label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.05)

        self.clickX = -1
        self.clickY = -1