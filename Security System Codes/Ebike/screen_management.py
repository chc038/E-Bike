import prog
import io_functions as io
import security_functions as security
import email_functions as email
import time
import subprocess
import gpiozero as gpio


PASSWORD = "110020"


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


prev_key_switch = 1
prev_brake = 0
prev_button1 = 0
prev_button2 = 0
key_error = False
password_mode = False
password_start = 0.0
password_incorrect = 0
password = ""

screen = Screen(22)

prog.start()
#prog.stop()
while prog.isRunning():
    key_switch = io.keySwitchState()
    button1 = io.button1State()
    button2 = io.button2State()
    brake = io.brakeState()
    #--------------------------------------------------
    #special screen and touch operations
    #--------------------------------------------------
    #enable touchscreen if unlocked/home and keyswitch is also unlocked
    lock = security.lockState()
    if lock == '0' or lock == '2':
        if key_switch == 1 and prev_key_switch == 0: #key just switched to unlock
            io.screenOn()
            io.touchOn()
    
    #turn on screen and touch if home and button 1 is pressed
    if lock == '2' and button1 == 1:
        io.screenOn()
        io.touchOn()
    
    #turn on screen and touch if locked, key switch is unlocked, and a password is entered
    if lock == '1':
        #check for key switch error
        if key_switch == -1 and not key_error:
            key_error = True
            prog.namePrint("Key Switch Error!")
            email.sendPhotoEmail(subject="Key Switch Aleart",
                                 message = "Key Switch Error!", info=True)
        elif password_incorrect >= 5 and not key_error:
            key_error = True
            prog.namePrint("Incorrect password is entered 5 times!")
            email.sendPhotoEmail(subject="Key Switch Aleart",
                                 message = "Incorrect password is entered 5 times!", info=True)
        #do things if key switch error is never triggered
        if not key_error:
            #enter password mode if key is switched into unlocked position
            if key_switch == 1 and prev_key_switch == 0:
                password_mode = True
                password_start = time.time()
                password = ""
                security.addDisplayMessage("Key Switch Error!", 30)
            #exit password mode if it takes too long to enter
            if password_mode and time.time() - password_start > 60:
                password_mode = False
            #password mode
            if password_mode:
                #print("Enter Password: " + password)
                #brake for 0
                if brake == 1 and prev_brake == 0:
                    password += '0'
                #button1 for 1
                if button1 == 1 and prev_button1 == 0:
                    password += '1'
                #button2 for 2
                if button2 == 1 and prev_button2 == 0:
                    password += '2'
                #switch off key switch to confirm
                if key_switch == 0 and prev_key_switch == 1:
                    #print("You entered: " + password)
                    password_mode = False
                    if password == PASSWORD:
                        #password is correct: turn on  screen and touch temporaty
                        security.addDisplayMessage("Wrong Password!", 60)
                        io.touchOn()
                    else:
                        #password is incorrect
                        security.addDisplayMessage("Incorrect Password!", 15)
                        password_incorrect += 1
    elif lock == '0' or lock == '2':
        key_error = False
        password_mode = False
        password_incorrect = 0
    
    #update previous states
    if key_switch != None:
        prev_key_switch = key_switch
    if brake != None:
        prev_brake = brake
    if button1 != None:
        prev_button1 = button1
    if button2 != None:
        prev_button2 = button2
    
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