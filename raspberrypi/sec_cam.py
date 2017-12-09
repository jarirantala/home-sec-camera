
import RPi.GPIO as GPIO
import os
import time
import picamera
import file_repository as file

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

camera = picamera.PiCamera()
#camera.vflip = True

def MOTION(channel):
    if GPIO.input(PIR_PIN):
        #datetime = time.strftime('%Y-%m-%d-%H:%M:%S', time.time())
        filename = 'pic' + str(round(time.time()) * 1000)
        print("Motion Detected... saving two images " + filename)
        camera.capture(filename + '.jpg')
        time.sleep(0.5)
        camera.capture(filename + '_2.jpg')
        file.uploadFile(filename + '.jpg')
        file.uploadFile(filename + '_2.jpg')
        os.remove(filename + '.jpg')
        os.remove(filename + '_2.jpg')
    else:
        print ("Stop")


print ("PIR Module Test (CTRL+C to exit)")
time.sleep(4)
print ("Ready")

try:
    GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=MOTION)
    while 1:
        time.sleep(1)
except KeyboardInterrupt:
    print (" Quit")
    camera.close()
    GPIO.cleanup()
except picamera.PiCameraValueError as e:
    print('CameraError: ' + str(e))
    GPIO.cleanup()
    camera.close()
