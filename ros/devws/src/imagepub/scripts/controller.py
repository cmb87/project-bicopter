import pygame
from time import sleep
from pySerialTransfer import pySerialTransfer as txfer

print("Init....")
pygame.init()
window = pygame.display.set_mode((300, 300))

clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS', 30)

rect = pygame.Rect(0, 0, 20, 20)
rect.center = window.get_rect().center
vel = 2

run = True

# =========================
class CommandStruct(object):
    angle1 = 90
    angle2 = 90
    angle3 = 90
    angle4 = 90
    angle5 = 90

class SensorStruct(object):
    range1 = 0.0
    range2 = 0.0
    angle1 = 90
    angle2 = 90
    angle3 = 90
    angle4 = 90
    angle5 = 90


cmdStruct = CommandStruct
# =========================

try:
    print("Connecting....")
    link = txfer.SerialTransfer('COM3')
    link.open()
    sleep(5)
    print("starting")
        
    while run:


        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
            # print(pygame.key.name(event.key))
                pass

        keys = pygame.key.get_pressed()
        

        cmdStruct.angle2 += 2*int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) 
        cmdStruct.angle1 += 2*int(keys[pygame.K_DOWN] - keys[pygame.K_UP]) 
        cmdStruct.angle3 += 2*int(keys[pygame.K_w] - keys[pygame.K_s]) 
        cmdStruct.angle4 += 2*int(keys[pygame.K_e] - keys[pygame.K_d]) 
        cmdStruct.angle5 += 2*int(keys[pygame.K_r] - keys[pygame.K_f]) 


        sendSize = 0
        sendSize += link.tx_obj([cmdStruct.angle1,cmdStruct.angle2,cmdStruct.angle3,cmdStruct.angle4,cmdStruct.angle5], start_pos=sendSize)

        link.send(sendSize)
    
        ###################################################################
        # Wait for a response and report any errors while receiving packets
        ##################################################################
        while not link.available():
            if link.status < 0:
                if link.status == txfer.CRC_ERROR:
                    print('ERROR: CRC_ERROR')
                elif link.status == txfer.PAYLOAD_ERROR:
                    print('ERROR: PAYLOAD_ERROR')
                elif link.status == txfer.STOP_BYTE_ERROR:
                    print('ERROR: STOP_BYTE_ERROR')
                else:
                    print('ERROR: {}'.format(link.status))


        recSize = 0
        SensorStruct.range1 = link.rx_obj(obj_type='f', start_pos=recSize)
        recSize += txfer.STRUCT_FORMAT_LENGTHS['f']
        
        SensorStruct.range2 = link.rx_obj(obj_type='f', start_pos=recSize)
        recSize += txfer.STRUCT_FORMAT_LENGTHS['f']

        SensorStruct.angle1 = link.rx_obj(obj_type='i', start_pos=recSize)
        recSize += txfer.STRUCT_FORMAT_LENGTHS['i']

        SensorStruct.angle2 = link.rx_obj(obj_type='i', start_pos=recSize)
        recSize += txfer.STRUCT_FORMAT_LENGTHS['i']

        SensorStruct.angle3 = link.rx_obj(obj_type='i', start_pos=recSize)
        recSize += txfer.STRUCT_FORMAT_LENGTHS['i']

        SensorStruct.angle4 = link.rx_obj(obj_type='i', start_pos=recSize)
        recSize += txfer.STRUCT_FORMAT_LENGTHS['i']

        SensorStruct.angle5 = link.rx_obj(obj_type='i', start_pos=recSize)
        recSize += txfer.STRUCT_FORMAT_LENGTHS['i']




        print(f"{cmdStruct.angle1}, {cmdStruct.angle2}, {cmdStruct.angle3}, {cmdStruct.angle4}, {cmdStruct.angle5}, {SensorStruct.range1}, {SensorStruct.range2}, {SensorStruct.angle1}, {SensorStruct.angle2}, {SensorStruct.angle3}, {SensorStruct.angle4}, {SensorStruct.angle5}")



except KeyboardInterrupt:
    link.close()


pygame.quit()
exit()