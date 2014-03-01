import spidev
import time
import numpy as np

#Establish SPI connection with Bus 0, Device 0
spi = spidev.SpiDev()
spi.open(0,0)
numberOfSamplesToAcquire = 1000
AcquiringTime = 0
ADCdata = []

def get_adc(channel):
    #Perform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8+channel)<<4, 0])
    #Filter data bits from returned bits
    adcout = ((r[1]&3) << 8) + r[2]
    #Return value from 0-1023
    return adcout

print 'Starting acquiring', numberOfSamplesToAcquire, 'samples.'

startTimer = time.clock()
for i in range(numberOfSamplesToAcquire):
    ADCdata.append(get_adc(0))
    time.sleep(0.001)
    
AcquiringTime = (time.clock() - startTimer)

print 'ADC sampling time of', numberOfSamplesToAcquire, 'samples:', AcquiringTime, \
'\nNumber of samples pro second:', numberOfSamplesToAcquire/AcquiringTime, '[S/s]'
