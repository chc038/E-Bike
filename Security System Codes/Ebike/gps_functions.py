import json
import time
import math


def getGPS():
    file = open("GPS_Files/gps_info.json", 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return None

def getGPSLocation():
    gps_info = getGPS()
    if gps_info != None:
        return (str(round(gps_info['latitude'],6)) + ','+
                str(round(gps_info['logitude'], 6)))
    else:
        return ""

def getGPSSpeed():
    gps_info = getGPS()
    if gps_info != None:
        return gps_info['speed']
    else:
        return None

def getGPSAge():
    gps_info = getGPS()
    if gps_info != None:
        gps_time = gps_info['time']
        return time.time() - gps_time
    else:
        return None

def strfGPSAge():
    age = getGPSAge()
    if age != None:
        age_hour = int(age / 3600)
        age_min = int((age % 3600) / 60)
        age_sec = int(age % 60)
        if age_hour > 0:
            return str(age_hour)+"h "+str(age_min)+"m "+str(age_sec)+"s"
        elif age_min > 0:
            return str(age_min)+"m "+str(age_sec)+"s"
        else:
            return str(age_sec)+"s"
    else:
        return ""

def strfGPSInfo():
    gps_str = "\nGPS INFO\n"
    gps_str += "Location: " + str(getGPSLocation()) + "\n"
    gps_str += "Speed: " + str(getGPSSpeed()) + "m/s \n"
    gps_str += "Age: " + str(strfGPSAge()) + "\n"
    return gps_str

def writeGPS(gps_info):
    file = open("GPS_Files/gps_info.json", 'w')
    file.write(json.dumps(gps_info, indent=2))
    file.close()

def writeGPSInfo(latitude, logitude, speed, tme):
    gps_info = {'latitude': latitude, 'logitude': logitude, 'speed': speed, 'time': tme}
    writeGPS(gps_info)
    
def findDistance(lat1, log1, lat2, log2):
    R = 6371000 # radius of earth in metres
    lat1_rad = lat1 * math.pi / 180
    lat2_rad = lat2 * math.pi / 180
    d_lat = (lat2_rad - lat1_rad)
    d_log = (log2 - log1) * math.pi / 180
    a = math.sin(d_lat/2)**2 + math.cos(lat1_rad)*math.cos(lat2_rad) * math.sin(d_log/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # in metres
    return d

def setParkLocation():
    file = open("GPS_Files/gps_info.json", 'r')
    content = file.read()
    file.close()
    if content != None:
        file = open("GPS_Files/park_location.json", 'w')
        file.write(content)
        file.close()
        return True
    else:
        return False

def getParkLocation():
    file = open("GPS_Files/park_location.json", 'r')
    content = file.read()
    file.close()
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        return None

