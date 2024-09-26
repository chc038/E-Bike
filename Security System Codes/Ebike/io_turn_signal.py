import time
import io_functions as io
import gpiozero as gpio
import prog
import my_timer


#timer
turn_signal_timer = my_timer.MyTimer(period=0.3, auto_refresh=True)

#gpio input
left_turn_switch = gpio.Button(25)
right_turn_switch = gpio.Button(12)

prog.start()
while prog.isRunning():
     #turn signal switch
    if left_turn_switch.is_pressed: #left turn signal
        if turn_signal_timer.passed():
            turn_signal_timer.refresh()
        if turn_signal_timer.getState() == 0:
            io.setOutput("turn_signal", 0)
        else:
            io.setOutput("turn_signal", 1)
    elif False:#right_turn_switch.is_pressed: #right turn signal
        if turn_signal_timer.passed():
            turn_signal_timer.refresh()
        if turn_signal_timer.getState() == 0:
            io.setOutput("turn_signal", 0)
        else:
            io.setOutput("turn_signal", 2)
    else: #no turn signal
        io.setOutput("turn_signal", 0)
    
    time.sleep(0.01)
