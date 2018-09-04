# Untitled - By: 黄惠泽 - 周一 6月 11 2018

import sensor, image, time, math


THRESHOLD = ((29, 76, -21, 84, -7, 70)) ##For red lines
THRESHOLD_GREY = (0, 100)

## Parameters for distance output
WINDOW_CENTER_X=160
WINDOW_CENTER_Y=120

distance_cam_to_line = 10 ## Camera is 10cm above from the tape
windows_length = 320
lens_angle = 64
K = windows_length/math.tan(lens_angle/2)

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

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_saturation(2)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    #img.lens_corr()
    line = img.get_regression([THRESHOLD])

    if (line):
        img.draw_line(line.line(), color = (0,0,0))
        print("theta:",line.theta())
        print("rho:",line.rho())
        if line.theta() > 90:
            print("The car should turn right %f degree" %(line.theta()-90))
        elif line.theta() < 90:
            print("The car should turn left %f degree" %(90-line.theta()))
        else:
            print("stay this way")

        if (line.x1()-line.x2())!=0:
            k = ((line.y1()-line.y2())/(line.x1()-line.x2()))
            b = line.y1()-k*line.x1()


        dis=0
        img.draw_cross(WINDOW_CENTER_X, WINDOW_CENTER_Y,color=(0,0,255))
        dis=distanceToCenter(k,b)
        if dis>=0:
            print('The center of line is%10.3fcm above from camera center:'%dis)
        else:
            print('The center of line is%10.3fcm below from camera center:'%-dis)


    print("FPS:",clock.fps())
