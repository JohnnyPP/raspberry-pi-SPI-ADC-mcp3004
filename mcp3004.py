import spidev
import time
import numpy as np


#Establish SPI connection with Bus 0, Device 0
spi = spidev.SpiDev()
spi.open(0,0)
ADCdata = []
AcquiringTime = []

def get_adc(channel):
    #Perform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8+channel)<<4, 0])
    #Filter data bits from returned bits
    adcout = ((r[1]&3) << 8) + r[2]
    #Return value from 0-1023
    return adcout

for i in range(10):   
    startTimer = time.clock()
    for i in range(10000):
        ADCdata.append(get_adc(0))
    
    AcquiringTime.append(time.clock() - startTimer)

print 'Mean ADC sampling time of 10000 samples:', "{0:.4f}".format(np.mean(AcquiringTime)), \
'[s]' '\nstandard deviation:', "{0:.4f}".format(np.std(AcquiringTime)), '[s]'



#while True:
    #print get_adc(0)
    #time.sleep(1)
