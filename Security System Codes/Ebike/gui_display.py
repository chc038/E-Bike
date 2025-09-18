from tkinter import *
import tkinter.font
import time
import io_functions as io
import security_functions as security
import gps_functions as gps
import email_functions as email
import camera_functions as camera
import prog
import subprocess
from PIL import ImageTk #sudo apt-get install python3-pil.imagetk


class Spacers():
    def __init__(self, parent, width, height, color, amount=1):
        self.amount = amount
        self.spacers = []
        for _ in range(self.amount):
            spacer = Canvas(parent, height=height, width=width, background=color, borderwidth=0, highlightthickness=0)
            self.spacers.append(spacer)

    def updateWidth(self, width):
        width = round(width+0.4, 0)
        old_width = self.spacers[0].winfo_width()
        if width != old_width:
            for spacer in self.spacers:
                spacer.configure(width=width)


class RadiobottonTab():
    def __init__(self, parent, vals, update_func, rw, cl, font, background,
                 pad=2, title='', mark='---', color_sequence=('red', 'green', 'cyan')):
        self.update_func = update_func
        self.color_sequence = color_sequence
        self.variable = IntVar()
        self.label = Label(parent, text=title, font=font, width=12) 
        self.label.grid(row=rw, column=cl, padx=pad, pady=pad) #label the thing to be controlled
        mark = Label(parent, text=mark, font=font, background=background)
        mark.grid(row=rw, column=cl+1, pady=pad) #makrer seperating the name and controls
        frame = Frame(parent)
        frame.grid(row=rw, column=cl+2, sticky=E, padx=pad, pady=pad) #frame to hold the radiobuttons
        self.radiobuttons = {}
        for ind in range(len(vals)): #create radiobuttons with given values
            val, txt, function = vals[ind]
            button = Radiobutton(frame, text=txt, font=font, variable=self.variable, value=val,
                                 command=function, background=color_sequence[ind],
                                 activebackground=color_sequence[ind], indicatoron=False, width=7)
            button.pack(side=RIGHT)
            self.radiobuttons[str(val)] = (ind, txt, button, function)
    
    def update(self):
        value = self.update_func()
        if value != None:
            self.variable.set(value)
            ind = self.radiobuttons[str(value)][0]
            color = self.color_sequence[ind]
            self.label.configure(background=color)


class CameraInfoDisplay():
    def __init__(self, parent, background):
        #controls
        setting_frame = Frame(parent, background=background)
        setting_frame.pack(side=TOP, pady=5)
        BUTTON_FONT = tkinter.font.Font(family='Helvetica', size=16)
        self.light = RadiobottonTab(setting_frame, vals=((0,'OFF',io.lightOff),(1,'ON',io.lightOn),(2,'BLINK',io.lightBlink)),
                                    update_func=io.lightState, cl=1, rw=1, font=BUTTON_FONT, background=background, title='Light')
        self.ir_light = RadiobottonTab(setting_frame, vals=((0,'OFF',io.irLightOff),(1,'ON',io.irLightOn)),
                                       update_func=io.irLightState, cl=1, rw=3, font=BUTTON_FONT, background=background, title='IR Lights')
        self.taillight = RadiobottonTab(setting_frame, vals=((0,'OFF',io.taillightOff),(1,'ON',io.taillightOn)),
                                        update_func=io.taillightState, cl=1, rw=5, font=BUTTON_FONT, background=background, title='Taillights')
        #info
        CAM_INFO_WIDTH = 460
        SPEED_HEIGHT = 240
        SPD_FONT = tkinter.font.Font(family='Helvetica', size=200) 
        SPD_FONT_2 = tkinter.font.Font(family='Helvetica', size=10, weight='bold')
        self.speed_canv = Canvas(parent, width=CAM_INFO_WIDTH, height=SPEED_HEIGHT, 
                            borderwidth=0, highlightthickness=0, background=background)
        self.speed_txt = self.speed_canv.create_text(CAM_INFO_WIDTH/2, SPEED_HEIGHT*0.6,
                                         text='00.0', font=SPD_FONT, fill='white')
        self.speed_unit = self.speed_canv.create_text(CAM_INFO_WIDTH/2, SPEED_HEIGHT*0.95,
                                          text='mph', font=SPD_FONT_2, fill='white')
        self.speed_canv.pack(side=TOP, pady=3)
        #motor and turn signal
        MOTOR_HEIGHT = 150
        MOT_FONT = tkinter.font.Font(family='Helvetica', size=50)
        self.motor_canv = Canvas(parent, width=CAM_INFO_WIDTH, height=MOTOR_HEIGHT,
                            borderwidth=0, highlightthickness=0, background=background)
        self.vol_txt = self.motor_canv.create_text(CAM_INFO_WIDTH/2, MOTOR_HEIGHT*0.25,
                                         text='48.3 V', font=MOT_FONT, fill='white')
        self.pwr_txt = self.motor_canv.create_text(CAM_INFO_WIDTH/2, MOTOR_HEIGHT*0.75,
                                         text='-2350 W', font=MOT_FONT, fill='white')
        self.turn_sig_left = self.motor_canv.create_line(50-43, MOTOR_HEIGHT/2, 50+43, MOTOR_HEIGHT/2,
                                                         width=20, fill='yellow', arrow=FIRST, arrowshape=(40, 40, 24))
        self.turn_sig_right = self.motor_canv.create_line(CAM_INFO_WIDTH-50+43, MOTOR_HEIGHT/2,
                                                             CAM_INFO_WIDTH-50-43, MOTOR_HEIGHT/2,
                                                             width=20, fill='yellow', arrow=FIRST, arrowshape=(40, 40, 24))
        self.motor_canv.pack(side=TOP, pady=3)
        #gps buttons
        BUTTON_WIDTH = 8
        BUTTON_PADX = 30
        BUTTON_PADY = 3
        BUTTON_COLOR = 'light blue'
        gps_button_frame = Frame(parent, background=background)
        gps_button_frame.pack(side=TOP, pady=3)
        eml_gps_button = Button(gps_button_frame, command=emailGPS, height=1, width=BUTTON_WIDTH,
                                  text='Email GPS', font=BUTTON_FONT, background=BUTTON_COLOR, foreground='black')
        eml_gps_button.grid(row=1, column=1, padx=BUTTON_PADX, pady=BUTTON_PADY)
        eml_info_button = Button(gps_button_frame, command=emailInformation, height=1, width=BUTTON_WIDTH,
                                   text='Email Info', font=BUTTON_FONT, background=BUTTON_COLOR, foreground='black')
        eml_info_button.grid(row=2, column=1, padx=BUTTON_PADX, pady=BUTTON_PADY)
        cpy_gps_button = Button(gps_button_frame, command=copyGPS, height=1, width=BUTTON_WIDTH,
                                 text='Copy GPS', font=BUTTON_FONT, background=BUTTON_COLOR, foreground='black')
        cpy_gps_button.grid(row=1, column=2, padx=BUTTON_PADX, pady=BUTTON_PADY)
        cpy_info_button = Button(gps_button_frame, command=copyInfo, height=1, width=BUTTON_WIDTH,
                                 text='Copy Info', font=BUTTON_FONT, background=BUTTON_COLOR, foreground='black')
        cpy_info_button.grid(row=2, column=2, padx=BUTTON_PADX, pady=BUTTON_PADY)
    
    def update(self):
        #update ontrols
        self.light.update()
        self.ir_light.update()
        self.taillight.update()
        #update speed
        gps_speed = gps.getGPSSpeed()
        gps_age = gps.getGPSAge()
        spd_unt = prog.getUnit()
        speed = 0.0
        if gps_speed != None and gps_age != None and gps_age <= 2:
            speed = gps_speed
        if spd_unt == 0:
            self.speed_canv.itemconfigure(self.speed_txt, text=round(speed*3.6, 1))
            self.speed_canv.itemconfigure(self.speed_unit, text='km/h')
        elif spd_unt == 1:
            self.speed_canv.itemconfigure(self.speed_txt, text=round(speed*2.23694, 1))
            self.speed_canv.itemconfigure(self.speed_unit, text='mph')
        #update motor parameters
        main_current = io.mainBatteryCurrent()
        motor_voltage = io.motorInputVoltage()
        motor_current = io.motorInputCurrent()
        motor1_current = io.motor1InputCurrent()
        motor2_current = io.motor2InputCurrent()
        vesc_state = io.vescState()
        vesc1_state = io.vesc1State()
        vesc2_state = io.vesc2State()
        if main_current != None:
            if (vesc_state == 1 and vesc1_state == 1 and vesc2_state == 1 and motor_voltage != None
                and motor_current != None and motor1_current != None and motor2_current != None):
                total_current = main_current + motor_current + motor1_current + motor2_current
                total_power = motor_voltage*total_current
                self.motor_canv.itemconfigure(self.vol_txt, text=str(round(motor_voltage, 1))+" V")
                self.motor_canv.itemconfigure(self.pwr_txt, text=str(round(total_power/10)*10)+" W")
            elif vesc_state == 1 and motor_voltage != None and motor_current != None: #inly vesc20 is on
                total_current = main_current + motor_current
                total_power = motor_voltage*total_current
                self.motor_canv.itemconfigure(self.vol_txt, text=str(round(motor_voltage, 1))+" V")
                self.motor_canv.itemconfigure(self.pwr_txt, text=str(round(total_power/10)*10)+" W")
            elif vesc_state == 0: #vesc off, ignore vesc data
                self.motor_canv.itemconfigure(self.vol_txt, text=str("0.0 V"))
                self.motor_canv.itemconfigure(self.pwr_txt, text=str("0 W"))
            #update turn signal
            turn_sig_state = io.turnSignalState()
            if turn_sig_state == 0:
                self.motor_canv.itemconfigure(self.turn_sig_left, fill='')
                self.motor_canv.itemconfigure(self.turn_sig_right, fill='')
            elif turn_sig_state == 1:
                self.motor_canv.itemconfigure(self.turn_sig_left, fill='yellow')
                self.motor_canv.itemconfigure(self.turn_sig_right, fill='')
            elif turn_sig_state == 2:
                self.motor_canv.itemconfigure(self.turn_sig_left, fill='')
                self.motor_canv.itemconfigure(self.turn_sig_right, fill='yellow')


