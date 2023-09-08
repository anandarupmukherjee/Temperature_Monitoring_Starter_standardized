
import math
from smbus2 import SMBus
from mlx90614 import MLX90614
from w1thermsensor import W1ThermSensor
import max6675
import adafruit_ahtx0
import board
import logging
import importlib


# import sys
# sys.path.append(docker exec -it )
# from DFRobot_MAX31855 import *

logger = logging.getLogger("main.measure.sensor")


adc_module = "DFRobot_MAX31855"
try:
    local_lib = importlib.import_module(f"adc.{adc_module}")
    logger.debug(f"Imported {adc_module}")
except ModuleNotFoundError as e:
    logger.error(f"Unable to import module {adc_module}. Stopping!!")






class k_type:
    # https://github.com/DFRobot/DFRobot_MAX31855/tree/main/raspberrypi/python
    def __init__(self):
        self.I2C_1       = 0x01
        self.I2C_ADDRESS = 0x10
        #Create MAX31855 object
        self.max31855 = local_lib.DFRobot_MAX31855(self.I2C_1 ,self.I2C_ADDRESS) 
        

    def ambient_temp(self):
        logger.info("TemperatureMeasureBuildingBlock- k-type started")
        return self.max31855.read_celsius() 



class MLX90614_temp:
    def __init__(self):
        self.bus = SMBus(1)
        self.sensor=MLX90614(self.bus,address=0x5a)

    def ambient_temp(self):
        logger.info("TemperatureMeasureBuildingBlock- MLX90614_temp started")
        return self.sensor.get_amb_temp()

    def object_temp(self):
        return self.sensor.get_obj_temp()
        


class sht30:
    def __init__(self):
        self.bus = SMBus(1)
        self.bus.write_i2c_block_data(0x44, 0x2C, [0x06])
        time.sleep(0.5)
        self.data = self.bus.read_i2c_block_data(0x44, 0x00, 6)

    def ambient_temp(self):
        logger.info("TemperatureMeasureBuildingBlock- SHT30 started")
        self.temp = self.data[0] * 256 + self.data[1]
        return -45 + (175 * self.temp / 65535.0)



class W1Therm:
    def __init__(self):
        self.sensor = W1ThermSensor()
        

    def ambient_temp(self):
        logger.info("TemperatureMeasureBuildingBlock- w1therm started")
        return self.sensor.get_temperature()


# class k_type:
#     # https://github.com/archemius/MAX6675-Raspberry-pi-python/blob/master/temp_read_1_sensor.py
#     def __init__(self):
#         self.cs = 23
#         self.sck = 24
#         self.so = 25
#         max6675.set_pin(self.cs, self.sck, self.so, 1) #[unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
        

#     def ambient_temp(self):
#         logger.info("TemperatureMeasureBuildingBlock- k-type started")
#         return max6675.read_temp(self.cs)



class aht20:
    def __init__(self):
        # self.bus = SMBus(1)
        # self.sensor=adafruit_ahtx0.AHTx0(self.bus,address=0x38)
        i2c = board.I2C()
        self.sensor = adafruit_ahtx0.AHTx0(i2c)
        
    def ambient_temp(self):
        logger.info("TemperatureMeasureBuildingBlock- aht20 started")
        return self.sensor.temperature
