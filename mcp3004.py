import spidev
import time
import numpy as np

#Establish SPI connection with Bus 0, Device 0
spi = spidev.SpiDev()
spi.open(0,0)
numberOfSamplesToAcquire = 100
AcquiringTime = 1
ADCdata = []
i = 0
startTimer = time.clock()

def get_adc(channel):
    #Perform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8+channel)<<4, 0])
    #Filter data bits from returned bits
    adcout = ((r[1]&3) << 8) + r[2]
    #Return value from 0-1023
    return adcout

print 'Starting acquiring', numberOfSamplesToAcquire, 'samples.'

startTimer = time.time()

#while i<numberOfSamplesToAcquire:
#    ADCdata.append(get_adc(0))
#    print get_adc(0)
#    i=i+1
#    time.sleep(0.01)  
#AcquiringTime = (time.time() - startTimer)

startTimer = time.time()
for i in range(numberOfSamplesToAcquire):
    ADCdata.append(get_adc(0))
    time.sleep(0.01)    
AcquiringTime = (time.time() - startTimer)

print 'ADC sampling time of', numberOfSamplesToAcquire, 'samples:', AcquiringTime,
print '\nNumber of samples pro second:', numberOfSamplesToAcquire/AcquiringTime, '[S/s]'
#print ADCdata[0]