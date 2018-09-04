# Untitled - By: 黄惠泽 - 周五 5月 18 2018


enable_lens_corr = True # turn on for straighter lines...

import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    lines=[]
    for l in img.find_lines(threshold = 1000, theta_margin = 50, rho_margin = 50):

    #filter the lines whose degrees are outside the range
        if l.theta()<50 or l.theta()>130:
            lines = img.find_lines(threshold = 1000, theta_margin = 50, rho_margin = 50)
            img.draw_line(l.line(), color = (255, 0, 0))
            print(l)

    #find the average value of all the angles of lines in the image
    i=0
    angle_sum = 0
    deflection_angle = 0
    for i in range(len(lines)):
        if (lines[i].y2()-lines[i].y1())>110:
            angle_sum += math.atan((lines[i].x1()-lines[i].x2())/120)
        else:
            angle_sum += (1.57-math.atan((lines[i].y2()-lines[i].y1())/160))

    b=0.00001
    deflection_angle = angle_sum/(len(lines)+b) #avoid division by zero

    # Convert angle in radians to degrees.
    deflection_angle = math.degrees(deflection_angle)

    print(deflection_angle)

    print("FPS %f" % clock.fps())
