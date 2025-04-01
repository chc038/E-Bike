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


last_data_time = 0
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
        with serial.Serial(SERIAL_PORT, baudrate=115200, timeout=0.05) as ser:
            prog.timePrint("VESC Connected!")
            while prog.isRunning():
                #get values from vesc 1 (can_id = 1)
                GetValues.can_id = 31
                ser.write(pyvesc.encode_request(GetValues))
                time.sleep(0.2)
                if ser.in_waiting > 0:
                    try:
                        msg, consumed = pyvesc.decode(ser.read(ser.in_waiting))
                        if msg:
                            #reecord time
                            last_data_time = time.time()
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
                                prog.timePrint("VESC1 Fault: " + str(msg.mc_fault_code))
                    except Exception as e:
                        prog.timePrint("VESC1 Error! " + repr(e))
                
                #get values from other vesc 2 (the one with usb cord plugged in)
                time.sleep(0.2)
                GetValues.can_id = None
                ser.write(pyvesc.encode_request(GetValues))
                time.sleep(0.2)
                if ser.in_waiting > 0:
                    try:
                        msg2, consumed = pyvesc.decode(ser.read(ser.in_waiting))
                        if msg2:
                            #reecord time
                            last_data_time = time.time()
                            #write values to file
                            infos_vesc = io.getInfosVESC()
                            infos_vesc["isOn2"] = 1
                            infos_vesc["inpVoltage2"] = msg2.v_in
                            infos_vesc["avgInputCurrent2"] = msg2.avg_input_current
                            infos_vesc["avgMotorCurrent2"] = msg2.avg_motor_current
                            #infos_vesc["dutyCycleNow2"] = msg2.duty_cycle_now
                            infos_vesc["rpm2"] = msg2.rpm
                            #infos_vesc["ampHours2"] = msg2.amp_hours
                            #infos_vesc["wattHours2"] = msg2.watt_hours
                            #infos_vesc["tachometer2"] = msg2.tachometer
                            infos_vesc["tempMosfet2"] = msg2.temp_fet
                            infos_vesc["tempMotor2"] = msg2.temp_motor
                            #infos_vesc["timems2"] = msg2.time_ms
                            io.writeInfosVESC(infos_vesc)
                            #print fault code
                            if msg2.mc_fault_code != b'\x00':
                                prog.timePrint("VESC2 Fault: " + str(msg2.mc_fault_code))
                    except Exception as e:
                        prog.timePrint("VESC2 Error! " + repr(e))
                time.sleep(0.2)
                #record off if no data for a long time
                if time.time() - last_data_time > 5:
                    infos_vesc = io.getInfosVESC()
                    infos_vesc["isOn"] = 0
                    infos_vesc["isOn2"] = 0
                    io.writeInfosVESC(infos_vesc)
    except (serial.serialutil.SerialException, OSError) as e:
        prog.timePrint("VESC Disconnected! " + repr(e))
        infos_vesc = io.getInfosVESC()
        infos_vesc["isOn"] = 0
        infos_vesc["isOn2"] = 0
        io.writeInfosVESC(infos_vesc)
        time.sleep(10)
    time.sleep(5)    

