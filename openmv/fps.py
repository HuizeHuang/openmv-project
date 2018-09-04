# Untitled - By: 黄惠泽 - 周四 5月 24 2018

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

red_threshold_01=(29, 76, -21, 78, 7, 66)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    list1=[]
    list2=[]
    list3=[]
    list4=[]

    blobs = img.find_blobs([red_threshold_01], area_threshold=150)

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
               if pixels1[0]>200 and pixels1[1]<150 and pixels1[2]<150:
                   list1.append(x)
                   list2.append(y)
                   img.draw_cross(x, y)
                   break;
       lst=range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h())
       lst1=[i for i in reversed(lst)]
       for x in range(0,320,20):

           for y in lst1:
               pixels1 = img.get_pixel(x,y)
               if pixels1[0]>200 and pixels1[1]<150 and pixels1[2]<150:
                   list1.append(x)
                   list2.append(y)
                   img.draw_cross(x, y)
                   break;

    print(clock.fps())