class MessageHandle():
    def __init__(self, manual_overide=60):
        self.messages = []
        self.message = {'message': "No Message", 'elapse': 0}
        self.manual_time = time.time() + 5
        self.manual_overide = manual_overide

    def currentMessage(self):
        if self.message['elapse'] < time.time():
            if len(self.messages) > 0:
                self.message = self.messages[0]
                self.messages[0:1] = []
                if time.time() > self.manual_time and security.lockState() != '0':
                    packDisplay("message")
                    io.screenOn()
                    prog.namePrint("Showing message display")
                prog.namePrint("Displaying message: " + str(self.message['message']))
            else:
                self.message = {'message': "No Message", 'elapse': 0}
                #go back to selected display and tuen off screen if locked
                if display_frames['message'].winfo_ismapped():
                    packDisplay(disp_button_var.get())
                    if security.lockState() == '1':
                        io.screenOff()
        return self.message['message']

    def addMessages(self, messages):
        if messages != None and len(messages) > 0:
            self.messages += messages

    def manualClick(self):
        """will not automitically switch to message display after manual_overide seconds of calling this function"""
        self.manual_time = time.time() + self.manual_overide

def packDisplay(display):
    for display_name in display_frames.keys():
        if display_name != display:
            display_frames[display_name].pack_forget()
    display_frames[display].pack(side=TOP)
def displaySelect():
    message_handle.manualClick()
    packDisplay(disp_button_var.get())

def updateInfoTopCanv(window_width):
    #update width of spacers
    spacer_width = ((window_width - TURN_SIG_WIDTH*2 - LIGHT_WIDTH - BRAKE_WIDTH - SCREEN_WIDTH - LOCK_WIDTH - TIME_WIDTH - 10)
                    / info_top_spacers.amount)
    info_top_spacers.updateWidth(spacer_width)
    #update turn signal
    turn_sig_state = io.turnSignalState()
    if turn_sig_state == 0:
        turn_sig_left_canv.itemconfigure(turn_sig_left, fill='')
        turn_sig_right_canv.itemconfigure(turn_sig_right, fill='')
    elif turn_sig_state == 1:
        turn_sig_left_canv.itemconfigure(turn_sig_left, fill='yellow')
        turn_sig_right_canv.itemconfigure(turn_sig_right, fill='')
    elif turn_sig_state == 2:
        turn_sig_left_canv.itemconfigure(turn_sig_left, fill='')
        turn_sig_right_canv.itemconfigure(turn_sig_right, fill='yellow')
    #update light status
    light_state = io.lightState()
    if light_state == 0:
        light_canv.itemconfigure('light', fill='')
    elif light_state == 1:
        light_canv.itemconfigure('light', fill='white')
    elif light_state == 2:
        light_canv.itemconfigure('light', fill='red')
    #update brake status
    brake_state = io.brakeState()
    if brake_state == 0:
        brake_canv.itemconfigure('brake', outline='')
    elif brake_state == 1:
        brake_canv.itemconfigure('brake', outline='white')
    #update chain tension status
    #chain_state = io.chainSensorState()
    chain_state = 0
    if chain_state == 0:
        brake_canv.itemconfigure(chain_txt, fill='')
    elif chain_state == 1:
        brake_canv.itemconfigure(chain_txt, fill='red')
    #update screen status
    screen_state = io.screenState()
    if screen_state == 0:
        screen_canv.itemconfigure(screen_fill, fill=BACKGROUND_COLOR)
        screen_canv.itemconfigure(screen_ind, fill='red')
    if screen_state == 1:
        screen_canv.itemconfigure(screen_fill, fill='black')
        screen_canv.itemconfigure(screen_ind, fill='light green')
    #update lock status
    lock_state = security.lockState()
    if lock_state == '0': #unlock
        lock_canv.itemconfigure('unlockF', fill='white')
        lock_canv.itemconfigure('both', fill='white')
        lock_canv.itemconfigure('unlockO', outline='white')
        lock_canv.itemconfigure('lockF', fill='')
        lock_canv.itemconfigure('home', fill='')
        lock_canv.itemconfigure('lockO', outline='')
    elif lock_state == '1': #lock
        lock_canv.itemconfigure('lockF', fill='white')
        lock_canv.itemconfigure('both', fill='white')
        lock_canv.itemconfigure('lockO', outline='white')
        lock_canv.itemconfigure('unlockF', fill='')
        lock_canv.itemconfigure('unlockO', outline='')
        lock_canv.itemconfigure('home', fill='')
    elif lock_state == '2': #home
        lock_canv.itemconfigure('home', fill='white')
        lock_canv.itemconfigure('unlockF', fill='')
        lock_canv.itemconfigure('lockF', fill='')
        lock_canv.itemconfigure('both', fill='')
        lock_canv.itemconfigure('unlockO', outline='')
        lock_canv.itemconfigure('lockO', outline='')
    #update time and date
    time_canv.itemconfigure(time_txt, text=time.strftime('%H:%M'))
    time_canv.itemconfigure(date_txt, text=time.strftime('%a %m/%d/%Y'))
    
