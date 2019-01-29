import matplotlib.pyplot as plt
from bitstring import BitArray
import serial
import os
import time

def parse_input_buffer(buf):
    null_bit = buf[0] & 1
    first_bit = (buf[0] & 1 << 1) >> 1
    second_bit = (buf[0] & 1 << 2) >> 2
    third_bit = (buf[0] & 1 << 3) >> 3
    buf[1] = buf[1] | third_bit << 7
    buf[2] = buf[2] | second_bit << 7
    buf[3] = buf[3] | first_bit << 7
    buf[4] = buf[4] | null_bit << 7
    ch1 = bytearray(buf[1])
    ch1.append(buf[2])
    ch1.append(buf[3])
    ch1.append(buf[4])
    ch1 = int.from_bytes(ch1, byteorder='little')
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
    print(bin(int(86, 16))[2:].zfill(8))

    for i in range(len(full_data)):
        data1 = full_data[i]
        half1 = data1[:6]
        half2 = data1[5:]
        port1.append(parse_input_buffer(half1))
        port2.append(parse_input_buffer(half2))

