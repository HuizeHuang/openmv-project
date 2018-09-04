
import sensor

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.set_windowing(30,30)         #Sets the resolution of the camera to a
                                    #sub resolution inside of the current resolution.
sensor.set_contrast(0)              #Set the camera image contrast. -3 to +3.
sensor.set_brightness(0)            #Set the camera image brightness. -3 to +3.
sensor.set_saturation(0)            #Set the camera image saturation. -3 to +3.
sensor.set_auto_gain(False)         #You need to turn off white balance too if you want to
                                    #track colors.
sensor.set_auto_whitebal(False)     #You need to turn off white balance too if you want to
                                    #track colors.
sensor.set_lens_correction(True)    #radi integer radius of pixels to correct (int).
                                    #coef power of correction (int).
while(True):
    img = sensor.snapshot()         # Take a picture and return the image.