def updateInfoMidCanv(window_width):
    #update width of spacers
    spacer_width = ((window_width - MOTOR_CANV_WIDTH - SPEED_CANV_WIDTH - OTHER_CANV_WIDTH - 2)
                    / info_mid_spacers.amount)
    info_mid_spacers.updateWidth(width=spacer_width)
    #update motor parameters
    main_current = io.mainBatteryCurrent()
    motor_voltage = io.motorInputVoltage()
    motor_current = io.motorInputCurrent()
    motor1_current = io.motor1InputCurrent()
    motor2_current = io.motor2InputCurrent()
    vesc_state = io.vescState()
    vesc1_state = io.vesc1State()
    vesc2_state = io.vesc2State()
    if main_current != None:
        if (vesc_state == 1 and vesc1_state == 1 and vesc2_state == 1 and motor_voltage != None
            and motor_current != None and motor1_current != None and motor2_current != None):
            total_current = main_current + motor_current + motor1_current + motor2_current
            total_power = motor_voltage*total_current
            motor_canv.itemconfigure(cur_txt, text=str(round(total_current, 1))+" A")
            motor_canv.itemconfigure(pwr_txt, text=str(round(total_power))+" W")
            motor_canv.itemconfigure(vol_txt, text=str(round(motor_voltage, 1))+" V")
        elif vesc_state == 1 and motor_voltage != None and motor_current != None: #only vesc 20 is on
            total_current = main_current + motor_current
            total_power = motor_voltage*total_current
            motor_canv.itemconfigure(cur_txt, text=str(round(total_current, 1))+" A")
            motor_canv.itemconfigure(pwr_txt, text=str(round(total_power))+" W")
            motor_canv.itemconfigure(vol_txt, text=str(round(motor_voltage, 1))+" V")
        elif vesc_state == 0: #vesc off, ignore vesc data
            motor_canv.itemconfigure(cur_txt, text=str(round(main_current, 1))+" A")
            motor_canv.itemconfigure(pwr_txt, text="0 W")
            motor_canv.itemconfigure(vol_txt, text="0 V")
    #update speed
    gps_speed = gps.getGPSSpeed()
    gps_age = gps.getGPSAge()
    motor_rpm = io.motorRPM()
    motor1_rpm = io.motor1RPM()
    motor2_rpm = io.motor1RPM()
    spd_unt = prog.getUnit()
    speed = 0.0 #m/s
    if gps_speed != None and gps_age != None and gps_age <= 2:
        speed = gps_speed
    elif vesc1_state == 1 and motor1_rpm != None:
        speed = motor1_rpm * 4.2089e-4
    elif vesc2_state == 1 and motor2_rpm != None:
        speed = motor2_rpm * 4.2089e-4
    elif vesc1_state == 0 and vesc2_state == 0 and motor_rpm != None:
        speed = motor_rpm * 0.07899
    if spd_unt == 0:
        speed_canv.itemconfigure(speed_txt, text=round(speed*3.6, 1))
        speed_canv.itemconfigure(speed_unit, text='km/h')
    elif spd_unt == 1:
        speed_canv.itemconfigure(speed_txt, text=round(speed*2.23694, 1))
        speed_canv.itemconfigure(speed_unit, text='mph')
    #update other information
    bus_voltage = io.bus12Voltage()
    if bus_voltage != None:
        other_canv.itemconfigure(vol_12v_txt, text=str(round(bus_voltage, 1))+"v")
    if vesc1_state == 0 and vesc2_state == 0:
        other_canv.itemconfigure(temp_name, fill='red')
        other_canv.itemconfigure(temp_txt, text="0c 0c")
    elif vesc_state == 1 and vesc2_state == 1:
        other_canv.itemconfigure(temp_name, fill='white')
        motor1_temp = io.motor1Temperature()
        motor2_temp = io.motor2Temperature()
        if motor1_temp != None and motor2_temp != None:
            other_canv.itemconfigure(temp_txt, text=str(round(motor1_temp))+ "c " +
                                     str(round(motor2_temp))+ "c")
    cpu_temp = io.cpuTemperature()
    memory = io.memory()
    if cpu_temp != None and memory != None:
        other_canv.itemconfigure(cpu_mem_txt, text=str(round(cpu_temp))+ "c " + str(memory))
    
    
def updateInfoBotCanv(window_width):
    #update width of spacers
    spacer_width = (window_width - DIST_WIDTH*2 - GPS_WIDTH - 10) / info_bot_spacers.amount
    info_bot_spacers.updateWidth(spacer_width)
    #update gps info
    gps_age = gps.getGPSAge()
    gps_location = gps.getGPSLocation()
    if gps_age != None and gps_location != None:
        if gps_age <= 2:
            gps_canv.itemconfigure(gps_sts, fill='black')
        else:
            gps_canv.itemconfigure(gps_sts, fill='red')
        gps_canv.itemconfigure(gps_txt, text=gps_location)
    #update distance info
    dst_unt = prog.getUnit()
    total_distance = io.totalDistance()
    if dst_unt == 0 and total_distance != None:
        total_dist_canv.itemconfigure(total_dist_unit, text="total km")
        total_dist_canv.itemconfigure(total_dist_txt, text=round(total_distance/1000, 1))
    elif dst_unt == 1 and total_distance != None:
        total_dist_canv.itemconfigure(total_dist_unit, text="total miles")
        total_dist_canv.itemconfigure(total_dist_txt, text=round(total_distance/1609, 1))
    trip_distance = io.tripDistance()
    if dst_unt == 0 and trip_distance != None:
        trip_dist_canv.itemconfigure(trip_dist_unit, text="trip km")
        trip_dist_canv.itemconfigure(trip_dist_txt, text=round(trip_distance/1000, 1))
    elif dst_unt == 1 and trip_distance != None:
        trip_dist_canv.itemconfigure(trip_dist_unit, text="trip miles")
        trip_dist_canv.itemconfigure(trip_dist_txt, text=round(trip_distance/1609, 1))
    
