#encoding=utf-8
import os
import time
import serial
import sqlite3
from struct import *

def open_device(dev):
    return serial.Serial(dev, baudrate=9600, timeout=2.0)

def close_device(ser):
    ser.close()

def read_one_data(ser):
    rv = b''
    while True:
        ch1 = ser.read()
        if ch1 == b'\x42':
            ch2 = ser.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += ser.read(32)
                return rv

def read_native_pm(ser):
    recv = read_one_data(ser)
    length = unpack('>h', recv[2:4])[0]
    if length != 28:
        return (False, "the length of data is not equal 28.")
    data = unpack('>hhhhhhhhhhhhh', recv[4:30])
    check = unpack('>h', recv[30:32])[0]
    sum = 0x42 + 0x4d + 28
    for d in data:
        sum += (d & 0x00ff)
        sum += ((d & 0xff00)>>8)
    if check != sum:
        pass;#return (False, "check sum is not right, hope:actual, {}:{}".format(sum, check))
    return (True, data)

if __name__ == '__main__':
    ser = open_device("/dev/ttyUSB0")
    try:
        ret, data = read_native_pm(ser)
        ser.flushInput()
        if ret == False:
           print "read error: " , data
        print "version: ", (data[12] & 0xff00)>>8
        print "error code: ", (data[12] & 0x00ff)
        print(
              'PM1.0(CF=1): {}\n'
              'PM2.5(CF=1): {}\n'
              'PM10 (CF=1): {}\n'
              'PM1.0 (STD): {}\n'
              'PM2.5 (STD): {}\n'
              'PM10  (STD): {}\n'
              '>0.3um     : {}\n'
              '>0.5um     : {}\n'
              '>1.0um     : {}\n'
              '>2.5um     : {}\n'
              '>5.0um     : {}\n'
              '>10um      : {}\n'
              .format(data[0], data[1], data[2],
                                       data[3], data[4], data[5],
                                       data[6], data[7], data[8],
                                       data[9], data[10], data[11]))

    except KeyboardInterrupt:
        if ser != None:
            ser.close()
