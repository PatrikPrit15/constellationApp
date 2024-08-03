import pandas as pd
import tkinter as tk
from tkinter import ttk
import random
import math
from PIL import Image, ImageTk  # Use PIL for more image format support

class Constellation:
    def __init__(self, constellationPD):
        self.code = constellationPD['IAU code']
        self.nameLAT = constellationPD['Latin name']
        self.nameEN = constellationPD['English name']
        self.area = constellationPD['Constellation area in %']
        self.mainstar = constellationPD['Principal star']
        RAstr = constellationPD['RA']
        self.RA = float(RAstr[0:2]) + float(RAstr[3:5]) / 60
        DECstr = constellationPD['Dec']
        self.DEC = float(DECstr[1:3]) + float(DECstr[5:7]) / 60
        self.DEC = -self.DEC if DECstr[0] == '-' else self.DEC

class Game:
    def __init__(self):
        constellationsPD = pd.read_csv('constellations.csv', delimiter=';')
        self.constellations = [Constellation(constellationsPD.loc[i]) for i in range(len(constellationsPD))] 

        self.root = tk.Tk()
        self.root.title('Astro Game')
        self.root.geometry('1200x800')
        self.root.config(bg='#2e3f4f')

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 14), background='#2e3f4f', foreground='white')
        self.style.configure('TButton', font=('Helvetica', 14), background='#2e3f4f', foreground='white')
        self.style.configure('TCanvas', background='#0d1b2a')

        self.image_path = './map.png'  # Update with your image path
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((int(self.root.winfo_screenwidth() * 0.8), int(self.root.winfo_screenheight() * 0.64)))
        self.bg_image = ImageTk.PhotoImage(self.image)

        # Create canvas
        self.canvas = tk.Canvas(self.root, bg='#0d1b2a', highlightthickness=0)
        self.canvas.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.7)
        # self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        self.label = ttk.Label(self.root, text='Click on the constellation:')
        self.label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.05)

        self.result_label = ttk.Label(self.root, text='', anchor='center')
        self.result_label.place(relx=0.1, rely=0.9, relwidth=0.8, relheight=0.05)

        self.clickX = -1
        self.clickY = -1

    def callback(self, event):
        x = event.x / self.canvas.winfo_width()
        y = event.y / self.canvas.winfo_height()
        self.clickX = x
        self.clickY = y 

    def spherical_distance(self, RA1, DEC1, RA2, DEC2):
        RA1 = math.radians(RA1 * 15)
        DEC1 = math.radians(DEC1)
        RA2 = math.radians(RA2 * 15)
        DEC2 = math.radians(DEC2)
        return math.acos(math.sin(DEC1) * math.sin(DEC2) + math.cos(DEC1) * math.cos(DEC2) * math.cos(RA1 - RA2))

    def start(self):
        self.canvas.bind("<Button-1>", self.callback)
        while True:
            constellation = random.choice(self.constellations)
            self.label.config(text='Click on the constellation: ' + constellation.nameLAT)
            self.root.update()

            # register click
            while self.clickX == -1:
                self.root.update()

            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)


            x = self.clickX
            y = self.clickY
            self.clickX = -1
            self.clickY = -1

            clickRA = 24 * (1 - x)
            clickDEC = 180 * (1 - y) - 90
            distance = self.spherical_distance(constellation.RA, constellation.DEC, clickRA, clickDEC) * 180 / math.pi

            realX = (24 - constellation.RA) / 24
            realY = (90 - constellation.DEC) / 180
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            self.canvas.create_oval(realX * canvas_width - 5, realY * canvas_height - 5,
                                    realX * canvas_width + 5, realY * canvas_height + 5, fill='red')

            self.result_label.config(text=f"Constellation: {constellation.code}/{constellation.nameEN}/{constellation.nameLAT}, "
                                          f"Alpha Star: {constellation.mainstar}, Distance: {distance:.2f} degrees")


            self.root.update()
            
            while self.clickX == -1:
                self.root.update()
            self.clickX = -1
            self.clickY = -1

            self.canvas.delete('all')
            self.result_label.config(text="")


game = Game()
game.start()