def updateInformation():
    window_width = root_window.winfo_width()
    updateInfoTopCanv(window_width)
    updateInfoMidCanv(window_width)
    updateInfoBotCanv(window_width)

def updateSetting():
    light.update()
    ir_light.update()
    taillight.update()
    power_12v.update()
    motor.update()
    screen_ctrl.update()
    touch_ctrl.update()
    unit.update()
    buzzer.update()
    virtual_fence.update()
    vibration_detection.update()
    vib_sensitivity.set(prog.vibrationSensitivity())

def updateMessage():
    message_txt.configure(text = message_handle.currentMessage())
    message_handle.addMessages(security.displayMessages())

def vibSenSetting():
    prog.vibSenSet(vib_sensitivity.get())

def lightTouchControl(event):
    if (LIGHT_WIDTH/2-55 < event.x and event.x < LIGHT_WIDTH/2+55 and
        INFO_TOP_HEIGHT/2-45 < event.y and event.y < INFO_TOP_HEIGHT/2+45):
        io.toggleLight()
def screenTouchControl(event):
    if (SCREEN_WIDTH/2-65 < event.x and event.x < SCREEN_WIDTH/2+65 and
        INFO_TOP_HEIGHT/2-40 < event.y and event.y < INFO_TOP_HEIGHT/2+40):
        io.toggleScreen()
def lockTouchControl(event):
    if (LOCK_WIDTH/2-40 < event.x and event.x < LOCK_WIDTH/2+45 and
        INFO_TOP_HEIGHT/2-40 < event.y and event.y < INFO_TOP_HEIGHT/2+40):
        if INFO_TOP_HEIGHT/2 < event.y:
            security.homeSequence()
        elif LOCK_WIDTH/2 < event.x:
            security.lockSequence()
        else:
            security.unlockSequence()

def emailGPS():
    gps_info = gps.getGPSLocation()
    email.sendEmail(subject="Ebike Information", message=gps_info)
    prog.namePrint("Emailed GPS")
def emailInformation():
    info = "\n" + '-'*30 + "\n" + time.strftime('%c') + "\n" + '-'*30 + "\n"
    info += gps.strfGPSInfo()
    info += io.strfOutputs() + io.strfInfos() + io.strfInfosADC() + io.strfInfosVESC()
    info += security.securityInfo()
    email.sendPhotoEmail(subject="Ebike Information", message=info)
    prog.namePrint("Emailed Information")
def copyGPS():
    try:
        gps_info = gps.getGPSLocation()
        subprocess.run('echo "'+ gps_info +'" | xsel --clipboard --input', shell=True)
        prog.namePrint("Copied GPS location to clipboard")
    except Exception:
        prog.namePrint("Failed to copy GPS location")
def copyInfo():
    try:
        info = "\n" + '-'*30 + "\n" + time.strftime('%c') + "\n" + '-'*30 + "\n"
        info += gps.strfGPSInfo()
        info += io.strfOutputs() + io.strfInfos() + io.strfInfosADC() + io.strfInfosVESC()
        info += security.securityInfo()
        subprocess.run('echo "'+ info +'" | xsel --clipboard --input', shell=True)
        prog.namePrint("Copied Information to clipboard")
    except Exception:
        prog.namePrint("Failed to copy Information")


#--------------------------------------------------
#root window for all displays
#--------------------------------------------------
BACKGROUND_COLOR = 'blue'
root_window = Tk()
root_window.title("Ebike Dashboard")
root_window.configure(background=BACKGROUND_COLOR)
root_window.protocol("WM_DELETE_WINDOW", prog.stop)
display_frames = {}

#radiobottoms for selecting display
disp_button_frame = Frame(root_window, background=BACKGROUND_COLOR)
disp_button_frame.pack(side=TOP)
DISP_BUTTON_COLOR = 'light blue'
DISP_BUTTON_FONT = tkinter.font.Font(family='Helvetica', size=25)
disp_button_var = StringVar(value="information")
info_button = Radiobutton(disp_button_frame, indicatoron=False,
                          text="Information", font=DISP_BUTTON_FONT, width=10,
                          command=displaySelect,
                          variable=disp_button_var, value="information",
                          background=DISP_BUTTON_COLOR, selectcolor=BACKGROUND_COLOR)
info_button.pack(side=LEFT, padx=3)
setting_button = Radiobutton(disp_button_frame, indicatoron=False,
                          text="Setting", font=DISP_BUTTON_FONT, width=10,
                          command=displaySelect,
                          variable=disp_button_var, value="setting",
                          background=DISP_BUTTON_COLOR, selectcolor=BACKGROUND_COLOR)
setting_button.pack(side=LEFT, padx=3)
message_button = Radiobutton(disp_button_frame, indicatoron=False,
                          text="Message", font=DISP_BUTTON_FONT, width=10,
                          command=displaySelect,
                          variable=disp_button_var, value="message",
                          background=DISP_BUTTON_COLOR, selectcolor=BACKGROUND_COLOR)
message_button.pack(side=LEFT, padx=3)
lock_cam_button = Radiobutton(disp_button_frame, indicatoron=False,
                          text="Lock Cam", font=DISP_BUTTON_FONT, width=10,
                          command=displaySelect,
                          variable=disp_button_var, value="lock_cam",
                          background=DISP_BUTTON_COLOR, selectcolor=BACKGROUND_COLOR)
lock_cam_button.pack(side=LEFT, padx=3)


#--------------------------------------------------
#information display
#--------------------------------------------------
display_frames['information'] = Frame(root_window, background=BACKGROUND_COLOR)
#--------------------------------------------------
#top frame for functional displays
#--------------------------------------------------
INFO_TOP_HEIGHT = 150
info_top_frame = Frame(display_frames['information'], background=BACKGROUND_COLOR)
info_top_frame.pack(side=TOP)
#turn signal
TURN_SIG_WIDTH = 150
turn_sig_left_canv = Canvas(info_top_frame, width=TURN_SIG_WIDTH, height=INFO_TOP_HEIGHT,
                            background=BACKGROUND_COLOR, highlightthickness=0)
