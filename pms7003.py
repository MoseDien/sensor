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

def read_native_pms(ser):
    recv = read_one_data(ser)
    length = unpack('>h', recv[2:4])[0]
    if length != 28:
        return (False, "the length of data is not equal 28.")
    pms = unpack('>hhhhhhhhhhhhh', recv[4:30])

    # check sum
    check = unpack('>h', recv[30:32])[0]
    sum = 0x42 + 0x4d + 28
    for pm in pms:
        sum += (pm & 0x00ff)
        sum += ((pm & 0xff00)>>8)
    if check != sum:
        return (False, "check sum is not right, hope:actual, {}:{}".format(sum, check))

    return (True, pms)

if __name__ == '__main__':
    with open_device("/dev/ttyUSB0") as ser:
        ret, pms = read_native_pms(ser)
	ser.flushInput()
        if ret == False:
           print "read error: " , pms
        print "version: ", (pms[12] & 0xff00)>>8
        print "error code: ", (pms[12] & 0x00ff)
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
              .format(pms[0], pms[1], pms[2],
                                       pms[3], pms[4], pms[5],
                                       pms[6], pms[7], pms[8],
                                       pms[9], pms[10], pms[11]))

