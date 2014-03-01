import spidev
import time
import numpy as np


#Establish SPI connection with Bus 0, Device 0
spi = spidev.SpiDev()
spi.open(0,0)
numberOfSamplesToAcquire = 10000
numberOfMeasurements = 10
ADCdata = []
AcquiringTime = []

def get_adc(channel):
    #Perform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8+channel)<<4, 0])
    #Filter data bits from returned bits
    adcout = ((r[1]&3) << 8) + r[2]
    #Return value from 0-1023
    return adcout

print 'Starting acquiring', numberOfSamplesToAcquire, 'samples.' \
 '\nNumber of measuements in a row: ', numberOfMeasurements

for i in range(numberOfMeasurements):   
    startTimer = time.clock()
    for i in range(numberOfSamplesToAcquire):
        ADCdata.append(get_adc(0))
    
    AcquiringTime.append(time.clock() - startTimer)

meanTime = np.mean(AcquiringTime)

print 'Mean ADC sampling time of', numberOfSamplesToAcquire, 'samples:', "{0:.4f}".format(meanTime), \
'[s]' '\nStandard deviation:', "{0:.4f}".format(np.std(AcquiringTime)), '[s]' \
'\nNumber of samples pro second:', numberOfSamplesToAcquire/meanTime, '[S/s]'