turn_sig_left = turn_sig_left_canv.create_line(TURN_SIG_WIDTH/2-60, INFO_TOP_HEIGHT/2,
                                               TURN_SIG_WIDTH/2+60, INFO_TOP_HEIGHT/2,
                                               width=30, fill='yellow', arrow=FIRST, arrowshape=(50, 50, 30))
turn_sig_right_canv = Canvas(info_top_frame, width=TURN_SIG_WIDTH, height=INFO_TOP_HEIGHT,
                            background=BACKGROUND_COLOR, highlightthickness=0)
turn_sig_right = turn_sig_right_canv.create_line(TURN_SIG_WIDTH/2+60, INFO_TOP_HEIGHT/2,
                                               TURN_SIG_WIDTH/2-60, INFO_TOP_HEIGHT/2,
                                               width=30, fill='yellow', arrow=FIRST, arrowshape=(50, 50, 30))
#light
LIGHT_WIDTH = 140
light_canv = Canvas(info_top_frame, width=LIGHT_WIDTH, height=INFO_TOP_HEIGHT,
                    background=BACKGROUND_COLOR, highlightthickness=0)
light_canv.create_oval(LIGHT_WIDTH/2-15, INFO_TOP_HEIGHT/2-45, LIGHT_WIDTH/2+5, INFO_TOP_HEIGHT/2+45, tag='light',
                          width=5, outline='white', fill='white')
light_canv.create_arc(LIGHT_WIDTH/2-55, INFO_TOP_HEIGHT/2-45, LIGHT_WIDTH/2+45, INFO_TOP_HEIGHT/2+45,
                         width=5, outline='white', start=90, extent=180, style=ARC)
light_canv.create_line(LIGHT_WIDTH/2+15, INFO_TOP_HEIGHT/2-25, LIGHT_WIDTH/2+55, INFO_TOP_HEIGHT/2-25, tag='light',
                          width=5, fill='white', dash=(15,10))
light_canv.create_line(LIGHT_WIDTH/2+15, INFO_TOP_HEIGHT/2, LIGHT_WIDTH/2+55, INFO_TOP_HEIGHT/2, tag='light',
                          width=5, fill='white', dash=(15,10))
light_canv.create_line(LIGHT_WIDTH/2+15, INFO_TOP_HEIGHT/2+25, LIGHT_WIDTH/2+55, INFO_TOP_HEIGHT/2+25, tag='light',
                          width=5, fill='white', dash=(15,10))
light_canv.bind('<Button-1>', lightTouchControl)
#brake
BRAKE_WIDTH = 130
brake_canv = Canvas(info_top_frame, width=BRAKE_WIDTH, height=INFO_TOP_HEIGHT,
                    background=BACKGROUND_COLOR, highlightthickness=0)
brake_canv.create_oval(BRAKE_WIDTH/2-40, INFO_TOP_HEIGHT/2-40, BRAKE_WIDTH/2+40, INFO_TOP_HEIGHT/2+40, tag='brake',
                       width=5, outline='white')
brake_canv.create_arc(BRAKE_WIDTH/2-50, INFO_TOP_HEIGHT/2-50, BRAKE_WIDTH/2+50, INFO_TOP_HEIGHT/2+50, tag='brake',
                      width=5, outline='white', start=-45, extent=90, style=ARC)
brake_canv.create_arc(BRAKE_WIDTH/2-50, INFO_TOP_HEIGHT/2-50, BRAKE_WIDTH/2+50, INFO_TOP_HEIGHT/2+50,
                      tag='brake', width=5, outline='white', start=135, extent=90, style=ARC)
chain_txt = brake_canv.create_text(BRAKE_WIDTH/2, INFO_TOP_HEIGHT/2,
                                   text="!", font=tkinter.font.Font(family='Helvetica', size=50), fill='red')
#screen
SCREEN_WIDTH = 160
screen_canv = Canvas(info_top_frame, width=SCREEN_WIDTH, height=INFO_TOP_HEIGHT,
                     background=BACKGROUND_COLOR, highlightthickness=0)
screen_canv.create_rectangle(SCREEN_WIDTH/2-65, INFO_TOP_HEIGHT/2-40, SCREEN_WIDTH/2+65, INFO_TOP_HEIGHT/2+40,
                             width=0, fill='white')
screen_fill = screen_canv.create_rectangle(SCREEN_WIDTH/2-55, INFO_TOP_HEIGHT/2-30,
                                           SCREEN_WIDTH/2+55, INFO_TOP_HEIGHT/2+30, width=0, fill='black')
screen_ind = screen_canv.create_oval(SCREEN_WIDTH/2-3, INFO_TOP_HEIGHT/2+32, SCREEN_WIDTH/2+3, INFO_TOP_HEIGHT/2+38,
                                     width=0, fill='red')
screen_canv.bind('<Button-1>', screenTouchControl)
#lock
LOCK_WIDTH = 110
lock_canv = Canvas(info_top_frame, width=LOCK_WIDTH, height=INFO_TOP_HEIGHT,
                   background=BACKGROUND_COLOR, highlightthickness=0)
lock_canv.create_arc(LOCK_WIDTH/2, INFO_TOP_HEIGHT/2-45, LOCK_WIDTH/2+40, INFO_TOP_HEIGHT/2-5, tag='lockO',
                     outline='white', width=5, start=0, extent=180, style=ARC) #lock
lock_canv.create_arc(LOCK_WIDTH/2-40, INFO_TOP_HEIGHT/2-45, LOCK_WIDTH/2, INFO_TOP_HEIGHT/2-5, tag='unlockO',
                     outline='white', width=5, start=0, extent=180, style=ARC) #unlock
lock_canv.create_line(LOCK_WIDTH/2+40, INFO_TOP_HEIGHT/2-25, LOCK_WIDTH/2+40, INFO_TOP_HEIGHT/2-5, tag='lockF',
                      fill='white', width=5) #lock
lock_canv.create_line(LOCK_WIDTH/2-40, INFO_TOP_HEIGHT/2-25, LOCK_WIDTH/2-40, INFO_TOP_HEIGHT/2-5, tag='unlockF',
                      fill='white', width=5) #unlock
lock_canv.create_line(LOCK_WIDTH/2, INFO_TOP_HEIGHT/2-25, LOCK_WIDTH/2, INFO_TOP_HEIGHT/2-5, tag='both',
                      fill='white', width=5) #lock & unlock
lock_canv.create_rectangle(LOCK_WIDTH/2-5, INFO_TOP_HEIGHT/2-5, LOCK_WIDTH/2+45, INFO_TOP_HEIGHT/2+45, tag='both',
                           fill='white', width=0) #lock & unlock
