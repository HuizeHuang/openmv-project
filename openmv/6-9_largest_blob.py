# Untitled - By: 黄惠泽 - 周四 6月 7 2018

import sensor, image, time

## Red Threshold
red_threshold_RGB =(51, 75, 19, 84, -7, 70)
## Global variables for finding the largest blob
most_pixels = 0
largest_blob = 0


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img.lens_corr(1.8) # for 2.8mm lens...
    blobs = img.find_blobs([red_threshold_RGB], merge=True)
    if blobs:
        ## Find largest blob
        for i in range(len(blobs)):
            if blobs[i].pixels() > most_pixels:
                most_pixels = blobs[i].pixels()
                largest_blob = i

        ## Draw a rectangle around the largest blob and mark the center
        img.draw_rectangle(blobs[largest_blob].rect(),color=(0,0,255))
        img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy())



    print(clock.fps())
