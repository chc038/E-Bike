import prog
import io_functions as io
import time
import serial
#download from: https://github.com/LiamBindle/PyVESC
#dependency: pip install crccheck --break-system-packages
#may need to change "_comm_forward_can = 34" in pyvesc/protocol/base.py for can bus forwarding to work
import pyvesc
from pyvesc.VESC.messages import GetValues


PRINT_THINGS = False
#SERIAL_PORT = "/dev/ttyACM0"
SERIAL_PORT = "/dev/ttyUSB0"


last_data_0 = 0
last_data_1 = 0
last_data_2 = 0
prog.start()
while prog.isRunning():
    #open serial port and comm with vesc if main battery is connected
    #main_vol = io.mainBatteryVoltage()
    #time.sleep(1)
    #if main_vol != None:
    #    if main_vol >= 12.5:
    #try serial communication with vesc until serial fault occurs (due to vesc off)
    try:
        #open serial port connected to vesc and continuously get values
        with serial.Serial(SERIAL_PORT, baudrate=115200, timeout=0.1) as ser:
            prog.timePrint("VESC Connected!")
            while prog.isRunning():
                #print(time.time())
                #get values from vesc 20 (can id 20, the one with usb cord plugged in)
                GetValues.can_id = None
                ser.write(pyvesc.encode_request(GetValues))
                # try to read response
                time.sleep(0.08)
                if ser.in_waiting > 0:
                    try:
                        msg, consumed = pyvesc.decode(ser.read(ser.in_waiting))
                        if msg:
                            #print("OK 0")
                            #record time
                            last_data_0 = time.time()
                            #write values to file
                            infos_vesc = io.getInfosVESC()
                            infos_vesc["isOn"] = 1
                            infos_vesc["inpVoltage"] = msg.v_in
                            infos_vesc["avgInputCurrent"] = msg.avg_input_current
                            infos_vesc["avgMotorCurrent"] = msg.avg_motor_current
                            #infos_vesc["dutyCycleNow"] = msg.duty_cycle_now
                            infos_vesc["rpm"] = msg.rpm
                            #infos_vesc["ampHours"] = msg.amp_hours
                            #infos_vesc["wattHours"] = msg.watt_hours
                            #infos_vesc["tachometer"] = msg.tachometer
                            infos_vesc["tempMosfet"] = msg.temp_fet
                            infos_vesc["tempMotor"] = msg.temp_motor
                            #infos_vesc["timems"] = msg.time_ms
                            io.writeInfosVESC(infos_vesc)
                            #print fault code
                            if msg.mc_fault_code != b'\x00':
                                prog.timePrint("VESC20 Fault: " + str(msg.mc_fault_code))
                    except Exception as e:
                        prog.timePrint("VESC20 Error! " + repr(e))
                
                #get values from vesc 1 (can_id = 31)
                GetValues.can_id = 31
                ser.write(pyvesc.encode_request(GetValues))
                # try to read response
                time.sleep(0.08)
                if ser.in_waiting > 0:
                    try:
                        msg, consumed = pyvesc.decode(ser.read(ser.in_waiting))
                        if msg:
                            #print("OK 1")
                            #record time
                            last_data_1 = time.time()
                            #write values to file
                            infos_vesc = io.getInfosVESC()
                            infos_vesc["isOn1"] = 1
                            infos_vesc["inpVoltage1"] = msg.v_in
                            infos_vesc["avgInputCurrent1"] = msg.avg_input_current
                            infos_vesc["avgMotorCurrent1"] = msg.avg_motor_current
                            infos_vesc["rpm1"] = msg.rpm
                            infos_vesc["tempMosfet1"] = msg.temp_fet
                            infos_vesc["tempMotor1"] = msg.temp_motor
                            io.writeInfosVESC(infos_vesc)
                            #print fault code
                            if msg.mc_fault_code != b'\x00':
                                prog.timePrint("VESC1 Fault: " + str(msg.mc_fault_code))
                    except Exception as e:
                        prog.timePrint("VESC1 Error! " + repr(e))
                
                #get values from other vesc 2 (can_id = 32) 
                GetValues.can_id = 32
                ser.write(pyvesc.encode_request(GetValues))
                # try to read response
                time.sleep(0.08)
                if ser.in_waiting > 0:
                    try:
                        msg, consumed = pyvesc.decode(ser.read(ser.in_waiting))
                        if msg:
                            #print("OK 2")
                            #record time
                            last_data_2 = time.time()
                            #write values to file
                            infos_vesc = io.getInfosVESC()
                            infos_vesc["isOn2"] = 1
                            infos_vesc["inpVoltage2"] = msg.v_in
                            infos_vesc["avgInputCurrent2"] = msg.avg_input_current
                            infos_vesc["avgMotorCurrent2"] = msg.avg_motor_current
                            infos_vesc["rpm2"] = msg.rpm
                            infos_vesc["tempMosfet2"] = msg.temp_fet
                            infos_vesc["tempMotor2"] = msg.temp_motor
                            io.writeInfosVESC(infos_vesc)
                            #print fault code
                            if msg.mc_fault_code != b'\x00':
                                prog.timePrint("VESC2 Fault: " + str(msg.mc_fault_code))
                    except Exception as e:
                        prog.timePrint("VESC2 Error! " + repr(e))
                
                #record off if no data for a long time
                if time.time() - last_data_0 > 3:
                    infos_vesc = io.getInfosVESC()
                    infos_vesc["isOn"] = 0
                    io.writeInfosVESC(infos_vesc)
                if time.time() - last_data_1 > 3:
                    infos_vesc = io.getInfosVESC()
                    infos_vesc["isOn1"] = 0
                    io.writeInfosVESC(infos_vesc)
                if time.time() - last_data_2 > 3:
                    infos_vesc = io.getInfosVESC()
                    infos_vesc["isOn2"] = 0
                    io.writeInfosVESC(infos_vesc)
    except (serial.serialutil.SerialException, OSError) as e:
        prog.timePrint("VESC Disconnected! " + repr(e))
        infos_vesc = io.getInfosVESC()
        infos_vesc["isOn"] = 0
        infos_vesc["isOn1"] = 0
        infos_vesc["isOn2"] = 0
        io.writeInfosVESC(infos_vesc)
        time.sleep(10)
    time.sleep(5)    