lock_canv.create_rectangle(LOCK_WIDTH/2-25, INFO_TOP_HEIGHT/2-5, LOCK_WIDTH/2+25, INFO_TOP_HEIGHT/2+45, tag='home',
                           fill='white', width=0) #home
lock_canv.create_polygon(LOCK_WIDTH/2, INFO_TOP_HEIGHT/2-45, LOCK_WIDTH/2+40, INFO_TOP_HEIGHT/2-5,
                         LOCK_WIDTH/2-40, INFO_TOP_HEIGHT/2-5, tag='home',
                         fill='white', width=0) #home
lock_canv.bind('<Button-1>', lockTouchControl)
#time and Date
TIME_WIDTH = 250
TIME_FONT = tkinter.font.Font(family='Helvetica', size=70)
DATE_FONT = tkinter.font.Font(family='Helvetica', size=25)
time_canv = Canvas(info_top_frame, width=TIME_WIDTH, height=INFO_TOP_HEIGHT,
                   background=BACKGROUND_COLOR, highlightthickness=0)
time_txt = time_canv.create_text(TIME_WIDTH/2, 65, text='00:00', font=TIME_FONT, fill='black')
date_txt = time_canv.create_text(TIME_WIDTH/2, 125, text='Mon 01/01/2000', font=DATE_FONT, fill='black')
#spacers
info_top_spacers = Spacers(info_top_frame, width=10, height=INFO_TOP_HEIGHT, color=BACKGROUND_COLOR, amount=6)
#pack things into info top frame
turn_sig_left_canv.pack(side=LEFT)
info_top_spacers.spacers[0].pack(side=LEFT)
turn_sig_right_canv.pack(side=RIGHT)
info_top_spacers.spacers[1].pack(side=RIGHT)
light_canv.pack(side=LEFT)
info_top_spacers.spacers[2].pack(side=LEFT)
lock_canv.pack(side=RIGHT)
info_top_spacers.spacers[3].pack(side=RIGHT)
brake_canv.pack(side=LEFT)
info_top_spacers.spacers[4].pack(side=LEFT)
screen_canv.pack(side=RIGHT)
info_top_spacers.spacers[5].pack(side=RIGHT)
time_canv.pack(side=LEFT)
#--------------------------------------------------
#middle frame for speed and other parameters
#--------------------------------------------------
INFO_MID_HEIGHT = 350
INFO_MID_COLOR = 'black'
info_mid_frame = Frame(display_frames['information'], background=INFO_MID_COLOR)
info_mid_frame.pack(side=TOP)
#motor parameters
MOTOR_CANV_WIDTH = 300
MOTOR_FONT = tkinter.font.Font(family='Helvetica', size=60)
MOTOR_FONT_2 = tkinter.font.Font(family='Helvetica', size=15, weight='bold')
motor_canv = Canvas(info_mid_frame, height=INFO_MID_HEIGHT, width=MOTOR_CANV_WIDTH,
                    borderwidth=0, highlightthickness=0, background=INFO_MID_COLOR)
motor_canv.create_text(MOTOR_CANV_WIDTH/2, INFO_MID_HEIGHT*0.075,
                       text='main battery', font=MOTOR_FONT_2, fill='white', anchor=CENTER)
pwr_txt = motor_canv.create_text(MOTOR_CANV_WIDTH/2, INFO_MID_HEIGHT*0.275,
                                 text='1000 W', font=MOTOR_FONT, fill='white')
vol_txt = motor_canv.create_text(MOTOR_CANV_WIDTH/2, INFO_MID_HEIGHT*0.55,
                                 text='48.1 V', font=MOTOR_FONT, fill='white')
cur_txt = motor_canv.create_text(MOTOR_CANV_WIDTH/2, INFO_MID_HEIGHT*0.825,
                                 text='10.1 A', font=MOTOR_FONT, fill='white')
#speed
SPEED_CANV_WIDTH = 600
SPEED_FONT = tkinter.font.Font(family='Helvetica', size=225) 
SPEED_FONT_2 = tkinter.font.Font(family='Helvetica', size=20, weight='bold')
SPEED_FONT_3 = tkinter.font.Font(family='Helvetica', size=15, weight='bold')
speed_canv = Canvas(info_mid_frame, height=INFO_MID_HEIGHT, width=SPEED_CANV_WIDTH,
                    borderwidth=0, highlightthickness=0, background=INFO_MID_COLOR)
speed_canv.create_text(SPEED_CANV_WIDTH/2, INFO_MID_HEIGHT*0.06,
                       text='speed', font=SPEED_FONT_3, fill='white')
speed_txt = speed_canv.create_text(SPEED_CANV_WIDTH/2, INFO_MID_HEIGHT*0.575,
                                 text='00.0', font=SPEED_FONT, fill='white')
speed_unit = speed_canv.create_text(SPEED_CANV_WIDTH/2, INFO_MID_HEIGHT*0.9,
                                  text='mph', font=SPEED_FONT_2, fill='white')
#other information
OTHER_CANV_WIDTH = 300
OTHER_FONT = tkinter.font.Font(family='Helvetica', size=50)
OTHER_FONT_2 = tkinter.font.Font(family='Helvetica', size=15, weight='bold')
other_canv = Canvas(info_mid_frame, height=INFO_MID_HEIGHT, width=OTHER_CANV_WIDTH,
                    borderwidth=0, highlightthickness=0, background=INFO_MID_COLOR)
vol_12v_name = other_canv.create_text(OTHER_CANV_WIDTH/2, INFO_MID_HEIGHT*0.075,
                                 text="12v bus", font=OTHER_FONT_2, fill='white')
vol_12v_txt = other_canv.create_text(OTHER_CANV_WIDTH/2, INFO_MID_HEIGHT*0.225,
                                     text="12.1v", font=OTHER_FONT, fill='white')
temp_name = other_canv.create_text(OTHER_CANV_WIDTH/2, INFO_MID_HEIGHT*0.3875,
                                 text="motor 1 / motor 2", font=OTHER_FONT_2, fill='white')
temp_txt = other_canv.create_text(OTHER_CANV_WIDTH/2, INFO_MID_HEIGHT*0.5375,
                                     text="20c 30c", font=OTHER_FONT, fill='white')
cpu_mem_name = other_canv.create_text(OTHER_CANV_WIDTH/2, INFO_MID_HEIGHT*0.7,
                                 text="cpu / memory", font=OTHER_FONT_2, fill='white')
cpu_mem_txt = other_canv.create_text(OTHER_CANV_WIDTH/2, INFO_MID_HEIGHT*0.85,
                                     text="60c 100G", font=OTHER_FONT, fill='white')
#spacers and lines
info_mid_spacers = Spacers(info_mid_frame, width=13, height=INFO_MID_HEIGHT, color=INFO_MID_COLOR, amount=6)
INFO_MID_LINE_COLOR = 'white'
INFO_MID_LINE_CUTOFF = 35
info_mid_line_left = Canvas(info_mid_frame, height=INFO_MID_HEIGHT-INFO_MID_LINE_CUTOFF, width=1,
                            borderwidth=0, highlightthickness=0, background=INFO_MID_LINE_COLOR)
