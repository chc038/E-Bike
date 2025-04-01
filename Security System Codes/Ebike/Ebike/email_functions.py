import camera_functions as camera
import gps_functions as gps
import json 
import os
import time


def getEmails():
    file = open("Program_Files/email_messages.json", 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return None
def writeEmails(emails):
    file = open("Program_Files/email_messages.json", 'w')
    file.write(json.dumps(emails, indent=2))
    file.close()
def addEmail(email):
    emails = getEmails()
    if emails != None:
        emails.append(email)
        writeEmails(emails)
        return True
    else:
        return False
def clearEmails():
    writeEmails([])

def sendEmail(subject=None, message="", attatchments=None, info=False):
    if info:
        message += "\n" + gps.getGPSLocation() +time.strftime("\n%c")
    email = {'subject': subject, 'message': message, 'attatchments': attatchments}
    suc, count = (False, 0)
    while not suc:
        if count > 10:
            print(__file__ + ": Error adding Email to list")
            break
        suc = addEmail(email)
        count += 1

def sendPhotoEmail(subject=None, message="", info=False):
    attatchments = []
    filename0 = camera.getFilename0() #camera 0
    if os.path.exists(filename0):
        attatchments.append(filename0)
    else:
        print(__file__ + ": Unable to find image from camera 0!")
    sendEmail(subject=subject, message=message, attatchments=attatchments, info=info)


