import time
import prog
import email_functions as email
import io_functions as io


class Battery():
    def __init__(self, low_vol, dis_vol=2.5, buffer=1):
        self.voltage = 0
        self.previous_voltage = 0
        self.low_voltage = low_vol
        self.disconnect_voltage = dis_vol
        self.buffer=buffer
        self.disconnected = False
        self.low = False

    def update_voltage(self, vol):
        self.previous_voltage = self.voltage #update previous voltage
        self.voltage = vol #update voltage
        if self.previous_voltage < self.disconnect_voltage-self.buffer:
            self.disconnected = True
        elif self.previous_voltage > self.disconnect_voltage+self.buffer:
            self.disconnected = False
        if self.previous_voltage < self.low_voltage-self.buffer:
            self.low = True
        elif self.previous_voltage > self.low_voltage+self.buffer:
            self.low = False

    def disconnecting(self):
        if not self.disconnected:
            if self.previous_voltage > self.disconnect_voltage-self.buffer and self.voltage < self.disconnect_voltage-self.buffer:
                self.disconnected = True
                return True
        return False

    def connecting(self):
        if self.disconnected:
            if self.previous_voltage < self.disconnect_voltage+self.buffer and self.voltage > self.disconnect_voltage+self.buffer:
                self.disconnected = False
                return True
        return False

    def going_low(self):
        if not self.low:
            if self.previous_voltage > self.low_voltage-self.buffer and self.voltage < self.low_voltage-self.buffer:
                self.low = True
                return True
        return False

    def is_low(self):
        if self.voltage < self.low_voltage:
            return True
        else:
            return False


time.sleep(5)
main_battery = Battery(42, dis_vol=10, buffer=2)
aux_battery = Battery(9.3)

prog.start()
while prog.isRunning():
    b48 = io.mainBatteryVoltage()
    b12 = io.bus12Voltage()
    if b48 != None:
        main_battery.update_voltage(b48)
    if b12 != None:
        aux_battery.update_voltage(b12)
    
    #check main voltage
    if main_battery.going_low(): #if main battery low voltage
        prog.namePrint('Main Battery Low!')
        email.sendPhotoEmail(subject="Battery Alearts",
                             message=time.strftime("Main Battery Low Voltage!\n%c"))
    if main_battery.disconnecting(): #if main battery disconnected
        prog.namePrint('--Main Battery Disconnected!')
        email.sendPhotoEmail(subject="Battery Alearts",
                             message=time.strftime("Main Battery Disconnected!\n%c"))
    elif main_battery.connecting(): #if main battery connected
        prog.namePrint('--Main Battery Connected!')
        email.sendPhotoEmail(subject="Battery Alearts",
                             message=time.strftime("Main Battery Connected!\n%c"))

    #check auxilary voltage
    if aux_battery.going_low(): #if auxilary battery low voltage
        prog.namePrint('--Aux Battery Low!')
        email.sendPhotoEmail(subject="Battery Alearts",
                             message=time.strftime("Auxilary Battery Low Voltage!\n%c"))

    time.sleep(1) #wait a bit


prog.end()
