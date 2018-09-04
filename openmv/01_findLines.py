# Untitled - By: 黄惠泽 - 周五 5月 18 2018

#lens length 0.4cm
#lens correction
enable_lens_corr = True # turn on for straighter lines...

import sensor, image, time, math


#distance settings
ROI = (0, 50, 160, 20)
red_THRESHOLD = (60, 70, 50, 80, -15, 70)
green_THRESHOLD = (36, 79, -73, -7, 25, 69)
WINDOW_CENTER_X = 80
WINDOW_CENTER_Y = 60
distance_cam_to_line = 10
width_of_pixel = 160
K = 2*math.tan(32)
Transform_pixel_to_centimeter = (K*distance_cam_to_line)/width_of_pixel # cam is 10cm away from the plain
red_color_code = 1 # code = 2^0 = 1
green_color_code = 2 # code = 2^1 = 2
dis=0
def distanceToCenter(blob):
    winCx = WINDOW_CENTER_X
    winCy = WINDOW_CENTER_Y
    x = blob.cx()
    y = blob.cy()
    return math.sqrt(math.pow(winCx - x, 2) + math.pow(winCy - y, 2))


sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()


while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    img.draw_cross(80,60,color=(255,0,0))
    blobs = img.find_blobs([red_THRESHOLD], roi=ROI)
    lines=[]
    if blobs:

        ################
        ##output angle##
        ################

        for l in img.find_lines(threshold = 1000, theta_margin = 50, rho_margin = 50):
            #filter the lines whose degrees are outside the range
            if l.theta()<50 or l.theta()>150:
                lines = img.find_lines(threshold = 1000, theta_margin = 50, rho_margin = 50)
                img.draw_line(l.line(), color = (255, 0, 0))
                #print(l)

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
        deflection_angle = math.degrees(deflection_angle)
        print(deflection_angle)

        ###################
        ##output distance##
        ###################

        # Find the index of the blob with the most pixels.
        most_pixels = 0
        largest_blob = 0
        for i in range(len(blobs)):

        #find the largest blob in the view
            if blobs[i].pixels() > most_pixels:
                most_pixels = blobs[i].pixels()
                largest_blob = i

        # Draw a rect around the blob.
        img.draw_rectangle(blobs[largest_blob].rect())
        img.draw_cross(blobs[largest_blob].cx(),
                       blobs[largest_blob].cy())
        dis = distanceToCenter(blobs[largest_blob]) * Transform_pixel_to_centimeter

        # Convert angle in radians to degrees.

        print(str(dis)+"cm"+"  "+str(deflection_angle)+"degrees")


    ################
    ## DataMatrix ##
    ################
    matrices = img.find_datamatrices()
    for matrix in matrices:
        img.draw_rectangle(matrix.rect(), color = (255, 0, 0))
        print_args = (matrix.rows(), matrix.columns(), matrix.payload(), (180 * matrix.rotation()) / math.pi, clock.fps())
        print("Matrix [%d:%d], Payload \"%s\", rotation %f (degrees), FPS %f" % print_args)
    if not matrices:
        print("FPS %f" % clock.fps())


