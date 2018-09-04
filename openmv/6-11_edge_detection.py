# Erode and Dilate Example
#
# This example shows off the erode and dilate functions which you can run on
# a binary image to remove noise. This example was originally a test but its
# useful for showing off how these functions work.

import pyb, sensor, image



sensor.reset()
sensor.set_framesize(sensor.QVGA)
sensor.set_pixformat(sensor.RGB565)

grayscale_thres = (170, 255)
rgb565_thres = (29, 76, -21, 78, 7, 66)
binary_thres = 255
while(True):

    img = sensor.snapshot()
    print("1234")


    blobs = img.find_blobs([rgb565_thres], area_threshold=150)

    if blobs:
        most_pixels = 0
        largest_blob = 0
        for i in range(len(blobs)):
            if blobs[i].pixels() > most_pixels:
                most_pixels = blobs[i].pixels()
                largest_blob = i
        img.draw_rectangle(blobs[largest_blob].rect(),color=(0,0,0))
        img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy())

        for i in range(20):
            img = sensor.snapshot()
            img.binary([rgb565_thres])
            img.erode(2)
        for i in range(20):
            img = sensor.snapshot()
            img.binary([rgb565_thres])
            img.dilate(2)



        for l in img.find_lines(roi=blobs[largest_blob].rect()):
            #filter the lines whose degrees are outside the range
            if l.theta()>45 and l.theta()<135:
                lines = img.find_lines()
                img.draw_line(l.line(), color = (255, 0, 255))
                #print(l)






