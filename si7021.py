# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7021
# This code is designed to work with the SI7021_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SI7021_I2CS#tabs-0-product_tabset-2

import smbus
import time

addr = 0x40 # SI7021 address, 0x40(64)
cmd_humi = 0xF5 // no hold master mode
cmd_temp = 0xF3 // no hold master mode
cmd_reset = 0xFE

def get_bus():
    return smbus.SMBus(1)

def read_humi(bus):
    bus.write_byte(addr, cmd_humi)
    time.sleep(0.3)

    # Read data back, 2 bytes, Humidity MSB first
    data0 = bus.read_byte(addr)
    data1 = bus.read_byte(addr)

    # Convert the data
    humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
    return humidity

def read_temp(bus):
    bus.write_byte(addr, cmd_temp)
    time.sleep(0.3)

    # Read data back, 2 bytes, Temperature MSB first
    data0 = bus.read_byte(addr)
    data1 = bus.read_byte(addr)

    # Convert the data
    cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
    fTemp = cTemp * 1.8 + 32
    return cTemp

if __name__ == '__main__':
    bus = get_bus()
    humidity = read_humi(bus)
    time.sleep(0.3)
    cTemp = read_temp(bus)
    print "Relative Humidity is : %.2f %%" %humidity
    print "Temperature in Celsius is : %.2f C" %cTemp
