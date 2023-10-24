import json

OUTPUTS_FILE = "IO_Files/outputs.json"
INFO_FILE = "IO_Files/info.json"
INFO_ADC_FILE = "IO_Files/info_adc.json"
INFO_VESC_FILE = "IO_Files/info_vesc.json"

def getOutputs():
    file = open(OUTPUTS_FILE, 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return None
def getOutput(key):
    outputs = getOutputs()
    if outputs != None:
        try:
            return outputs[key]
        except KeyError:
            print("Key Error: " + key)
            return None
    else:
        return None
def strfOutputs():
    outputs = getOutputs()
    if outputs != None:
        output_str =  "\nOUTPUTS\n"
        for key in outputs.keys():
            output_str += key + ": " + str(outputs[key]) + "\n"
        return output_str
    else:
        return None
def setOutputs(outputs):
    file = open(OUTPUTS_FILE, 'w')
    file.write(json.dumps(outputs, indent=2))
    file.close()
def setOutput(key, value):
    outputs = getOutputs()
    if outputs != None:
        if outputs[key] != value:
            outputs[key] = value
            setOutputs(outputs)
        return True
    else:
        return False

def getInfos():
    file = open(INFO_FILE, 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return {}
def getInfo(key):
    infos = getInfos()
    if len(infos) > 0:
        try:
            return infos[key]
        except KeyError:
            print("Key Error: " + key)
            return None
    else:
        return None
def strfInfos():
    infos = getInfos()
    if infos != None:
        info_str = "\nINFORMATION\n"
        for key in infos.keys():
            info_str += key + ": " + str(infos[key]) + "\n"
        return info_str
    else:
        return None
def writeInfos(infos):
    file = open(INFO_FILE, 'w')
    file.write(json.dumps(infos, indent=2))
    file.close()

def getInfosADC():
    file = open(INFO_ADC_FILE, 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return {}
def getInfoADC(key):
    infos = getInfosADC()
    if len(infos) > 0:
        try:
            return infos[key]
        except KeyError:
            print("Key Error: " + key)
            return None
    else:
        return None
def strfInfosADC():
    infos = getInfosADC()
    if infos != None:
        info_str = "\nINFORMATION_ADC\n"
        for key in infos.keys():
            info_str += key + ": " + str(infos[key]) + "\n"
        return info_str
    else:
        return None
def writeInfosADC(infos):
    file = open(INFO_ADC_FILE, 'w')
    file.write(json.dumps(infos, indent=2))
    file.close()

def getInfosVESC():
    file = open(INFO_VESC_FILE, 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return {}
def getInfoVESC(key):
    infos = getInfosVESC()
    if len(infos) > 0:
        try:
            return infos[key]
        except KeyError:
            print("Key Error: " + key)
            return None
    else:
        return None
def strfInfosVESC():
    infos = getInfosVESC()
    if infos != None:
        info_str = "\nINFORMATION_VESC\n"
        for key in infos.keys():
            info_str += key + ": " + str(infos[key]) + "\n"
        return info_str
    else:
        return None
def writeInfosVESC(infos):
    file = open(INFO_VESC_FILE, 'w')
    file.write(json.dumps(infos, indent=2))
    file.close()

#light
def lightState():
    return getOutput("light")
def lightOff():
    setOutput("light", 0)
def lightOn():
    setOutput("light", 1)
def lightBlink():
    setOutput("light", 2)
def toggleLight():
    light_state = lightState()
    if light_state == 0:
        lightOn()
    else:
        lightOff()

#taillight
def taillightState():
    return getOutput("taillight")
def taillightOn():
    setOutput("taillight", 1)
def taillightOff():
    setOutput("taillight", 0)

#ir light
def irLightState():
    return getOutput("ir_light")
def irLightOn():
    setOutput("ir_light", 1)
def irLightOff():
    setOutput("ir_light", 0)

#12v output
def power12vState():
    return getOutput("power_12v")
def power12vOn():
    setOutput("power_12v", 1)
def power12vOff():
    setOutput("power_12v", 0)

#regen braking
def motorState():
    return getOutput("motor")
def motorOn():
    setOutput("motor", 1)
def motorOff():
    setOutput("motor", 0)
def motorToggle():
    setOutput("motor", 2)


#screen
def screenState():
    return getOutput("screen")
def screenOn():
    setOutput("screen", 1)
def screenOff():
    setOutput("screen", 0)
def screenToggle():
    setOutput("screen", 2)
def toggleScreen():
    screen_state = screenState()
    if screen_state == 0:
        screenOn()
    elif screen_state == 1:
        screenOff()

def touchState():
    return getOutput("touch")
def touchOn():
    setOutput("touch", 1)
def touchOff():
    setOutput("touch", 0)


#buttons
def button1State():
    return getInfo("button_1")
def button2State():
    return getInfo("button_2")

#brake
def brakeState():
    return getInfo("brake")

#turn signal
def turnSignalState():
    return getOutput("turn_signal")

#key switch
def keySwitchState():
    return getInfoADC("key_switch")

#main battery voltage
def mainBatteryVoltage():
    return getInfoADC("battery_48v")

#12v bus voltage
def bus12Voltage():
    return getInfoADC("bus_12v")

#main battery current
def mainBatteryCurrent():
    return getInfoADC("main_current")

#cpu
def cpuTemperature():
    return getInfoADC('cpu_temperature')
def memory():
    return getInfoADC('memory')

#vesc
def vescState():
    return getInfoVESC("isOn")
def motorInputVoltage():
    return getInfoVESC("inpVoltage")
def motorInputCurrent():
    return getInfoVESC("avgInputCurrent")
def motorRPM():
    return getInfoVESC("rpm")
def motorWattHours():
    return getInfoVESC("wattHours")
def motorDistance():
    return getInfoVESC("tachometer")
def motorTemperature():
    return getInfoVESC("tempMotor")
def mosfetTemperature():
    return getInfoVESC("tempMosfet")

def vesc2State():
    return getInfoVESC("isOn2")
def motor2InputVoltage():
    return getInfoVESC("inpVoltage2")
def motor2InputCurrent():
    return getInfoVESC("avgInputCurrent2")
def motor2RPM():
    return getInfoVESC("rpm2")
def motor2WattHours():
    return getInfoVESC("wattHours2")
def motor2Distance():
    return getInfoVESC("tachometer2")
def motor2Temperature():
    return getInfoVESC("tempMotor2")
def mosfet2Temperature():
    return getInfoVESC("tempMosfet2")

#chain tension sensor
def chainSensorState():
    return getInfoVESC("chainSensor")

#distance record
def getDistances(): #distance is in meters
    file = open("IO_Files/distance.json", 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return None
def totalDistance():
    distances = getDistances()
    if distances != None:
        return distances['total']
    else:
        return None
def tripDistance():
    distances = getDistances()
    if distances != None:
        return distances['trip']
    else:
        return None
def strfDistance():
    distances = getDistances()
    if distances != None:
        distance_str = "\nDISTANCE\n"
        for key in distances.keys():
            distance_str += key + ": " + str(distances[key]) + "\n"
        return distance_str
    else:
        return None
def writeDistances(distances):
    file = open("IO_Files/distance.json", 'w')
    file.write(json.dumps(distances, indent=2))
    file.close()
def addDistance(distance):
    distances = getDistances()
    if distances != None:
        distances['total'] += distance
        distances['trip'] += distance
        writeDistances(distances)
        return True
    else:
        return False
def clearTripDistance():
    distances = getDistances()
    if distances != None:
        distances['trip'] = 0
        writeDistances(distances)
        return True
    else:
        return False
    

def getIMUData():
    file = open("IO_Files/imu.json", 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return None
def writeIMUData(data):
    file = open("IO_Files/imu.json", 'w')
    file.write(json.dumps(data, indent=2))
    file.close()

