# Untitled - By: 黄惠泽 - 周三 5月 23 2018

import sensor, image, time,math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

##function of finding median##
def find_median(lst):
    q2=0
    n=len(lst)
    lst=sorted(lst)
    if n%2==0:
        q2=(lst[int(n/2)]+lst[int(n/2-1)])/2
    if n%2==1:
        q2=lst[int((n-1)/2)]
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

    print("distance%",lst_dis)
    q1,q3=find_quartile(lst_dis)
    print("q1,q3", q1,q3)
    IQR=q3-q1
    mini=q1-0.8*IQR
    maxi=q3+0.8*IQR
    print("IQR,mini,maxi",IQR,mini,maxi)
    for i in range(len(lst_dis)):
        if lst_dis[i]<mini or lst_dis[i]>maxi:
            lst2.pop(i)
            lst1.pop(i)
    return lst1,lst2

def calcAB(x,y):
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


while(True):
    clock.tick()
    img = sensor.snapshot()
    lst1=[1,10,20,30,40,50,60]
    lst2=[1,10,20,30,70,50,120]

    lst5=find_quartile(lst2)
    print("quartile:",lst5)

    f,g=calcAB(lst1,lst2)
    lst3,lst4=remove_outliers(lst1,lst2,f,g)
    #for i in range(len(lst3)):
        #img.draw_cross(lst3[i], lst4[i])
    #print("y = %10.5fx + %10.5f" %(f,g))
    #line_tuple = (20, int(f*20+g), 300, int(f*300+g))
    #img.draw_line(line_tuple)
    print("lst3",lst3)
    print("lst4",lst4)
    #print("after modified")
    f,g=calcAB(lst3,lst4)
    #print("y = %10.5fx + %10.5f" %(f,g))


    line_tuple = (20, int(f*20+g), 300, int(f*300+g))
    #img.draw_line(line_tuple, color=(255,0,0))
    print(clock.fps())
