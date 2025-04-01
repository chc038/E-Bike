import time
import prog
import security_functions as security
import gps_functions as gps
import email_functions as email


time.sleep(0.01) #wait a bit
ena = False
lock_sts = False

prog.start()
while prog.isRunning():
    ena = prog.virtualFence()
    lock_sts = security.lockState()
    
    if ena == 1 and lock_sts == '1': #if enabled and locked, get location
        park_loc = gps.getParkLocation() #get park location
        loc = gps.getGPS() #get current location
        if park_loc != None and loc != None: #if successfullt gathered info
            park_lat = park_loc['latitude'] #get park latitude
            park_log = park_loc['longitude'] #get park longitude
            lat = loc['latitude'] #get current latitude
            log = loc['longitude'] #get current longitude

            #check for location differences
            if gps.findDistance(park_lat, park_log, lat, log) > 300: #if difference too big
                prog.namePrint('Virtual Fence Aleart')
                security.virtualFenceSet(1)
                email.sendPhotoEmail(subject='Virtual Fence Aleart',
                                     message="Ebike Location Changed!", info=True)
                prog.sleep(59) #wait 1 minuet before checking again
            else:
                security.virtualFenceSet(0)
    else:
        security.virtualFenceSet(0)
    
    time.sleep(1) #wait 0.1 s


prog.end()

