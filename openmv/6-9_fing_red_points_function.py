# Untitled - By: 黄惠泽 - 周四 6月 7 2018

import sensor, image, time

## Red Threshold
red_threshold_LAB =(51, 75, 19, 84, -7, 70)
## Global variables for finding the largest blob
most_pixels = 0
largest_blob = 0

red_threshold_RGB= (200,256,0,150,0,150)

list1=[]
list2=[]
list3=[]
list4=[]

def find_redLines():

    blobs = img.find_blobs([red_threshold_LAB], area_threshold=150)

    if blobs:
        most_pixels = 0
        largest_blob = 0
        for i in range(len(blobs)):
            if blobs[i].pixels() > most_pixels:
                most_pixels = blobs[i].pixels()
                largest_blob = i
        img.draw_rectangle(blobs[largest_blob].rect(),color=(0,0,0))
        img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy())


        for x in range(0,320,20):
            for y in range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h()):
                pixels1 = img.get_pixel(x,y)
                if pixels1[0]>red_threshold_RGB[0] and pixels1[0]<red_threshold_RGB[1] and pixels1[1]>red_threshold_RGB[2] and pixels1[1]<red_threshold_RGB[3] and pixels1[2]>red_threshold_RGB[4] and pixels1[2]<red_threshold_RGB[5]:
                    list1.append(x)
                    list2.append(y)
                    img.draw_cross(x, y)
                    break;
        lst=range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h())
        lst1=[i for i in reversed(lst)]
        for x in range(0,320,20):
            for y in lst1:
                pixels1 = img.get_pixel(x,y)
                if pixels1[0]>red_threshold_RGB[0] and pixels1[0]<red_threshold_RGB[1] and pixels1[1]>red_threshold_RGB[2] and pixels1[1]<red_threshold_RGB[3] and pixels1[2]>red_threshold_RGB[4] and pixels1[2]<red_threshold_RGB[5]:
                    list3.append(x)
                    list4.append(y)
                    img.draw_cross(x, y)
                    break;
    return list1, list2, list3, list4, red_threshold_RGB


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_saturation(2)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img.lens_corr(1.8) # for 2.8mm lens...
    list1,list2,list3,list4,present_threshold=find_redLines()
    ## Clear the list ##
    list1.clear()
    list2.clear()
    list3.clear()
    list4.clear()

    print(clock.fps())
