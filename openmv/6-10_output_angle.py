# Untitled - By: 黄惠泽 - 周四 6月 7 2018

import sensor, image, time, math

## Red Threshold in LAB color space for finding the largest blobs
red_threshold_LAB =(51, 75, 19, 84, -7, 70)
## Red Threshold in RGB color space for get_pixels() finding the right color
red_threshold_RGB= (200,256,0,160,0,180)
## Global variables for finding the largest blob
most_pixels = 0
largest_blob = 0
# Lists stores coordinates on x, y axis of two sets of points on each edge respectively
list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
## Threshold for black line
rgb_line = (0,0 ,0)

## Parameters for distance output
WINDOW_CENTER_X=160
WINDOW_CENTER_Y=120

distance_cam_to_line = 10 ## Camera is 10cm above from the tape
windows_length = 320
lens_angle = 64
K = windows_length/math.tan(lens_angle/2)


##################################################################################################################################
## Define a function given the coordinates (x, y) of sample points and returns a, b of best fitting regression line using least squares
##################################################################################################################################
def calcAB(x,y):

    if x is not None and y is not None :
        if len(x)<len(y):
            n = len(x)
        else:
            n = len(y)
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
    return a,b

############################
## Remove Outliers Module ##
############################

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

## Find quartiles ##
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

## Remove outliers ##
def remove_outliers(lst1,lst2,m,n):
    q1=0
    q3=0
    IQR=0
    mini=0
    maxi=0
    i=0
    lst_dis=[]
    for i in range(len(lst_dis)):
        lst_dis.append(abs(lst2[i]-(m*lst1[i]+n)))
    q1,q3=find_quartile(lst_dis)
    IQR=q3-q1
    mini=q1-0.1*IQR
    maxi=q3+0.1*IQR
    if len(lst_dis)!=0 and len(lst_dis)<len(lst2):
        while i<len(lst_dis):
            if lst_dis[i]<mini or lst_dis[i]>maxi:
                lst2.pop(i)
                lst1.pop(i)
                i -= 1
            i +=1
        return lst1,lst2
    else:
        return lst1,lst2

## Calculate distance ##
def distanceToCenter(a,b):
   winCx = WINDOW_CENTER_X
   winCy = WINDOW_CENTER_Y
   x = winCx
   y = a*winCx + b
   d = abs(y-winCy)
   L = distance_cam_to_line*(d/K)
   return L

######################################################################################
## Define a function combining find_largest_blob module and find_sets_of_points module
######################################################################################
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

        ## Find pixels from above edge of rectangle
        for x in range(0,320,20):
            a,b = calcAB(list1,list2)
            for y in range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h()):
                pixels1 = img.get_pixel(x,y)
                if pixels1[0]>red_threshold_RGB[0] and pixels1[0]<red_threshold_RGB[1] and pixels1[1]>red_threshold_RGB[2] and pixels1[1]<red_threshold_RGB[3] and pixels1[2]>red_threshold_RGB[4] and pixels1[2]<red_threshold_RGB[5]:
                    #if abs(y-(a*x+b))<20:
                    list1.append(x)
                    list2.append(y)
                    img.draw_cross(x, y)
                    break;



        ## Find pixels from below edge of rectangle
        lst=range(blobs[largest_blob].y(),blobs[largest_blob].y()+blobs[largest_blob].h())
        lst1=[i for i in reversed(lst)]

        for x in range(0,320,20):
            a,b = calcAB(list3,list4)
            for y in lst1:
                pixels1 = img.get_pixel(x,y)
                if pixels1[0]>red_threshold_RGB[0] and pixels1[0]<red_threshold_RGB[1] and pixels1[1]>red_threshold_RGB[2] and pixels1[1]<red_threshold_RGB[3] and pixels1[2]>red_threshold_RGB[4] and pixels1[2]<red_threshold_RGB[5]:
                    #if abs(y-(a*x+b))<20:
                    list3.append(x)
                    list4.append(y)
                    img.draw_cross(x, y)
                    break;
    return list1, list2, list3, list4, red_threshold_RGB


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img.lens_corr(1.8) # for 2.8mm lens...
    list1,list2,list3,list4,present_threshold=find_redLines()

    ## Calculate the slope and intercept a, b for the first line and print it in the serial terminal
    a,b=calcAB(list1,list2)

    ## Take two points on the line and draw it on the image
    line_tuple = (20, int(a*20+b), 300, int(a*300+b))
    img.draw_line(line_tuple, color=rgb_line)

    print("line1: y = %10.3fx + %10.3f" %(a,b))

    #print("y1_before:",list2)
    list1,list2=remove_outliers(list1,list2,a,b)
    a,b=calcAB(list1,list2)
    #print("line1_after: y = %10.3fx + %10.3f" %(a,b))
    #print("y1_after:",list2)

    ## Take two points on the line and draw it on the image
    line_tuple = (20, int(a*20+b), 300, int(a*300+b))
    img.draw_line(line_tuple, color=(0,0,255))

    ## Calculate the slope and intercept c, d for the second line and print it in the serial terminal
    c,d=calcAB(list3,list4)

    ## Take two points on the line and draw it on the image
    line_tuple = (20, int(c*20+d), 300, int(c*300+d))
    img.draw_line(line_tuple, color=rgb_line)

    print("line2: y = %10.3fx + %10.3f" %(c,d))
    #print("x1",list3)
    #print("y2_before:",list4)
    list3,list4=remove_outliers(list3,list4,c,d)
    c,d=calcAB(list3,list4)
    #print("line2_after: y = %10.3fx + %10.3f" %(c,d))
    #print("y2_after:",list4)

    ## Take two points on the line and draw it on the image
    line_tuple = (20, int(c*20+d), 300, int(c*300+d))
    img.draw_line(line_tuple, color=(0,0,255))

    ######################
    ## find center line ##
    ######################
    minimum=len(list2)
    if len(list2)>len(list4):
        minimum=len(list4)

    for i in range(minimum):
        list5.append(int((list2[i]+list4[i])/2))

    f,g=calcAB(list1,list5)
    print("center line: y = %10.5fx + %10.5f" %(f,g))

    line_tuple = (20, int(f*20+g), 300, int(f*300+g))
    img.draw_line(line_tuple, color=rgb_line)

    ###############################
    ## output angle and distance ##
    ###############################
    angle=0
    angle=math.atan(f)
    angle = math.degrees(angle)
    if angle>0:
        print('The car should turn right%10.3f degree'%angle)
    elif angle<0:
        print('The car should turn left%10.3f degree'%-angle)
    else:
        print("Do not turn")

    dis=0
    img.draw_cross(WINDOW_CENTER_X, WINDOW_CENTER_Y,color=(0,0,255))
    dis=distanceToCenter(f,g)
    print('The center of line is%10.3fcm away from camera center:'%dis)



    ## Clear the list ##
    list1.clear()
    list2.clear()
    list3.clear()
    list4.clear()
    list5.clear()
    print("fps:",clock.fps())
