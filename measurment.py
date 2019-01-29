import matplotlib.pyplot as plt
from bitstring import BitArray
import serial
import os
import time

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def parse_input_buffer(buf):
    null_bit = int.from_bytes(buf[0], byteorder='little') & 1
    first_bit = (int.from_bytes(buf[0], byteorder='little') & 1 << 1) >> 1
    second_bit = (int.from_bytes(buf[0], byteorder='little') & 1 << 2) >> 2
    third_bit = (int.from_bytes(buf[0], byteorder='little') & 1 << 3) >> 3
    buf[1] = int.from_bytes(buf[1], byteorder='little') | third_bit << 7
    buf[2] = int.from_bytes(buf[2], byteorder='little') | second_bit << 7
    buf[3] = int.from_bytes(buf[3], byteorder='little') | first_bit << 7
    buf[4] = int.from_bytes(buf[4], byteorder='little') | null_bit << 7
    ch1 = int.from_bytes(int_to_bytes(buf[1]+buf[2]+buf[3]+buf[4]), byteorder='little')
    return ch1


def read_one_byte(port):
    while port.in_waiting == 0:
        pass
    bt = port.read(1)
    return bt


def run(port, speed, dirName, num=1, message=b'\01', saving=True, uGraph=True, iGraph=False):
    ser = serial.Serial(port=port,
                        baudrate=speed,
                        # stopBits=selectedStopBits
                        )  # open serial port

    print(ser.getSettingsDict())
    ser.isOpen()

    ser.write(message)
    data = ""

    full_data = []
    start = False
    endMeasurement = False

    while not start:
        one_byte = read_one_byte(ser)
        if one_byte == b'\x0f':
            start = True
            print("Started")
    print("Out of loop")
    while not endMeasurement:
        data = []
        one_byte = read_one_byte(ser)
        if one_byte == b'\x07':
            print("Ended")
            break
        print("Not end")
        data.append(one_byte)
        while len(data) != 10:
            one_byte = read_one_byte(ser)
            data.append(one_byte)
        print(data)
        full_data.append(data)

    ser.close()
    port1 = []
    port2 = []


    for i in range(len(full_data)):
        data1 = full_data[i]
        half1 = data1[:6]
        half2 = data1[5:]
        port1.append(parse_input_buffer(half1))
        port2.append(parse_input_buffer(half2))

