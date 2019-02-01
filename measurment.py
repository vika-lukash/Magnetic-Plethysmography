import matplotlib.pyplot as plt
from bitstring import BitArray
import serial
import os
import time


def parse_input_buffer(buf):
    null_bit = ord((buf[0])) & 1
    first_bit = (ord((buf[0])) & (1 << 1)) >> 1
    second_bit = (ord((buf[0])) & (1 << 2)) >> 2
    third_bit = (ord((buf[0])) & (1 << 3)) >> 3
    buf_int = []
    buf_int.append((ord((buf[1])) & 127) | (third_bit << 7))
    buf_int.append((ord((buf[2])) & 127) | (second_bit << 7))
    buf_int.append((ord((buf[3])) & 127) | (first_bit << 7))
    buf_int.append((ord((buf[4])) & 127) | (null_bit << 7))
    ch1 = (buf_int[0] << 24) | (buf_int[1] << 16) | (buf_int[2] << 8) | buf_int[3]
    if ch1 > 2**31:
        ch1 = ch1-2**32

    print("bulbul" + str(ch1 - 2**31))
   # ch1 = 0
    #k = 3
    #for num in buf:
     #   ch1 += num << k*8
      #  k = k-1
    return ch1


def read_one_byte(port):
    while port.in_waiting == 0:
        pass
    bt = port.read(1)
    return bt

def saveData(dirName, num, port1, port2):
    print("U1 = ", port1)
    print("U2= ", port2)


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

        port2.append(parse_input_buffer(half2))
        port1.append(parse_input_buffer(half1))
        print(port1[i])
        print(port2[i])

   #fileName = os.path.join("C:\Users\vika-\Magnetic-Plethysmography\popitka.txt")
    #if not os.path.exists(r'C:\Users\vika-\Magnetic-Plethysmography\'):
   # path = r'C:\Users\vika-\Magnetic-Plethysmography'
    #os.makedirs(path)

    fileName = dirName + "/%s.txt" % num
    os.makedirs(fileName)
    fileName = os.path.join(fileName, 'results')

    with open(fileName, "a") as file:
        for i in range(len(port1)):
            file.write(str(port1[i]) + " " + str(port2[i]))
            file.write("\n")
    plt.figure(1)
    plt.plot(range(len(port1)), port1)
    plt.plot(range(len(port2)), port2)
    plt.show()












 #if saving:
  #  try:
   #     os.mkdir(dirName)
    #except:
     #   pass
    #saveData(dirName, num, port1, port2)





def calibration(port,speed):
    run(port, speed, "calibration", message=b'\xFF', saving=False, uGraph=False, iGraph=True)




#if uGraph:
        #plt.figure(1)
       #plt.plot(range(len(port1)), port1)
        #plt.show()


#if iGraph:
 #   plt.figure(2)
  #  plt.plot(range(len(port2)), port2)
   # plt.show()










