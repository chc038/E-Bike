#sudo pip install mpu6050-raspberrypi
from mpu6050 import mpu6050
import time
import prog
import os
import io_functions as io


COSA = 0.9455185756 #19 deg
SINA = 0.3255681545
DATA_FOLDER = "/home/pi/Documents/Accel_Data"
DATA_HEADER = "tm(s),accel_x(m/s),accel_y(m/s),accel_z(m/s)"

class LoopTimer():
    def __init__(self):
        self.time = time.time()
    
    def wait_till(self, sleep_tm):
        time_now = time.time()
        while time_now - self.time < sleep_tm:
            time.sleep(0.0001)
            time_now = time.time()
        self.time = time_now


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
        to_write += content + '\n'
        with open(filename, 'a') as file:
            file.write(to_write)
            

mpu = mpu6050(0x68)
loop_timer = LoopTimer()
data_file = DataFile(DATA_FOLDER, DATA_HEADER)

prog.start()
while prog.isRunning():    
    try:
        #get data
        data = mpu.get_all_data()
        #print(data)
        accel_data = data[0]
        gyro_data = data[1]
        temp = data[2]
        
        #temp data
        new_data = {'temp': temp}
        
        #process acceleration data
#         acc_tang = {}
#         acc_tang['fb'] = -accel_data['x']*SINA + accel_data['y']*COSA
#         acc_tang['ud'] = accel_data['x']*COSA + accel_data['y']*SINA - 1
#         acc_tang['sd'] = accel_data['z']
        new_data['accel_x'] = accel_data['x']
        new_data['accel_y'] = accel_data['y']
        new_data['accel_z'] = accel_data['z']
        
        #process gyro data
        new_data['gyro_x'] = gyro_data['x']
        new_data['gyro_y'] = gyro_data['y']
        new_data['gyro_z'] = gyro_data['z']
        
        #write all data for use in other programs
        io.writeIMUData(new_data)
        
        #write accel data to storage
        data_str = ""
        data_str += str(round(time.time(), 2)) + ','
        data_str += str(round(accel_data['x'], 5)) + ','
        data_str += str(round(accel_data['y'], 5)) + ','
        data_str += str(round(accel_data['z'], 5))
        data_file.add_data_to_file(data_str)
                
    except Exception as e:
        print(repr(e))

    loop_timer.wait_till(0.2)


prog.end()