info_mid_line_right = Canvas(info_mid_frame, height=INFO_MID_HEIGHT-INFO_MID_LINE_CUTOFF, width=1,
                            borderwidth=0, highlightthickness=0, background=INFO_MID_LINE_COLOR)
#pack things into info mid frame
info_mid_spacers.spacers[0].pack(side=LEFT)
motor_canv.pack(side=LEFT)
info_mid_spacers.spacers[1].pack(side=LEFT)
info_mid_line_left.pack(side=LEFT)
info_mid_spacers.spacers[2].pack(side=LEFT)
speed_canv.pack(side=LEFT)
info_mid_spacers.spacers[3].pack(side=LEFT)
info_mid_line_right.pack(side=LEFT)
info_mid_spacers.spacers[4].pack(side=LEFT)
other_canv.pack(side=LEFT)
info_mid_spacers.spacers[5].pack(side=LEFT)
#--------------------------------------------------
#bottom frame for displaying GPS location and distance
#--------------------------------------------------
INFO_BOT_HEIGHT = 100
info_bot_frame = Frame(display_frames['information'], background=BACKGROUND_COLOR)
info_bot_frame.pack(side=TOP)
#gps location
GPS_WIDTH = 750
GPS_FONT = tkinter.font.Font(family='Helvetica', size=30)
GPS_FONT_2 = tkinter.font.Font(family='Helvetica', size=15)
gps_canv = Canvas(info_bot_frame, width=GPS_WIDTH, height=INFO_BOT_HEIGHT,
                  borderwidth=0, highlightthickness=0, background=BACKGROUND_COLOR)
gps_sts = gps_canv.create_text(GPS_WIDTH/2, INFO_BOT_HEIGHT*0.25,
                               text='GPS', font=GPS_FONT_2, fill='black')
gps_txt = gps_canv.create_text(GPS_WIDTH/2, INFO_BOT_HEIGHT*0.6,
                               text='036.525312, -118.809319', font=GPS_FONT, fill='black')
GPS_BUTTON_WIDTH = 110
GPS_BUTTON_HEIGHT = 80
GPS_BUTTON_PADY = 3
GPS_BUTTON_COLOR = 'light blue'
GPS_BUTTON_FONT = tkinter.font.Font(family='Helvetica', size=15)
gps_left_button_frame = Frame(gps_canv, background=BACKGROUND_COLOR)
gps_canv.create_window(GPS_BUTTON_WIDTH/2, INFO_BOT_HEIGHT*0.55,
                       width=GPS_BUTTON_WIDTH, height=GPS_BUTTON_HEIGHT, window=gps_left_button_frame)
email_gps_button = Button(gps_left_button_frame, command=emailGPS, height=1, width=10,
                          text='Email GPS', font=GPS_BUTTON_FONT, background=GPS_BUTTON_COLOR, foreground='black')
email_gps_button.pack(side=TOP, pady=GPS_BUTTON_PADY)
email_info_button = Button(gps_left_button_frame, command=emailInformation, height=1, width=10,
                           text='Email Info', font=GPS_BUTTON_FONT, background=GPS_BUTTON_COLOR, foreground='black')
email_info_button.pack(side=TOP, pady=GPS_BUTTON_PADY)
gps_right_button_frame = Frame(gps_canv, background=BACKGROUND_COLOR)
gps_canv.create_window(GPS_WIDTH-GPS_BUTTON_WIDTH/2, INFO_BOT_HEIGHT*0.55,
                       width=GPS_BUTTON_WIDTH, height=GPS_BUTTON_HEIGHT, window=gps_right_button_frame)
copy_gps_button = Button(gps_right_button_frame, command=copyGPS, height=1, width=10,
                         text='Copy GPS', font=GPS_BUTTON_FONT, background=GPS_BUTTON_COLOR, foreground='black')
copy_gps_button.pack(side=TOP, pady=GPS_BUTTON_PADY)
copy_info_button = Button(gps_right_button_frame, command=copyInfo, height=1, width=10,
                         text='Copy Info', font=GPS_BUTTON_FONT, background=GPS_BUTTON_COLOR, foreground='black')
copy_info_button.pack(side=TOP, pady=GPS_BUTTON_PADY)
#distances
DIST_WIDTH = 200
DIST_FONT = tkinter.font.Font(family='Helvetica', size=30)
DIST_FONT_2 = tkinter.font.Font(family='Helvetica', size=15)
total_dist_canv = Canvas(info_bot_frame, width=DIST_WIDTH, height=INFO_BOT_HEIGHT,
                         borderwidth=0, highlightthickness=0, background=BACKGROUND_COLOR)
total_dist_unit = total_dist_canv.create_text(DIST_WIDTH/2, INFO_BOT_HEIGHT*0.25,
                                              text='total miles', font=DIST_FONT_2, fill='black')
total_dist_txt = total_dist_canv.create_text(DIST_WIDTH/2, INFO_BOT_HEIGHT*0.6,
                                             text='123456.0', font=DIST_FONT, fill='black')
trip_dist_canv = Canvas(info_bot_frame, width=DIST_WIDTH, height=INFO_BOT_HEIGHT,
                        borderwidth=0, highlightthickness=0, background=BACKGROUND_COLOR)
trip_dist_unit = trip_dist_canv.create_text(DIST_WIDTH/2, INFO_BOT_HEIGHT*0.25,
                                            text='trip miles', font=DIST_FONT_2, fill='black')
trip_dist_txt = trip_dist_canv.create_text(DIST_WIDTH/2, INFO_BOT_HEIGHT*0.6,
                                             text='1234.0', font=DIST_FONT, fill='black')
#spacers
info_bot_spacers = Spacers(info_bot_frame, width=10, height=INFO_BOT_HEIGHT, color=BACKGROUND_COLOR, amount=4)
#pack things into info bottom frame
info_bot_spacers.spacers[0].pack(side=LEFT)
total_dist_canv.pack(side=LEFT)
info_bot_spacers.spacers[1].pack(side=LEFT)
gps_canv.pack(side=LEFT)
info_bot_spacers.spacers[2].pack(side=LEFT)
trip_dist_canv.pack(side=LEFT)
info_bot_spacers.spacers[3].pack(side=LEFT)


#--------------------------------------------------
#settings and controls display
#--------------------------------------------------
display_frames['setting'] = Frame(root_window, background=BACKGROUND_COLOR)
set_frame = Frame(display_frames['setting'], background=BACKGROUND_COLOR)
set_frame.pack(padx=3, pady=3)
SETTING_FONT = tkinter.font.Font(family='Helvetica', size=25)
#controls
light = RadiobottonTab(set_frame, vals=((0,'OFF',io.lightOff),(1,'ON',io.lightOn),(2,'BLINK',io.lightBlink)),
                     update_func=io.lightState, rw=0, cl=0, font=SETTING_FONT, background=BACKGROUND_COLOR, title='Light')
