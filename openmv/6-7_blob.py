# Untitled - By: 黄惠泽 - 周四 6月 7 2018

import sensor, image, time

## Red Threshold
red_threshold =(49, 70, 41, 84, 0, 70)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([red_threshold], merge=True)
    if blobs:   #if target color is found
        for blob in blobs:
            x = blob[0]
            y = blob[1]
            width = blob[2]
            height = blob[3]
            center_x = blob[5]
            center_y = blob[6]
            # draw a rectangle around the blob
            img.draw_rectangle([x, y, width, height])
            # draw a cross in the center of rectangle
            img.draw_cross(center_x, center_y)
    print(clock.fps())
