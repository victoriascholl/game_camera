import RPi.GPIO
import picamera
import time
import Adafruit_TMP.TMP006 as TMP006
import numpy
import os
import datetime
import sys

# Converts temp sensor reading from Celsius to Fahrenheit if desired
def c_to_f(c):       
   return c * 9.0 / 5.0 + 32.0

# Builds  string command to send email with specified image
def email_image(image, toAddress = 'vms3476@rit.edu', 
   fromAddress = 'vms3476@rit.edu', subject = 'Game camera detection',
   smtpServer = 'mail.cis.rit.edu', message = 'Image captured'):

   sendEmailString = 'sendEmail '
   try:
      sendEmailString += ' -f ' + str(fromAddress)
      sendEmailString += ' -t ' + str(toAddress)
      sendEmailString += ' -a ' + str(image)
      sendEmailString += ' -s ' + str(smtpServer)
      sendEmailString += ' -m ' + str(message)
   except ValueError:
      print 'You need to supply all 4 parameters: '
      print 'fromAddress, toAddress, image, smtpServer'

   if subject:
      sendEmailString += ' -u ' + str(subject)
      os.system(sendEmailString)

   return 'image sent to ' + str(toAddress)



def detection(triggerPin1, triggerPin2, filename, ext, toAddress, \
              sensorInterval, detectionThresh):
   
   # Declares Broadcom GPIO pin layout   
   RPi.GPIO.setmode(RPi.GPIO.BCM)
 
   RPi.GPIO.setup(triggerPin1, RPi.GPIO.OUT) # Pins as OUTPUTS
   RPi.GPIO.setup(triggerPin2, RPi.GPIO.OUT)

   # Creates temp sensor object
   tempSensor = TMP006.TMP006()       
   tempSensor.begin()

   try:

      # Obtains average for 5 temp readings
      counter = 0                            
      readings = []
      while counter < 5:              
         readings.append(tempSensor.readObjTempC())
         time.sleep(sensorInterval)
         print readings
         counter += 1

      avg_temp = numpy.mean(readings)

		
      while True:
         curr_temp = tempSensor.readObjTempC() # Gets current temp reading

         # Prints current and average temperature readings
         print 'average temp: {0:0.3F}*C'.format(avg_temp) 
         print 'current temp: {0:0.3F}*C'.format(curr_temp) 

         # Converts temperatures to Fahrenheit
         #print 'average temp: {0:0.3F}*F'.format(c_to_f(avg_temp)) 
         #print 'current temp: {0:0.3F}*F'.format(c_to_f(avg_temp))

         # Compares current temp to avg.
         # If change exceeds specified detection threshold, 
         # Scene is illuminated, image is captured and emailed
         if abs(curr_temp - avg_temp) > detectionThresh:  
            
            RPi.GPIO.output(triggerPin1, RPi.GPIO.HIGH)   # LED's ON
            RPi.GPIO.output(triggerPin2, RPi.GPIO.HIGH)
         

            # Determines current time and adds it to image filename
            currTime = datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
            directory = 'images/'
            imageName = directory + filename + currTime + ext
      	
            # call raspistill to capture image
            os.system('/usr/bin/raspistill -v -o '+ imageName + ' -n')
            print 'Emailing image...'

            time.sleep(5)

            RPi.GPIO.output(triggerPin1, RPi.GPIO.LOW)    # LED's OFF 
            RPi.GPIO.output(triggerPin2, RPi.GPIO.LOW)

            email_image(imageName)             # email picture 

         readings.pop(0)                       # pops off first reading
         readings.append(curr_temp)            # appends current temp    
         avg_temp = numpy.mean(readings)       # takes new reading
         time.sleep(sensorInterval)


   except KeyboardInterrupt:
     print 'Exiting...'
     RPi.GPIO.cleanup()
     sys.exit(0)


if __name__ == '__main__':

   triggerPin1 = 4          # control pin for LED batch 1
   triggerPin2 = 17         # control pin for LED batch 1
   filename = 'image'       # image filename and extension
   ext = '.jpg'  
   toAddress = 'vms3476'    # address to receive email with image    

   sensorInterval = 1       # seconds between temp readings

   detectionThresh = 0.4    # C

   detection(triggerPin1, triggerPin2, filename, ext, toAddress, sensorInterval, detectionThresh)







