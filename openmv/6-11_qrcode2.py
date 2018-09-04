# Untitled - By: 黄惠泽 - 周二 5月 22 2018


import sensor, image, time, math, pyb, gc

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_windowing((320, 240))
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
sensor.set_saturation(2)
clock = time.clock()


pixels1=[]
rgb_black = (0,0,0)
red_threshold_LAB=(29, 76, -21, 78, 7, 66)#in LAB color space for finding blobs
green_threshold_LAB=(50,90,-80,-30,-10,30)

red_threshold_RGB= (200,256,0,150,0,150)  #in RGB color space for finding edges
green_threshold_RGB=(-1,60,200,256,120,256)
present_threshold=0

## Parameters for distance output
WINDOW_CENTER_X=160
WINDOW_CENTER_Y=120

distance_cam_to_line = 10 ## Camera is 10cm above from the tape
windows_length = 320
lens_angle = 64
K = windows_length/math.tan(lens_angle/2)

list1=[]
list2=[]
list3=[]
list4=[]
list5=[]

##function of finding median##
def find_median(lst):
    q2=0
    n=len(lst)
    lst=sorted(lst)
    if n!=0:
        if n%2==0:
            q2=(lst[int(n/2)]+lst[int(n/2-1)])/2
        if n%2==1:
            q2=lst[int((n-1)/2)]
        return q2
    else:
        return q2

def find_quartile(lst):
    lst1=[]
    lst2=[]
    q1=0
    q3=0
    n=len(lst)
    lst=sorted(lst)
    if n%2==0:
        lst1=lst[0:int(n/2)]
        lst2=lst[int(n/2):int(n)]
    else:
        lst1=lst[0:int((n-1)/2)]
        lst2=lst[int((n-1)/2+1):int(n)]
    q1=find_median(lst1)
    q3=find_median(lst2)
    return q1,q3

##remove outliers##
def remove_outliers(lst1,lst2,m,n):
    q1=0
    q3=0
    IQR=0
    mini=0
    maxi=0
    lst_dis=[]
    for i in range(len(lst2)):
        lst_dis.append(abs(lst2[i]-(m*lst1[i]+n)))
    q1,q3=find_quartile(lst_dis)
    IQR=q3-q1
    mini=q1-0.8*IQR
    maxi=q3+0.8*IQR
    if len(lst_dis)!=0 and len(lst_dis)<len(lst2):
        for i in range(len(lst_dis)):
            if lst_dis[i]<mini or lst_dis[i]>maxi:
                lst2.pop(i)
                lst1.pop(i)
        return lst1,lst2
    else:
        return lst1,lst2

def calcAB(x,y):
    if x is not None and y is not None:
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

## Calculate distance ##
def distanceToCenter(a,b):
   winCx = WINDOW_CENTER_X
   winCy = WINDOW_CENTER_Y
   x = winCx
   y = a*winCx + b
   d = abs(y-winCy)
   L = distance_cam_to_line*(d/K)
   if y-winCy <=0:
       return L
   else:
       return -L

def find_redLines():

    blobs = img.find_blobs([red_threshold_LAB], area_threshold=150)

    if blobs:
        most_pixels = 0
        largest_blob = 0
        for i in range(len(blobs)):
            if blobs[i].pixels() > most_pixels:
                most_pixels = blobs[i].pixels()
                largest_blob = i
        #img.draw_rectangle(blobs[largest_blob].rect(),color=(0,0,0))
        #img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy())


        for x in range(0,320,20):
            for y in range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h()):
                pixels1 = img.get_pixel(x,y)
                if pixels1[0]>red_threshold_RGB[0] and pixels1[0]<red_threshold_RGB[1] and pixels1[1]>red_threshold_RGB[2] and pixels1[1]<red_threshold_RGB[3] and pixels1[2]>red_threshold_RGB[4] and pixels1[2]<red_threshold_RGB[5]:
                    list1.append(x)
                    list2.append(y)
                    #img.draw_cross(x, y)
                    break;
        lst=range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h())
        lst1=[i for i in reversed(lst)]
        for x in range(0,320,20):
            for y in lst1:
                pixels1 = img.get_pixel(x,y)
                if pixels1[0]>red_threshold_RGB[0] and pixels1[0]<red_threshold_RGB[1] and pixels1[1]>red_threshold_RGB[2] and pixels1[1]<red_threshold_RGB[3] and pixels1[2]>red_threshold_RGB[4] and pixels1[2]<red_threshold_RGB[5]:
                    list3.append(x)
                    list4.append(y)
                    #img.draw_cross(x, y)
                    break;
    return list1, list2, list3, list4, red_threshold_RGB


