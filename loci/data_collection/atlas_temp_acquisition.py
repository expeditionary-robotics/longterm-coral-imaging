"""Code to stream or log data from Atlas Scientific P1000 probe.

Use: 
python3 loci/data_collection/atlas_temp_acquisition.py  -r 5 -w ./output/test_temp_logging -n temp_test.txt

Adapted from Atlas Scientific Raspberry Pi Examples Code, uart.py
"""

#!/usr/bin/python3

import serial
import sys
import os
import time
import argparse
from serial import SerialException

def read_line():
    """
    taken from the ftdi library and modified to 
    use the ezo line separator "\r"
    """
    lsl = len(b'\r')
    line_buffer = []
    while True:
        next_char = ser.read(1)
        if next_char == b'':
            break
        line_buffer.append(next_char)
        if (len(line_buffer) >= lsl and
                line_buffer[-lsl:] == [b'\r']):
            break
    return b''.join(line_buffer)
    
def read_lines():
    """
    also taken from ftdi lib to work with modified readline function
    """
    lines = []
    try:
        while True:
            line = read_line()
            if not line:
                break
                ser.flush_input()
            lines.append(line)
        return lines
    
    except SerialException as e:
        print( "Error, ", e)
        return None	

def send_cmd(cmd):
    """
    Send command to the Atlas Sensor.
    Before sending, add Carriage Return at the end of the command.
    :param cmd:
    :return:
    """
    buf = cmd + "\r"     	# add carriage return
    try:
        ser.write(buf.encode('utf-8'))
        return True
    except SerialException as e:
        print ("Error, ", e)
        return None
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Getting thermister recording information.")
    parser.add_argument("-w", "--write_path", type=str, action="store", default=os.getenv("OUTPUT_DIR"), help="Provide a target to write files")
    parser.add_argument("-n", "--file_name", type=str, action="store", default="temp_test.txt", help="Name of file to write temperature data")
    parser.add_argument("-r", "--logging_rate", type=int, action="store", default=1, help="Rate at which to log temperature, Hz")
    
    args = parser.parse_args()
    file_path = args.write_path
    file_target = os.path.join(file_path, args.file_name)
    polling_rate = args.logging_rate

    # Make the write path target if it is not already in existence
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)

    # to get a list of ports use the command: 
    # python -m serial.tools.list_ports
    # in the terminal
    usbport = '/dev/ttyUSB0' # change to match your pi's setup 

    print( "Opening serial port now...")

    try:
        ser = serial.Serial(usbport, 9600, timeout=0)  # put in continuous mode
    except serial.SerialException as e:
        print( "Error, ", e)
        sys.exit(0)

    while True:
        delaytime = float(polling_rate)
    
        send_cmd("C,0") # turn off continuous mode
        #clear all previous data
        time.sleep(1)
        ser.flush()
            
        # get the information of the board you're polling
        print("Polling sensor every %0.2f seconds, press ctrl-c to stop polling" % delaytime)
    
        try:
            while True:
                send_cmd("R")
                lines = read_lines()
                response_time = time.time_ns()
                for i in range(len(lines)):
                    # print lines[i]
                    if lines[i][0] != b'*'[0]:
                        data = str(lines[i].decode('utf-8')).strip("/n")
                        with open(file_target, 'a') as f:
                            data_string = str(response_time) + "," + str(data) + "\n"
                            f.write(data_string)
                        print("Response at ", response_time, ": ", data)
                time.sleep(delaytime)

        except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
            print("Continuous polling stopped")
