# Untitled - By: 黄惠泽 - 周二 5月 22 2018

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False)

#不要忘记调节镜头畸变
clock = time.clock()
pixels1=[]
pixels2=[]

rgb_black = (0,0,0)

def calcAB(x,y):
    n = len(x)
    sumX,sumY,sumXY,sumXX =0,0,0,0
    for i in range(0,n):
        sumX  += x[i]
        sumY  += y[i]
        sumXX += x[i]*x[i]
        sumXY += x[i]*y[i]
    if (n*sumXX -sumX*sumX)!= 0:
        a = (n*sumXY -sumX*sumY)/(n*sumXX -sumX*sumX)
        b = (sumXX*sumY - sumX*sumXY)/(n*sumXX-sumX*sumX)
    else:
        a=0
        b=0
    return a,b,

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr()
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    current_y=0
    for x in range(0,320,20):

        for y in range(0,240):
            pixels1 = img.get_pixel(x,y)
            if pixels1[0]>200 and pixels1[1]<150 and pixels1[2]<150:
                list1.append(x)
                list2.append(y)
                img.draw_cross(x, y)
                break;

    for x2 in range(0,340,20):
        a=int(x2/20)
        if(a<len(list2)):
            index_y = list2[a]
            for y2 in range(index_y,240,1):
                pixels1 = img.get_pixel(x2,y2)
                if pixels1[0]<220 or pixels1[1]>120 or pixels1[2]>80:
                    list3.append(x2)
                    list4.append(y2)
                    img.draw_cross(x2, y2)
                    print("test")
                    break;

    print(list1)
    print(list2)
    print(list3)
    print(list4)

    a,b=calcAB(list1,list2)
    print("y = %10.5fx + %10.5f" %(a,b))

    c,d=calcAB(list3,list4)
    print("y = %10.5fx + %10.5f" %(c,d))

    line_tuple = (20, int(a*20+b), 300, int(a*300+b))
    img.draw_line(line_tuple, color=rgb_black)

    line_tuple = (20, int(c*20+d), 300, int(c*300+d))
    img.draw_line(line_tuple, color=rgb_black)
    print(clock.fps())
