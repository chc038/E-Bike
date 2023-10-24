import time
import calendar
import serial
import gps_functions
import io_functions as io
import security_functions as security
import prog


PRINT_THINGS = False


class GPS_module():

    def __init__(self):
        """create a GPS_module object"""
        self.buffer = ''
        self.lat = 0.0
        self.log = 0.0
        self.lat_old = 0.0
        self.log_old = 0.0
        self.speed = 0.0
        self.time = 0
        self.sent_count = 0

    def add(self, info_string):
        """add new strings to buffer"""
        self.buffer += info_string

    def get_degree(self, deg_min):
        """get degree as a float from a string od form ddmm.mm or dddmm.mm"""
        if len(deg_min) >= 7 and '.' in deg_min: #should be of form ddmm.mm
            try:
                ind_dot = deg_min.index('.') #find the dot's index
                degree = float(deg_min[:ind_dot-2]) #first 2 characters are degree
                minute = float(deg_min[ind_dot-2:]) #the rest is minutes
                degree = degree + minute/60 #get the latitude in degrees with decimals
                return degree
            except ValueError:
                return 0.0
        else:
            return 0.0
    
    def find_time(self, time_str, format_str):
        try:
            utc_tm = time.strptime(time_str, format_str)
            return calendar.timegm(utc_tm)
        except ValueError:
            return 0.0

    def check_sentence(self, sentence):
        """check to see if the sentence is NMEA sentence and get gps info if so"""
        if '*' in sentence: #correct sentence has $ in front and * before checksum
            sentence = sentence.split(',') #split the sentence with comma
            if '$GPRMC' in sentence or '$GNRMC' in sentence: #GPRMC: Recormmended minimum specific GPS/Transit data
                if len(sentence) >= 10: #first 10 things will be used
                    if PRINT_THINGS:
                        print("----->$GPRMC/$GNRMC<-----")
                    warning = sentence[2] #2nd term is warning
                    if warning == 'A': #A for OK
                        #get latitude
                        latitude = sentence[3] #3rd term should be latitude
                        latitude = self.get_degree(latitude) #get the latitude in degrees
                        if sentence[4] == 'N':
                            self.lat = latitude #positive for northern hemisphere
                        elif sentence[4] == 'S':
                            self.lat = -latitude #negative for southern hemisphere
                        #get logitude
                        logitude = sentence[5] #5th term should be logitude
                        logitude = self.get_degree(logitude)
                        if sentence[6] == 'E':
                            self.log = logitude #positive for east
                        elif sentence[6] == 'W':
                            self.log = -logitude #negative for west
                        #get time
                        utc_tm = sentence[1] #1st term is utc time
                        utc_da = sentence[9] #9th term is utc date
                        if len(utc_tm) == 9 and len(utc_da) == 6: #it should be time: hhmmss.ss, date: ddmmyy
                            utc_tm = utc_tm[:6] #get hhmmss
                            self.time = self.find_time(utc_tm+' '+utc_da, '%H%M%S %d%m%y')
                        #get speed
                        speed = sentence[7]
                        try: 
                            self.speed = float(speed) / 1.94384 #convert to m/s
                        except ValueError:
                            self.speed = 0.0
                    elif warning == 'V': #V for warning
                        self.lat = 0.0
                        self.log = 0.0
                        self.time = 0
                    self.sent_count = 0 #initialize the sentence count
                
            elif (self.sent_count > 64 and
                  ('$GPGGA' in sentence or '$GNGGA' in sentence)): #GPGGA: GPS Fix Data. used if $GPRMC does not appear
                if len(sentence) >= 6: #first 6 things will be used
                    if PRINT_THINGS:
                        print("----->$GPGGA/$GNGGA<-----")
                    #get latitude
                    latitude = sentence[2] #second term should be latitude
                    latitude = self.get_degree(latitude) #get the latitude in degrees
                    if sentence[3] == 'N':
                        self.lat = latitude #positive for northern hemisphere
                    elif sentence[3] == 'S':
                        self.lat = -latitude #negative for southern hemisphere
                    #get logitude
                    logitude = sentence[4] #4th term should be logitude
                    logitude = self.get_degree(logitude)
                    if sentence[5] == 'E':
                        self.log = logitude #positive for east
                    elif sentence[5] == 'W':
                        self.log = -logitude #negative for west
                    #get time
                    utc_tm = sentence[1] #first term after $GPGGA is utc time
                    if len(utc_tm) == 9: #should be of form hhmmss.ss
                        utc_tm = utc_tm[:6] #get hhmmss
                        self.time = self.find_time(utc_tm, '%H%M%S')

            self.sent_count += 1 #incriment sentence count
    
    def check_info(self):
        """return true if this info look normal"""
        if not (self.lat == 0.0 and self.log == 0.0) and self.time != 0.0:
            return True
        else:
            return False
    
    def check(self):
        """check to see if there are NMEA sentences in the buffer and read gps info from the sentences"""
        while '\n' in self.buffer and '$' in self.buffer: #check for line change
            ind = self.buffer.index('\n') #find the end of the sentence
            sentence = self.buffer[:ind].strip() #get the sentence
            self.buffer = self.buffer[ind+1:] #remove the sentence from buffer
            self.check_sentence(sentence)
            if PRINT_THINGS:
                print(sentence)

    def update(self, info_string):
        self.add(info_string)
        self.check()
    
    def getDistance(self):
        if (self.lat_old, self.log_old) != (0.0, 0.0):
            distance = 0
            if self.lat != self.lat_old or self.log != self.log_old:
                #get distance
                distance = gps_functions.findDistance(self.lat_old, self.log_old,
                                                      self.lat, self.log)
                if distance > 10: #update old location when moved sufficiently far
                    self.lat_old = self.lat
                    self.log_old = self.log
                    if distance > 1000: #remove erratic/unreasonable distances
                        distance = 0
                else:
                    distance = 0
            if distance != 0 and PRINT_THINGS: #and PRINT_THINGS
                print("----->Adding distance<-----: " + str(distance))
            return(distance)
        else:
            self.lat_old = self.lat
            self.log_old = self.log
            return 0

    def get_lat(self):
        return self.lat

    def get_log(self):
        return self.log

    def get_time(self):
        return self.time

    def get_speed(self):
        return self.speed



