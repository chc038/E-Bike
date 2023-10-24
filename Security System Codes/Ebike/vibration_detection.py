from pygame import mixer
import time
import prog
import math
import security_functions as security
import email_functions as email
import gps_functions as gps
import io_functions as io



def accMagnitude(accx, accy, accz):
    return abs(math.sqrt(accx**2 + accy**2 + accz**2) - 9.81)
            

mixer.init()
sound = mixer.Sound('Security_Files/Aleart_Sound.wav')


prog.start()
while prog.isRunning():    
    #check for vibration
    if security.lockState() == '1' and prog.vibrationDetection() == 1:
        vib_sen = prog.vibrationSensitivity()
        #get acceleration data
        imu_data = io.getIMUData()
        if vib_sen != None and imu_data != None:
            acc_mag = accMagnitude(imu_data['accel_x'], imu_data['accel_y'], imu_data['accel_z']) * 1000 #mm/s/s
            if acc_mag > vib_sen:
                #make vibration aleart
                prog.namePrint("Vibration Detected!")
                security.addDisplayMessage("Vibration Aleart", 10)
                email.sendPhotoEmail(subject='Vibration Alearts',
                                     message="Ebike Vibration Detected!", info=True)
                if prog.buzzer() == 1:
                    #make aleart sound
                    for _ in range(5):
                        sound.play(maxtime=500)
                        time.sleep(1)
                
    time.sleep(1)


prog.end()
