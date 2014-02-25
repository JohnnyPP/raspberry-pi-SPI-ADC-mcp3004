import spidev
import time
import numpy as np
from threading import Thread
from Queue import Queue

queue = Queue(10)

spi = spidev.SpiDev()
spi.open(0,0)
numberOfSamplesToAcquire = 9
ADCdata = []
AcquiringTime = []

def get_adc(channel):
    #Perform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8+channel)<<4, 0])
    #Filter data bits from returned bits
    adcout = ((r[1]&3) << 8) + r[2]
    #Return value from 0-1023
    return adcout
    
class ProducerThread(Thread):
    def run(self):
        global queue      
        for i in range(numberOfSamplesToAcquire):
            queue.put(get_adc(0))
            
class ConsumerThread(Thread):
    def run(self):
        global queue   
        for i in range(numberOfSamplesToAcquire):
            ADCdata.append(queue.get())


ProducerThread().start()
ConsumerThread().start()

print 'Done!'
#for i in range(10):   
#    startTimer = time.clock()
#    for i in range(numberOfSamplesToAcquire):
#        ADCdata.append(get_adc(0))
    
#    AcquiringTime.append(time.clock() - startTimer)

#meanTime = np.mean(AcquiringTime)

#print 'Mean ADC sampling time of', numberOfSamplesToAcquire, 'samples:', "{0:.4f}".format(meanTime), \
#'[s]' '\nStandard deviation:', "{0:.4f}".format(np.std(AcquiringTime)), '[s]' \
#'\nNumber of samples pro second:', numberOfSamplesToAcquire/meanTime, '[S/s]'
