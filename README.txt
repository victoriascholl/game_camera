# game_camera
python code to control raspberry pi, cam, &amp; sensor(s). captures and emails image.

Steps to use prototype:
1. Plug in ethernet wire
2. Plug into power source
3. Either attach monitor (via HDMI cable) or ssh to pi from external computer
3. Enter login & password
4. cd to directory where detection.py is 
5. vi detection.py 
6. In test harness, edit the adjustable parameters:
    (Press "i" to enter insert mode)
    triggerPin1 (control pin for LED batch 1. Currently pin 4)
    triggerPin2 (control pin for LED batch 2. Currently pin 17)
    filename, ext (for image to be captured. Currently 'image.jpg')
    sensorInterval (seconds between temp readings. Set to 1 for testing; 
                    can be tuned for any environment)
    detectionThresh (change [in degrees Celsius) required for an image to be
                    captured and emailed. Set to 0.4 for testing)
7. Exit insert mode, close and save file (press ESC to exit insert mode, 
                                          then prSHIFT+ZZ, or :q to save and close)
8. Run the code by using the command: sudo python detection.py 
    Temperature readings will be gathered and averaged for the scene. 
    When the temperature exceeds the detection threshold, the IR LED's are turned on,
    an image is captured and emailed to the specified email address, and the IR LED's 
    are turned off. The system then continues gathering, averaging, and comparing 
    temperature readings 
9. Press CRTL+C at any time to exit program
# game_camera
