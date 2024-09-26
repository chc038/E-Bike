import prog
import io_functions as io
import security_functions as security
import email_functions as email
import time
import subprocess
import gpiozero as gpio


class Screen():
    def __init__(self, pin):
        self.ctrl = gpio.LED(pin)
        self.screen_sts = self.checkScreen()
        self.touch_sts = 0
        self.time = time.time()
    
    def checkScreen(self):
        info = subprocess.run("xinput --list", shell=True, capture_output=True).stdout
        return "TSTP MTouch" in str(info)
    
    def toggle(self):
        self.ctrl.on()
        time.sleep(0.25)
        self.ctrl.off()
        self.time = time.time()
    
    def runManyTimes(self, command):
        for _ in range(200):
            try:
                subprocess.run(command, shell=True, check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                time.sleep(0.1)
        return False

    def enableTouch(self):
        suc = self.runManyTimes('xinput enable "TSTP MTouch"')
        if suc:
            print(__file__ + ": Touchscreen Enabled")
        else:
            print(__file__ + ": Error enabling touchscreen!")
    
    def disableTouch(self):
        suc = self.runManyTimes('xinput disable "TSTP MTouch"')
        if suc:
            print(__file__ + ": Touchscreen Disabled")
        else:
            print(__file__ + ": Error disabling touchscreen!")
    
    def update(self, screen_sts, touch_sts):
        if time.time() - self.time > 5:
            #turn screen on or off
            if screen_sts == 0 and self.screen_sts:
                #screen off
                self.toggle()
                self.screen_sts = False
            elif screen_sts == 1 and not self.screen_sts:
                #screen on
                self.toggle()
                self.screen_sts = True
                if touch_sts == 0:
                    time.sleep(1)
                    self.disableTouch()
            elif screen_sts == 2:
                #screen toggle
                self.toggle()
                return int(self.screen_sts)
            #turn touch on or off
            if self.touch_sts != touch_sts:
                if touch_sts == 0:
                    self.disableTouch()
                elif touch_sts == 1:
                    self.enableTouch()
                self.touch_sts = touch_sts
        return None


key_error = False
unlock_count = 0
key_switch_reset = False
key_switch_reset_count = 0

screen = Screen(22)

prog.start()
#prog.stop()
while prog.isRunning():
    key_switch = io.keySwitchState()
    button1 = io.button1State()
    button2 = io.button2State()
    brake = io.brakeState()
    lock = security.lockState()
    #--------------------------------------------------
    #special screen and touch operations
    #--------------------------------------------------
    
    #turn on screen and touch if unlocked/home and button 1 is pressed
    if lock == '0' or lock == '2':
        if button1 == 1:
            io.screenOn()
            io.touchOn()
    
    #unlock if locked and key switch is activated
    if lock == '1':
        #make sure the key was not in the unlock position
        if not key_switch_reset and key_switch == 0:
            key_switch_reset_count += 1
            if key_switch_reset_count >= 10:
                key_switch_reset = True
        elif key_switch_reset_count > 1:
            key_switch_reset_count -= 1
        if key_switch_reset:
            #check for key switch error
            if key_switch == -1 and not key_error:
                key_error = True
                prog.namePrint("Key Switch Error!")
                email.sendPhotoEmail(subject="Key Switch Aleart",
                                     message = "Key Switch Error!", info=True)
            #check for key switch activation
            if not key_error and key_switch == 1:
                unlock_count += 1
                if unlock_count > 10:
                    #unlock system
                    prog.namePrint("Unlock by Key Switch")
                    security.unlockSequence()
                    unlock_count = 0
                    
            elif unlock_count > 1:
                unlock_count -= 1
    else:
        key_error = False
        key_switch_reset = False

            
    
    #--------------------------------------------------
    #manage touch when screen is on
    #--------------------------------------------------
    screen_state = io.screenState()
    touch_state = io.touchState()
    if screen_state != None and touch_state != None:
        screen_state_new = screen.update(screen_state, touch_state)
        if screen_state_new != None:
            io.setOutput("screen", screen_state_new)
    
    time.sleep(0.1)


prog.end()