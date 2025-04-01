import time
import io_functions as io
import gpiozero as gpio
import prog


#digital inputs
button_1 = gpio.Button(23, hold_time=0.3)
button_2 = gpio.Button(24, hold_time=0.3)
brake_switch = gpio.Button(21, pull_up=None, active_state=False)

prog.start()
while prog.isRunning():
    #info dictionary
    infos = io.getInfos()
    
    #button 1
    if button_1.is_held:
        infos["button_1"] = 1
    else:
        infos["button_1"] = 0
    
    #button 2
    if "button_2" in infos.keys() and infos["button_2"] == 0 and button_2.is_held:
        io.toggleLight() #toggle lights when pressed
    if button_2.is_held:
        infos["button_2"] = 1
    else:
        infos["button_2"] = 0
    
    #brake switch
    if brake_switch.is_pressed:
        io.setOutput("brake", 1)
        infos["brake"] = 1
    else:
        io.setOutput("brake", 0)
        infos["brake"] = 0
    
    #write inputs(info) to a file
    io.writeInfos(infos)
    time.sleep(0.01)
    
