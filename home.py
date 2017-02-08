#encoding=utf-8
import sqlite3
import time
import datetime
import pms7003
import si7021
import sht21


def get_db():
    conn = sqlite3.connect('sensors.db')
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS htpms
             (date integer, date_s text,  
             humi real, temp real,
	     pmcf10 integer, pmcf25 integer, pm100cf integer, 
	     pm10 integer, pm25 integer, pm100 integer, 
	     r03 integer, r05 integer, r10 integer, 
	     r25 integer, r50 integer, r100 integer
	     )''')
    return conn

def read_pms(ser):
    ret, pms = pms7003.read_native_pms(ser)
    if ret == False:
        pms = [-1] * 12
    return pms
 
def save_to_db(conn, time_i, time_s, humi, temp, pms):
    conn.cursor().execute("INSERT INTO htpms VALUES ({},'{}',{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(time_i, time_s,
                humi, temp,
                pms[0], pms[1], pms[2],
                pms[3], pms[4], pms[5],
                pms[6], pms[7], pms[8],
                pms[9], pms[10], pms[11]))

    conn.commit()

if __name__ == '__main__':
    '''
    '''
    with get_db() as conn:
        with pms7003.open_device("/dev/ttyUSB0") as ser: 
            while(True):
                time_i = round(time.time()*1000)
                time_s = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                pms = read_pms(ser)
                humi, temp = si7021.read_humi_temp()
                print "{} PM2.5: {}, Humidity: {:.2f}, Temprature: {:.2f}".format(time_s, pms[4], humi, temp)
		save_to_db(conn, time_i, time_s, humi, temp, pms)
                time.sleep(10)
