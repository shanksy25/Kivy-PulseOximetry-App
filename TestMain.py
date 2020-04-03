import pandas as pd
from scipy.signal import find_peaks
import numpy as np
from numpy import sqrt
import matplotlib.pyplot as plt
import scipy as sp
import math
import statistics
import os
import bluetooth
import sys
import serial
import time
import io
from datetime import datetime
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

class FirstScreen(Screen):
    pass

class SecondScreen(Screen):
    def Calc(Button):
        global ser
        ser = serial.Serial(port='COM3', baudrate=9600, timeout=1)
        time.sleep(2)
        global HR
        global SPO22
        data = []
        #print("connected to: " + ser.name)

        for i in range(0, 4000):
            blueData = ser.readline().decode().rstrip()
            dataArr = float(blueData)
            data.append(dataArr)
            #print(data)

        # Moving Average
        mov = np.convolve(data, 20)
        IR = mov[0:2000]
        R = mov[2000:4000]

        # Oximetry measurement
        mean1 = np.mean(IR)
        mean2 = np.mean(R)
        SPO2 = (mean2 / mean1) * 100
        SPO22 = SPO2 * 1.07  # calibration
        #print("Calculated SPO2 = ", SPO22, "%")

        # Peak Detection
        peaks, _ = find_peaks(IR, distance=50)
        # print(peaks)

        # Measure Heart rate
        num = len(IR)
        HR = np.mean(len(peaks) / num) * 60
        #print("Calculated Heart Rate = ", HR, "bpm")

        return (HR,SPO22)

    def update_text(self):
        text = ('connected to: ' + ser.name)
        text1 = ('Heart Rate: ' + str(HR) + ' bpm')
        text2 = ('Oxygen Saturation: ' + str(SPO22) + '%')
        self.ids.labelconn.text = text
        self.ids.label1.text = text1
        self.ids.label2.text = text2

class MyScreenManager(ScreenManager):
    pass

present = Builder.load_string('''

MyScreenManager:
    FirstScreen:
    SecondScreen:

<Button>:
    font_size: 15

<FirstScreen>:
    name: 'first'
    color: 1,0,1,1
    FloatLayout:
        Label:
            text: 'Welcome to Pulse Oximeter App.....please pair device first'
            font_size: 30

            FloatLayout:
                Button:
                    text: 'View Data'
                    on_release:
                        app.root.current = 'second'
                        root.manager.transition.direction = "left"

<SecondScreen>:
    name: 'second'
    GridLayout:
        rows: 3
        orientation: 'vertical'
        Label:
            text: 'View Data here'
            font_size: 40
        Label:
            id: labelconn
            text: ' '
            font_size: 10
        Label:
            id: label1
            text: 'Heart Rate:'
            font_size: 20
        Label:
            id: label2
            text: 'Oxygen Saturation:'
            font_size: 20

        GridLayout:
            cols: 2
            Button:
                text: 'Read Data'
                on_release:
                    root.Calc()
                    root.update_text()


            Button:
                text: 'Return Home'
                on_release:
                    app.root.current = 'first'
                    root.manager.transition.direction = "right"
''')

class MyApp(App):
    def build(self):
        return present

if __name__ == '__main__':
    MyApp().run()

