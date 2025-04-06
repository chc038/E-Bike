import json
import io_functions as io
import email_functions as email
import gps_functions as gps
import time


def lockState():
    file = open("Security_Files/lock.txt", 'r')
    content = file.read().strip()
    file.close()
    return content
def lockSet(state):
    state = str(state)
    if state in ['0', '1', '2']: 
        file = open("Security_Files/lock.txt", 'w')
        file.write(state)
        file.close()
    else:
        raise Exception("Invalid lock state!")
def lockStateToStr(state):
    if state == '0':
        return "Unlocked"
    elif state == '1':
        return "Locked"
    elif state == '2':
        return "Home"
    else:
        return None

def unlockSequence():
    io.turnSigBlink()
    lockSet(0)
    io.power12vOn()
    io.taillightOn()
    io.irLightOn()
    io.motorOn()
    io.screenOn()
    io.touchOff()
    io.clearTripDistance()
    email.sendPhotoEmail(subject='Ebike Operations', message='Ebike is Unlocked!\n' +
                         gps.getGPSLocation() + '\n' + time.strftime('%c'))
    print("Ebike is Unlocked!")
    #time.sleep(0.1)
    #io.turnSigBlink()
    
def lockSequence():
    io.turnSigBlink()
    gps.setParkLocation()
    lockSet(1)
    io.power12vOff()
    io.lightOff()
    io.taillightOff()
    io.irLightOn()
    io.motorOff()
    io.screenOff()
    io.touchOff()
    email.sendPhotoEmail(subject='Ebike Operations', message='Ebike is Locked!\n' +
                         gps.getGPSLocation() + '\n' + time.strftime('%c'))
    print("Ebike is Locked!")
    #time.sleep(0.1)
    #io.turnSigBlink()
def homeSequence():
    lockSet(2)
    io.power12vOff()
    io.lightOff()
    io.taillightOff()
    io.irLightOff()
    io.motorOff()
    io.screenOff()
    io.touchOn()
    email.sendPhotoEmail(subject='Ebike Operations', message='Ebike is Home!\n' +
                         gps.getGPSLocation() + '\n' + time.strftime('%c'))
    print("Ebike is Home!")


def virtualFenceState():
    file = open("Security_Files/virtual_fence.txt", 'r')
    content = file.read().strip()
    file.close()
    return content
def virtualFenceSet(state):
    state = str(state)
    if state in ['0', '1']:
        file = open("Security_Files/virtual_fence.txt", 'w')
        file.write(state)
        file.close()
    else:
        raise Exception("Invalid vf state!")


def getDisplayMessages():
    file = open("Security_Files/display_messages.json", 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return None
def writeDisplayMessages(messages):
    file = open("Security_Files/display_messages.json", 'w')
    file.write(json.dumps(messages, indent=2))
    file.close()
def addDisplayMessage(message, elapse):
    messages = getDisplayMessages()
    if messages != None:
        message_dict = {'message': message, 'elapse': time.time() + elapse}
        messages.append(message_dict)
        writeDisplayMessages(messages)
        return True
    else:
        return False
def displayMessages():
    messages = getDisplayMessages()
    if messages != None and len(messages) > 0:
        writeDisplayMessages([])
    return messages


def securityInfo():
    return "\nLock State: " + str(lockStateToStr(lockState())) + "\n"
    
