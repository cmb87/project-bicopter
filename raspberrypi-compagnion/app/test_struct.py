import sys
import serial, time, struct

data = [1500,1500,2000,1000, 1500,1500,2000,1000]
data_length = 16
data_format = "<8H"

print(data_length)

checksum = 0
total_data = ['$'.encode('utf-8'), 'M'.encode('utf-8'), '<'.encode('utf-8'), data_length, 200] + data

d1 = struct.pack('<2B'+data_format, *total_data[3:len(total_data)])

for i in d1:
    checksum = checksum ^ i
total_data.append(checksum)


print(total_data)