# info = """$GPRMC,203116.00,A,3252.23831,N,11713.00096,W,1.480,,311221,,,A*6A
# $GPVTG,,T,,M,1.380,N,2.555,K,A*2E
# $GPGGA,203116.00,3252.23831,N,11713.00096,W,1,03,3.93,202.9,M,-33.8,M,,*68
# $GPGSA,A,2,09,20,07,,,,,,,,,,4.06,3.93,1.00*05
# $GPGSV,3,1,11,03,21,179,,04,62,098,,07,47,292,13,08,25,126,*70
# $GPGSV,3,2,11,09,70,342,18,14,01,215,26,16,33,045,,20,05,322,24*78
# $GPGSV,3,3,11,22,02,168,,27,25,091,,30,22,272,17*4C
# $GPGLL,3252.23831,N,11713.00096,W,203116.00,A,A*7B
# """

#$GNRMC,162526.00,A,4111.94360,N,07314.85951,W,2.147,,261222,,,A*73
#$GNVTG,,T,,M,2.147,N,3.976,K,A*36
#$GNGGA,162526.00,4111.94360,N,07314.85951,W,1,06,3.50,36.3,M,-34.2,M,,*46
#$GNGSA,A,3,10,01,03,22,31,32,,,,,,,4.98,3.50,3.54*1D
#$GNGSA,A,3,,,,,,,,,,,,,4.98,3.50,3.54*1D
#$GPGSV,3,1,12,01,05,268,11,03,31,309,14,04,00,301,,10,07,169,11*70
#$GPGSV,3,2,12,12,03,036,10,16,09,200,,22,78,054,11,25,29,048,*7D
#$GPGSV,3,3,12,26,42,193,15,29,13,095,,31,76,342,08,32,49,111,08*79
#$GLGSV,2,1,08,65,22,143,,66,81,122,,67,41,326,,75,13,038,*6B
#$GLGSV,2,2,08,76,70,023,,77,54,231,,78,00,222,,84,03,009,*60
#$GNGLL,4111.94360,N,07314.85951,W,162526.00,A,A*6D

info = ""

# /dev/ttyS0 or /dev/ttyACM0
gps_serial = serial.Serial("/dev/ttyS0", 9600, timeout = 0.001)
gps = GPS_module()

prog.start()
while prog.isRunning():
    try:
        if gps_serial.in_waiting > 0: #see if there are content in serial port
            info = gps_serial.read(gps_serial.in_waiting).decode("utf-8")
            gps.update(info) #add the content to internal buffer of gps
    except UnicodeDecodeError:
        print(__file__ + ": serial decode error")

    if gps.check_info(): #if info looks right
        gps_functions.writeGPSInfo(latitude=gps.get_lat(), logitude=gps.get_log(),
                                    speed=gps.get_speed(), tme=gps.get_time())
        if security.lockState() == '0': #when unlocked
            io.addDistance(gps.getDistance())
    
    time.sleep(0.1)


#cleanup
#gps_serial.close()
prog.end()
