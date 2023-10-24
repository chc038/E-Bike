#sudo pip install adafruit-mcp3008
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time
import io_functions as io
import prog
import subprocess


class InputAverage():
    def __init__(self, avg_num=10):
        self.num = avg_num
        self.vals = []
    def add(self, value):
        self.vals.append(value)
        if len(self.vals) > self.num:
            self.vals[:1] = []
    def get(self):
        return sum(self.vals) / len(self.vals)


def getCPUTemp():
    try:
        file = open('/sys/class/thermal/thermal_zone0/temp')
        content = file.read().strip()
        file.close()
        temp_int = content[:2]
        temp_dec = content[2:]
        return float(temp_int + "." + temp_dec)
    except ValueError:
        return None
    
def getMemoryInfo():
    info = subprocess.run("df -h /", shell=True, capture_output=True).stdout
    info = str(info)
    info = info.split("\\n")[1]
    info = info.split(" ")
    info = [item for item in info if item != '']
    return info[1:4]

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

battery_48v_average = InputAverage(15)
bus_12v_average = InputAverage(30)
main_current_average = InputAverage(15)
cpu_temperature_average = InputAverage(30)

prog.start()
while prog.isRunning():
    #info dictionary
    infos_adc = io.getInfosADC()
      
    #key switch
    key_switch = mcp.read_adc(0)
    if key_switch >= 768:
        infos_adc["key_switch"] = 0
    elif key_switch >= 256: #768 > key_switch >= 256
        infos_adc["key_switch"] = 1
    else:
        infos_adc["key_switch"] = -1

    #main battery voltage
    battery_48v = mcp.read_adc(7) * (3.3/1023.0) * 19.10
    battery_48v_average.add(battery_48v)
    infos_adc["battery_48v"] = battery_48v_average.get()
    
    #12v bus voltage
    bus_12v = mcp.read_adc(1) * (3.3/1023.0) * 5.78
    bus_12v_average.add(bus_12v)
    infos_adc["bus_12v"] = bus_12v_average.get()
     
    #main battery current
    cur_sen_vol = mcp.read_adc(6) * (3.3/1023.0) * 2.04
    main_current = (cur_sen_vol - 2.5) / 0.185
    main_current_average.add(main_current)
    infos_adc["main_current"] = main_current_average.get()
    
    #get cpu temperature
    cpu_temperature = getCPUTemp()
    if cpu_temperature != None:
        cpu_temperature_average.add(cpu_temperature)
        infos_adc["cpu_temperature"] = cpu_temperature_average.get()
    
    #get free memory
    memory = getMemoryInfo()
    infos_adc['memory'] = memory[2]
    
    #save info to file
    io.writeInfosADC(infos_adc)
    time.sleep(0.3)


prog.end()

