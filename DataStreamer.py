import socket
import struct
import time
import sys


def readVehiclePath(fPath):

    print('Reading data from file.')

    fConn = open(fPath, 'r')
    fConn.readline()
    vPath = [list(map(float, cLine.split(','))) for cLine in fConn]
    fConn.close()

    return vPath


def getSocketConnection(ipAddr, portNo):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    s.connect((ipAddr, portNo))

    return s


def simulateStream(fPath, ip, port, debug=False, loop=True, rate=0.016666):

    vPath = readVehiclePath(fPath)
    dataRows = len(vPath)
    s = getSocketConnection(ip, port)

    print('Stream Started from first line of data in the file.')

    try:

        i = 0

        while True:
        
            i = i + 1
        
            # 5f converts the floats to single precision
            # 5d converts the floats to double precision
        
            dataToSend = vPath[i-1]
            fmtStr = '{:d}f'.format(len(dataToSend))
            bufData = struct.pack(fmtStr, *dataToSend)
            s.send(bufData)
        
            if debug: print(dataToSend)
        
            time.sleep(rate)
        
            if i == dataRows: 
                
                print('Starting again from first line of data.')
                if not loop: break
                i = 0

    except:

        print('Streaming stopped.')
        s.close()


if __name__ == '__main__':

    fPath = sys.argv[1]
    ipAddr = sys.argv[2]
    portNo = int(sys.argv[3])

    simulateStream(fPath, ipAddr, portNo)