def find_greenLines():

    blobs = img.find_blobs([green_threshold_LAB], area_threshold=150)

    if blobs:
        most_pixels = 0
        largest_blob = 0
        for i in range(len(blobs)):
            if blobs[i].pixels() > most_pixels:
                most_pixels = blobs[i].pixels()
                largest_blob = i
   #img.draw_rectangle(blobs[largest_blob].rect(),color=(0,0,0))
   #img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy())

        for x in range(0,320,20):
            for y in range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h()):
                pixels1 = img.get_pixel(x,y)
                if pixels1[0]>green_threshold_RGB[0] and pixels1[0]<green_threshold_RGB[1] and pixels1[1]>green_threshold_RGB[2] and pixels1[1]<green_threshold_RGB[3] and pixels1[2]>green_threshold_RGB[4] and pixels1[2]<green_threshold_RGB[5]:
                    list1.append(x)
                    list2.append(y)
                    #img.draw_cross(x, y)
                    break;
        lst=range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h())
        lst1=[i for i in reversed(lst)]
        for x in range(0,320,20):
            for y in lst1:
                pixels1 = img.get_pixel(x,y)
                if pixels1[0]>green_threshold_RGB[0] and pixels1[0]<green_threshold_RGB[1] and pixels1[1]>green_threshold_RGB[2] and pixels1[1]<green_threshold_RGB[3] and pixels1[2]>green_threshold_RGB[4] and pixels1[2]<green_threshold_RGB[5]:
                    list3.append(x)
                    list4.append(y)
                    #img.draw_cross(x, y)
                    break;
    return list1, list2, list3, list4, green_threshold_RGB

###########################
## Set initial color red ##
###########################
img = sensor.snapshot()
if find_redLines is not None:
    list1,list2,list3,list4,present_threshold = find_redLines()


while(True):

    clock.tick()
    img = sensor.snapshot()
    #img.lens_corr()

    ####################################
    ## Detect QRcode &Branch Decision ##
    ####################################

    for code in img.find_qrcodes():
        if code[4]== "change to green" and present_threshold==red_threshold_RGB:
            print("QR Code is detected, payload: change to green")
            img.draw_rectangle(code[0],code[1],code[2],code[3],color=(0,0,0))
            if find_greenLines is not None:
                list1,list2,list3,list4,present_threshold=find_greenLines()
        elif code[4]== "change to red" and present_threshold==green_threshold_RGB:
            print("QR Code is detected, payload: change to red")
            img.draw_rectangle(code[0],code[1],code[2],code[3],color=(0,0,0))
            if find_redLines is not None:
                list1,list2,list3,list4,present_threshold=find_redLines()

    #print(list1)
    #print("list2 before",list2)
    #print(list3)
    #print("list4 before",list4)

    #########################
    ## find two edge lines ##
    #########################
    if present_threshold==red_threshold_RGB:
        list1,list2,list3,list4,present_threshold=find_redLines()
    if present_threshold==green_threshold_RGB:
        list1,list2,list3,list4,present_threshold=find_greenLines()
    print("current threshold:",present_threshold)
    a,b=calcAB(list1,list2)
    list1,list2=remove_outliers(list1,list2,a,b)
    a,b=calcAB(list1,list2)
    #print("y = %10.5fx + %10.5f" %(a,b))
    #print("list2 after",list2)

    c,d=calcAB(list3,list4)
    list3,list4=remove_outliers(list3,list4,c,d)
    c,d=calcAB(list3,list4)
    #print("y = %10.5fx + %10.5f" %(c,d))
    #print("list4 after",list4)

    line_tuple = (20, int(a*20+b), 300, int(a*300+b))
    img.draw_line(line_tuple, color=rgb_black)

    line_tuple = (20, int(c*20+d), 300, int(c*300+d))
    img.draw_line(line_tuple, color=rgb_black)

    ######################
    ## find center line ##
    ######################
    minimum=len(list2)
    if len(list2)>len(list4):
        minimum=len(list4)

    for i in range(minimum):
        list5.append(int((list2[i]+list4[i])/2))

    f,g=calcAB(list1,list5)
    print("y = %10.5fx + %10.5f" %(f,g))

    line_tuple = (20, int(f*20+g), 300, int(f*300+g))
    img.draw_line(line_tuple, color=rgb_black)

    ###############################
    ## output angle and distance ##
    ###############################
    angle=0
    angle=math.atan(f)
    angle = math.degrees(angle)
    if angle>0:
        print('The car should turn left%10.3f degree'%angle)
    elif angle<0:
        print('The car should turn right%10.3f degree'%-angle)
    else:
        print("Do not turn")

    dis=0
    img.draw_cross(WINDOW_CENTER_X, WINDOW_CENTER_Y,color=(0,0,255))
    dis=distanceToCenter(f,g)
    if dis>=0:
        print('The center of line is%10.3fcm above from camera center:'%dis)
    else:
        print('The center of line is%10.3fcm below from camera center:'%-dis)

    ## Clear the list ##
    list1.clear()
    list2.clear()
    list3.clear()
    list4.clear()
    list5.clear()

    print(clock.fps())
