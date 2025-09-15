import requests
import time
import json
import prog
import email_functions as email
import io_functions as io

def readSchedule(filename='Program_Files/charge_schedule.json'):
    file = open(filename)
    content = file.read()
    file.close()
    return json.loads(content)


PLUG_IP = "192.168.50.136"
BASE_CMD = "http://" + PLUG_IP + "/cm?user=admin&password=Ulw9f4&"
ON_CMD = BASE_CMD + "cmnd=Power%20ON"
OFF_CMD = BASE_CMD + "cmnd=Power%20OFF"

W_DAY = {'Mon':0, 'Tue':1, 'Wed':2, 'Thu':3, 'Fri':4, 'Sat':5, 'Sun':6}


last_cmd_time = 0.0

prog.start()
while prog.isRunning():
    try:
#         #filter out commands today
#         commands = readSchedule()
#         commands_today = [command for command in commands
#                           if W_DAY[command['day']]==time.localtime().tm_wday]
# 
#         #change time to epoch seconds for comparison
#         str_today = time.strftime("%B %d %Y ")
#         start_time_today = time.mktime(time.strptime(str_today+'00:00', "%B %d %Y %H:%M"))
#         commands_today = [{'time': time.mktime(time.strptime(str_today+command['time'], "%B %d %Y %H:%M"))
#                            , 'cmd': command['cmd']}
#                           for command in commands_today]
# 
#         #filter out commands between last check and now
#         commands_today = [command for command in commands_today
#                           if last_cmd_time <= command['time'] and command['time'] <= time.time()]
# 
#         #sort out the latest command
#         if len(commands_today) > 0:
#             commands_today.sort(key=lambda command: command['time'], reverse=True)
#             last_cmd_time = time.time()
# 
#             #execute command
#             cmd = commands_today[0]['cmd']
#             if cmd == 'ON':
#                 result = requests.get(ON_CMD)
#                 prog.timePrint(repr(result.json()))
#             elif cmd == 'OFF':
#                 result = requests.get(OFF_CMD)
#                 prog.timePrint(repr(result.json()))
#             else:
#                 prog.timePrint("Invalid Command: " + str(cmd))
        
        #check main battery voltage
        vesc_on = io.vescState()
        b48 = io.motorInputVoltage()
        #activate charger if low voltage
        if vesc_on == 1 and b48 != None and b48 < 43.0:
            time.sleep(60)
            #check again after 1 min
            b48 = io.motorInputVoltage()
            if b48 != None and b48 < 43.0:
                prog.timePrint("Activating Charger due to Low Voltage")
                result = requests.get(ON_CMD)
                prog.timePrint(repr(result.json()))
            

    except Exception as e:
        #error activating charger
        prog.timePrint(repr(e))
        email.sendPhotoEmail(subject="Battery Alearts",
                             message=time.strftime("Error Activating Charger!\n%c"))

    time.sleep(2)
