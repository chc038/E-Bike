import time
import serial
import adafruit_gps #sudo pip3 install adafruit-circuitpython-gps
import gps_functions
import io_functions as io
import security_functions as security
import prog
import os


PRINT_THINGS = False
DATA_FOLDER = "/home/pi/Documents/GPS_Data"
DATA_HEADER = "tm(s),latitude(deg),logitude(deg),speed(m/s)"


class DataFile():
    def __init__(self, folder, header):
        self.folder = folder
        self.header = header
        self.tm = time.time()

    def add_data_to_file(self, content):
        """add content to file in predetermined location"""
        #make folder and generate file name
        foldername = self.folder + time.strftime('/%m-%d-%Y')
        prog.make_folder(foldername)
        filename = foldername + time.strftime('/%H-%M.csv')
        #header on first line
        to_write = ""
        if not os.path.exists(filename):
            self.tm = time.time()
            to_write += self.header + '\n'
        #write content to file
        to_write +=  content + '\n'
        with open(filename, 'a') as file:
            file.write(to_write)


last_latitude = 0.0
last_longitude = 0.0

#for gps module
gps_serial = serial.Serial("/dev/ttyS0", 9600, timeout = 0.001) # /dev/ttyS0 or /dev/ttyACM0
gps = adafruit_gps.GPS(gps_serial, debug=False)
gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') #Turn on minimum info (RMC only, location)
time.sleep(1)
gps.send_command(b"PMTK220,100") # Set update rate to 10hz (100ms update period)
time.sleep(1)

#for data logging
data_file = DataFile(DATA_FOLDER, DATA_HEADER)

prog.start()
while prog.isRunning():
    #update gps, proceed if new things are parsed
    if gps.update():
        update_time = round(time.time(), 2)
        if PRINT_THINGS:
            print("GPS Updated")
        #check to fee oif there is a GPS fix
        if gps.has_fix:
            #get location
            latitude = gps.latitude
            longitude = gps.longitude
            #get speed in m/s
            speed = 0.0
            if gps.speed_knots is not None:
               speed = gps.speed_knots / 1.94384
            #write to file
            gps_functions.writeGPSInfo(latitude=latitude, longitude=longitude,
                                       speed=speed, tme=update_time)
            
            #log gps data to another file
            data_str = str(update_time)+','+str(latitude)+','+str(longitude)+','+str(speed)
            data_file.add_data_to_file(data_str)
            if PRINT_THINGS:
                print(data_str)
            
            #add distance when unlocked        
            if security.lockState() == '0':
                if (last_latitude, last_longitude) != (0.0, 0.0):
                    #get distance
                    distance = gps_functions.findDistance(last_latitude, last_longitude,
                                                          latitude, longitude)
                    if distance > 15: #update old location when moved sufficiently far
                        last_latitude = latitude
                        last_longitude = longitude
                        if distance > 1000: #remove erratic/unreasonable distances
                            distance = 0
                        if distance != 0 and PRINT_THINGS: #and PRINT_THINGS
                            print("----->Adding distance<-----: " + str(distance))
                        io.addDistance(distance)
                else:
                    last_latitude = latitude
                    last_longitude = longitude
                  
    time.sleep(0.03)


#cleanup
#gps_serial.close()
prog.end()
