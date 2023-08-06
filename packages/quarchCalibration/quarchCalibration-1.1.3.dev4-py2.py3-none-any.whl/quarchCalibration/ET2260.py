import time
import sys
from socket import *
from tkinter import *
from tkinter.ttk import *

from pyModbusTCP.client import ModbusClient

class SwitchBoxControl:
    phase_list = ['L1', 'L2', 'L3']
    def __init__(self, name, mux=True):
        self.devices = {}
        self.name = name

    def discover(self):
        self.devices = {}

        self.tsock = socket(AF_INET, SOCK_DGRAM)
        self.tsock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.tsock.sendto('ICPDAS7188E,00'.encode("UTF-8"), ('255.255.255.255', 57188))

        self.rsock = socket(AF_INET, SOCK_DGRAM)
        self.rsock.bind(('', 54321))

        msgs = self.rsock.recvfrom(1024)
        self.rsock.close()

        strmsg = msgs[0].decode("utf8").split(",")
        strdict = {y[0]: y[1] for y in [x.split("=") for x in strmsg[2:]]}

        self.devices[strdict['ALIAS']] = strdict['IP']

    def connect(self):
        ip_addr = self.devices[self.name]

        self.client = ModbusClient(ip_addr, auto_open=True, auto_close=True)
        self.client.write_multiple_coils(0, [0, 0, 0])

    def select_phase(self, phase):
        self.client.write_multiple_coils(0, [0, 0, 0])
        if phase in self.phase_list:
            coil_index = self.phase_list.index(phase)
            self.client.write_single_coil(coil_index, 1)

    def get_phase(self):
        try:
            active = self.client.read_coils(0, 3)
            return self.phase_list[active.index(True)]
        except ValueError:
            return "None"

class ManualController:
    phase_sel = ["L1", "L2", "L3", "None"]
    def __init__(self, target="AC PAM Mux"):
        self.win = Tk()
        self.win.geometry("500x250")
        self.win.title("AC PAM Switchbox Controller")
        self.rbuttons = {}
        self.curphase = StringVar(value="None")
        self.dispphase = StringVar(value="None")
        inc = 0

        for label in self.phase_sel:
            self.rbuttons[label] = Radiobutton(self.win, text=label, variable=self.curphase, value=label, command=self.switch).grid(row=inc, column=0)
            inc += 1

        self.displayPhase = Label(self.win, textvariable=self.dispphase).grid(row=inc, column=0)
        inc += 1
        self.exitbutton = Button(self.win, text="Quit", command=self.exit).grid(row=inc, column=0)

        self.sbcon = SwitchBoxControl(target)
        self.sbcon.discover()
        self.sbcon.connect()

        Label(self.win, text="Connected to: " + target).grid(row=0, column=1)
        Label(self.win, text="IP addr:" + self.sbcon.devices[target]).grid(row=1, column=1)

        self.win.mainloop()

    def switch(self):
        self.sbcon.select_phase(self.curphase.get())
        self.dispphase.set(self.sbcon.get_phase())

    def exit(self):
        sys.exit(0)

if __name__ == "__main__":
    gui = ManualController("AC PAM Mux")