ir_light = RadiobottonTab(set_frame, vals=((0,'OFF',io.irLightOff),(1,'ON',io.irLightOn)),
                     update_func=io.irLightState, rw=1, cl=0, font=SETTING_FONT, background=BACKGROUND_COLOR, title='IR Lights')
taillight = RadiobottonTab(set_frame, vals=((0,'OFF',io.taillightOff),(1,'ON',io.taillightOn)),
                  update_func=io.taillightState, rw=2, cl=0, font=SETTING_FONT, background=BACKGROUND_COLOR, title='Taillights')
power_12v = RadiobottonTab(set_frame, vals=((0,'OFF',io.power12vOff),(1,'ON',io.power12vOn)),
                  update_func=io.power12vState, rw=3, cl=0, font=SETTING_FONT, background=BACKGROUND_COLOR, title='12V Power')
motor = RadiobottonTab(set_frame, vals=((0,'OFF',io.motorOff),(1,'ON',io.motorOn),(2,'TOG',io.motorToggle)),
                  update_func=io.motorState, rw=4, cl=0, font=SETTING_FONT, background=BACKGROUND_COLOR, title='Motor')
screen_ctrl = RadiobottonTab(set_frame, vals=((0,'OFF',io.screenOff),(1,'ON',io.screenOn),(2,'TOG',io.screenToggle)),
                          update_func=io.screenState, rw=5, cl=0, font=SETTING_FONT, background=BACKGROUND_COLOR, title='Screen')
touch_ctrl = RadiobottonTab(set_frame, vals=((0,'OFF',io.touchOff),(1,'ON',io.touchOn)),
                          update_func=io.touchState, rw=6, cl=0, font=SETTING_FONT, background=BACKGROUND_COLOR, title='Touch')
#settings
unit = RadiobottonTab(set_frame, vals=((0,'Metric',prog.metricUnit),(1,'Imperial',prog.imperialUnit)),
                      update_func=prog.getUnit, rw=0, cl=3, font=SETTING_FONT, background=BACKGROUND_COLOR, title='Unit',
                      color_sequence=('light blue', 'light blue'))
buzzer = RadiobottonTab(set_frame, vals=((0,'Disable',prog.buzzerDisable),(1,'Enable',prog.buzzerEnable)),
                        update_func=prog.buzzer, rw=1, cl=3, font=SETTING_FONT, background=BACKGROUND_COLOR, title='Buzzer')
virtual_fence = RadiobottonTab(set_frame, vals=((0,'Disable',prog.virFenDisable),(1,'Enable',prog.virFenEnable)),
                               update_func=prog.virtualFence, rw=2, cl=3, font=SETTING_FONT, background=BACKGROUND_COLOR, title='Virtual Fence')
vibration_detection = RadiobottonTab(set_frame, vals=((0,'Disable',prog.vibDetDisable),(1,'Enable',prog.vibDetEnable)),
                                     update_func=prog.vibrationDetection, rw=3, cl=3, font=SETTING_FONT, background=BACKGROUND_COLOR,
                                     title='Vibrate Detect')
#spinbox for vibration sensitivity
VIB_SEN_COLOR = 'light blue'
vib_sensitivity = IntVar()
vib_sen_label = Label(set_frame, text='Vib Sensitivity', font=SETTING_FONT, width=12, background=VIB_SEN_COLOR)
vib_sen_mark = Label(set_frame, text='---', font=SETTING_FONT, background=BACKGROUND_COLOR)
vib_sen_box = Spinbox(set_frame, font=SETTING_FONT, textvariable=vib_sensitivity,
                      from_=0, to=1000, increment=10, background=VIB_SEN_COLOR, width=13,
                      command=vibSenSetting, highlightthickness=0)
vib_sen_label.grid(row=4, column=3)
vib_sen_mark.grid(row=4, column=4)
vib_sen_box.grid(row=4, column=5)


#--------------------------------------------------
#messages display
#--------------------------------------------------
display_frames['message'] = Frame(root_window, background=BACKGROUND_COLOR)
MESSAGE_FONT = tkinter.font.Font(family='Helvetica', size=100)
message_txt = Label(display_frames['message'], width=16, height=4,
                    text="Message", font=MESSAGE_FONT, background=BACKGROUND_COLOR)
message_txt.pack()
message_handle = MessageHandle()

#--------------------------------------------------
#lock camera display
#--------------------------------------------------
display_frames['lock_cam'] = Frame(root_window, background=BACKGROUND_COLOR)
#image
IMAGE_COLOR = 'black'
IMAGE_WIDTH = 1266
IMAGE_HEIGHT = 600
lock_cam_canv = Canvas(display_frames['lock_cam'], width=IMAGE_WIDTH, height=IMAGE_HEIGHT,
                       background=IMAGE_COLOR, highlightthickness=0)
lock_cam_canv.pack(side=LEFT, padx=6, pady=6)
img = camera.getImage0()
imgTk = ImageTk.PhotoImage(img)
lock_cam_img = lock_cam_canv.create_image(400, IMAGE_HEIGHT/2, image=imgTk)
lock_cam_canv.create_line(803, 0, 803, IMAGE_HEIGHT, width=6, fill=BACKGROUND_COLOR)
#display useful info
lock_cam_info_frame = Frame(lock_cam_canv, background=IMAGE_COLOR)
lock_cam_canv.create_window(1036, IMAGE_HEIGHT/2, width=460, height=IMAGE_HEIGHT, win=lock_cam_info_frame)
lock_cam_info = CameraInfoDisplay(lock_cam_info_frame, IMAGE_COLOR)

#display information at startup
display_frames['information'].pack(side=TOP)
#--------------------------------------------------
#loop to run gui display
#--------------------------------------------------
prog.start()
while prog.isRunning():
    #run the window
    root_window.update_idletasks()
    root_window.update()

    #update the frame
    if display_frames['information'].winfo_ismapped():
        updateInformation()
    elif display_frames['setting'].winfo_ismapped():
        updateSetting()
    elif display_frames['message'].winfo_ismapped():
        pass
    elif display_frames['lock_cam'].winfo_ismapped():
        try:
            img = camera.getImage0()
            imgTk = ImageTk.PhotoImage(img)
            lock_cam_canv.itemconfigure(lock_cam_img, image=imgTk)
        except Exception as e:
            print(__file__ + ": Error updating lock camera image: " + str(repr(e)))
        lock_cam_info.update()
    
    updateMessage() #this one has to be constantly updated
    time.sleep(0.01)


#--------------------------------------------------
#end of gui display programs
#--------------------------------------------------
root_window.destroy()
prog.end()
