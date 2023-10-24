import json
import os
import __main__
import time


def start():
    with open("Program_Files/run_prog.txt", 'w') as file:
        file.write('1')
    print(__main__.__file__ + " started")
def stop():
    with open("Program_Files/run_prog.txt", 'w') as file:
        file.write('0')
def end():
    print(__main__.__file__ + " ended")
def isRunning():
    run = True
    with open("Program_Files/run_prog.txt", 'r') as file:
        if file.read().strip() == '0':
            run = False
    return run
def sleep(seconds):
    end_time = time.time() + seconds
    while time.time() < end_time:
        if not isRunning():
            break
        else:
            time.sleep(0.1)


def namePrint(content):
    content = str(content)
    print(__main__.__file__ + " --> " + str(content))
def timePrint(content):
    content = str(content)
    print(time.strftime("%m/%d_%H:%M ") + __main__.__file__ + " --> " + str(content))


def getSettings():
    file = open("Program_Files/settings.json", 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return None
def getSetting(setting):
    settings = getSettings()
    if settings != None:
        return settings[setting]
    else:
        return None
def writeSettings(settings):
    file = open("Program_Files/settings.json", 'w')
    file.write(json.dumps(settings, indent=2))
    file.close()
def writeSetting(setting, value):
    settings = getSettings()
    if settings != None:
        if settings[setting] != value:
            settings[setting] = value
            writeSettings(settings)
        return True
    else:
        return False

def getUnit():
    return getSetting('unit')
def metricUnit():
    writeSetting('unit', 0)
def imperialUnit():
    writeSetting('unit', 1)

def buzzer():
    return getSetting('buzzer')
def buzzerDisable():
    writeSetting('buzzer', 0)
def buzzerEnable():
    writeSetting('buzzer', 1)

def virtualFence():
    return getSetting('virtual_fence')
def virFenDisable():
    writeSetting('virtual_fence', 0)
def virFenEnable():
    writeSetting('virtual_fence', 1)

def vibrationDetection():
    return getSetting('vibration_detection')
def vibDetDisable():
    writeSetting('vibration_detection', 0)
def vibDetEnable():
    writeSetting('vibration_detection', 1)
    
def vibrationSensitivity():
    return getSetting('vibration_sensitivity')
def vibSenSet(value):
    writeSetting('vibration_sensitivity', value)


# def get_folder_filename(full_name):
#     """get folder name and filename from a string of path to a file"""
#     cnt = full_name.count('/')
#     ind = -1
#     for _ in range(cnt):
#         ind = full_name.index('/', ind+1)
#     folder = full_name[:ind]
#     filename = full_name[ind+1:]
#     return (folder, filename)

def make_folder(foldername):
    """make a the specified folder if it does not already exist"""
    if not os.path.exists(foldername):
        os.makedirs(foldername)


