import time
import io_functions as io
import gpiozero as gpio
import prog
import my_timer
import security_functions as security


#timers
light_timer = my_timer.MyTimer(period=0.5, auto_refresh=True)
taillight_timer = my_timer.MyTimer()

#outputs
power12v = gpio.LED(5)
light = gpio.LED(16)
left_turn_signal = gpio.LED(26)
right_turn_signal = gpio.LED(19)
ir_light = gpio.LED(20)
brake_light = gpio.LED(13)
taillight = gpio.LED(6)

#global variable
turn_signal_activated = 0.0
light_on_time = 0.0
prev_light = 0

prog.start()
while prog.isRunning():
    #output dictionary
    outputs = io.getOutputs()
    if outputs != None:
        
        #12v power
        power12v_state = outputs["power_12v"]
        if power12v_state == 0:
            power12v.off()
        elif power12v_state == 1:
            power12v.on()
        
        #light
        light_state = outputs["light"]
        if light_state == 0:
            light.off()
        elif light_state == 1:
            light.on()
        elif light_state == 2:
            if light_timer.getState() == 0:
                light.off()
            else:
                light.on()
        #turn off lights in lock and home mode after a while
        lock_state = security.lockState()
        if lock_state == '1' or lock_state == '2':
            if prev_light == 0 and (light_state == 1 or light_state == 2):
                light_on_time = time.time()
            elif light_state == 1 or light_state == 2:
                if time.time() - light_on_time >= 600:
                    io.lightOff()
                    prog.namePrint("Automatic light off")
        prev_light = light_state
        
        #turn signal
        turn_signal_state = outputs["turn_signal"]
        if turn_signal_state == 0:
            left_turn_signal.off()
            right_turn_signal.off()
        elif turn_signal_state == 1: #left turn
            left_turn_signal.on()
            right_turn_signal.off()
            turn_signal_activated = time.time()
        elif turn_signal_state == 2: #right turn
            left_turn_signal.off()
            right_turn_signal.on()
            turn_signal_activated = time.time()
        elif turn_signal_state == 3: #both lights
            left_turn_signal.on()
            right_turn_signal.on()
            turn_signal_activated = time.time()
        
        #ir light
        ir_light_state = outputs["ir_light"]
        if ir_light_state == 0:
            ir_light.off()
        elif ir_light_state == 1:
            ir_light.on()
        
        #brake light
        brake_state = outputs["brake"]
        if brake_state == 0:
            brake_light.off()
        elif brake_state == 1:
            brake_light.on()

        #taillight
        taillight_state = outputs["taillight"]
        # change to shutting off VESC
        if taillight_state == 1:
            taillight.off()
        elif taillight_state == 0:
            taillight.on()
        
#         if time.time() - turn_signal_activated < 0.5 and taillight_state == 1:
#             taillight_state = 2; #disable taillight blinking when turn signal is on
#         if taillight_state == 0:
#             taillight.off()
#         elif taillight_state == 1:
#             if brake_state == 0: #when not braking, blink slowly
#                 if taillight_timer.passed():
#                     if taillight_timer.getState() == 0:
#                         taillight.on()#on for 0.2s
#                         taillight_timer.refresh(new_period=0.2)
#                     else:
#                         taillight.off() #off for 1s
#                         taillight_timer.refresh(new_period=1)
#             else: #when braking, blink rapidly
#                 taillight_timer.period = 0.2 #blink at 0.2s on/off  period
#                 if taillight_timer.passed():
#                     if taillight_timer.getState() == 0:
#                         taillight.on()
#                         taillight_timer.refresh()
#                     else:
#                         taillight.off()
#                         taillight_timer.refresh()
#         elif taillight_state == 2:
#             if brake_state: #when turn signal on, turn on when braking and no blink
#                 taillight.on()
#             else:
#                 taillight.off()
    
    time.sleep(0.01)

