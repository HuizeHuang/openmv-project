# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, math

ROI = (0, 50, 160, 20)
red_THRESHOLD = (47, 62, 31, 78, 15, 70)
green_THRESHOLD = (36, 79, -73, -7, 25, 69)
WINDOW_CENTER_X = 80
WINDOW_CENTER_Y = 60
distance_cam_to_line = 10
width_of_pixel = 160
K = 2*math.tan(32)
Transform_pixel_to_centimeter = (K*distance_cam_to_line)/width_of_pixel # cam is 10cm away from the plain
red_color_code = 1 # code = 2^0 = 1
green_color_code = 2 # code = 2^1 = 2
def distanceToCenter(blob):
    winCx = WINDOW_CENTER_X
    winCy = WINDOW_CENTER_Y
    x = blob.cx()
    y = blob.cy()

    return math.sqrt(math.pow(winCx - x, 2) + math.pow(winCy - y, 2))


sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    dis=0
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    img.lens_corr(1.8) # for 2.8mm lens...
    img.draw_cross(80,60,color=(255,0,0))
    blobs = img.find_blobs([red_THRESHOLD], roi=ROI)
    if blobs:
               # Find the index of the blob with the most pixels.
               most_pixels = 0
               largest_blob = 0
               for i in range(len(blobs)):

               #目标区域找到的颜色块（线段块）可能不止一个，找到最大的一个，作为本区域内的目标直线
                   if blobs[i].pixels() > most_pixels:
                       most_pixels = blobs[i].pixels()
                       #merged_blobs[i][4]是这个颜色块的像素总数，如果此颜色块像素总数大于                     #most_pixels，则把本区域作为像素总数最大的颜色块。更新most_pixels和largest_blob
                       largest_blob = i

               # Draw a rect around the blob.
               img.draw_rectangle(blobs[largest_blob].rect())
               #将此区域的像素数最大的颜色块画矩形和十字形标记出来
               img.draw_cross(blobs[largest_blob].cx(),
                              blobs[largest_blob].cy())
               dis = distanceToCenter(blobs[largest_blob]) * Transform_pixel_to_centimeter

    lines = img.find_lines(threshold = 1000, theta_margin = 50, rho_margin = 50)
    for l in img.find_lines(threshold = 1000, theta_margin = 50, rho_margin = 50):
        img.draw_line(l.line(), color = (255, 0, 0))



   #find the average value of all the angles of lines in the image
    i=0
    angle_sum = 0
    deflection_angle = 0
    for i in range(len(lines)):
        angle_sum += math.atan((lines[i].x1()-lines[i].x2())/120)

    deflection_angle = angle_sum/(1.000000001+len(lines))

   # Convert angle in radians to degrees.
    deflection_angle = math.degrees(deflection_angle)
    print(str(dis)+"cm"+"  "+str(deflection_angle)+"degrees")
