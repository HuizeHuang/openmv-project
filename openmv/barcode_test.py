import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # High Res!
sensor.set_windowing((320,240)) # V Res of 80 == less work (40 for 2X the speed).
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# Barcode detection can run at the full 640x480 resolution of your OpenMV Cam's
# OV7725 camera module. Barcode detection will also work in RGB565 mode but at
# a lower resolution. That said, barcode detection requires a higher resolution
# to work well so it should always be run at 640x480 in grayscale...



while(True):
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr()
    codes = img.find_barcodes()
    for code in codes:
        img.draw_rectangle(code.rect())
        print_args = (code.payload(), (180 * code.rotation()) / math.pi, code.quality(), clock.fps())
        print("Payload \"%s\", rotation %f (degrees), quality %d, FPS %f" % print_args)
    if not codes:
        print("FPS %f" % clock.fps())
