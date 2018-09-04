#颜色识别内容
import sensor, image, time, math, pyb
from pyb import UART
from pyb import Servo

s1 = Servo(1) #P7 舵机1
s1.pulse_width(1900) #舵机1初始化到中间位置

#设置颜色识别阈值
green_threshold = (8, 20, -22, -9, -4, 19)#(22, 46, -49, -20, -33, 24)(11, 83, -43, -25, -2, 26)
white_threshold = (38, 47, -7, 7, -5, 5)
GRAYSCALE_THRESHOLD = [(13, 69)]


#发送的数据种类选择·
X_Size = 200
H_Size = 210

#找到最大的那块
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3]>max_size:
            max_blob = blob
            max_size = blob[2]*blob[3]
    return max_blob

#限幅函数
def XianFu(Data1,Data2):
    biggest = 1500
    if(Data1>biggest):
        Data1 = biggest
    if(Data1<-biggest):
        Data1 = -biggest
    if(Data2>biggest):
        Data2 = biggest
    if(Data2<-biggest):
        Data2 = -biggest
    return Data1,Data2

#数据类型转换
def Datatype_Change(data1,data2):
    a = data1
    b = data2
    x = int(a)
    y = int(b)
    return x , y

#数据打包
def UART_SEND_DATA(Send_Data1, Send_Data2):
    #对数据拆分处理
    k1 = Send_Data1//100
    k2 = Send_Data1%100
    k3 = Send_Data2//100
    k4 = Send_Data2%100
    #发送数据
    uart.writechar(200)                 #200：中心XY坐标
    uart.writechar(k1)			#输出数据的前两位
    uart.writechar(k2)			#输出数据的后两位
    uart.writechar(k3)			#输出数据的前两位
    uart.writechar(k4)			#输出数据的后两位
    uart.writechar(250)			#数据尾部

#近距离段串口格式发送
def UART_SEND_TURN_DATA(Send_Data1, Send_Data2):
    #对数据拆分处理
    k1 = Send_Data1//100
    k2 = Send_Data1%100
    k3 = Send_Data2//100
    k4 = Send_Data2%100
    #发送数据
    uart.writechar(210)                 #210：距离+角度
    uart.writechar(k1)			#输出数据的前两位
    uart.writechar(k2)			#输出数据的后两位
    uart.writechar(k3)			#输出数据的前两位
    uart.writechar(k4)			#输出数据的后两位
    uart.writechar(250)			#数据尾部

#找到最大的那块
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3]>max_size:
            max_blob = blob
            max_size = blob[2]*blob[3]
    return max_blob

#求n个x和的平均值
def Sum_Average(data,datalen):
    z = 0
    i = 0
    for i in range(datalen):
        z = z + data[i]
    z = z/len(data)
    return z

#求x与y的乘积
def X_Y_Multiple(data1,data2,datalen):
    i = 0
    z = 0
    for i in range(datalen):
        z = z + data1[i]*data2[i]
    return z

#求x的平方的和
def Square_Sum(data,datalen):
    i = 0
    z = 0
    for i in range(datalen):
        z = z + data[i]*data[i]
    return z

#设置摄像头相关参数
sensor.reset()
sensor.set_pixformat(sensor.RGB565)	#设置图片格式（彩色/灰度图）
sensor.set_framesize(sensor.QVGA)	#设置图像大小
sensor.skip_frames(10)			#等待设置生效
sensor.set_auto_whitebal(False)         #关闭白平衡
sensor.set_auto_gain(False)		#关闭自动亮度调节
sensor.set_contrast(0)          	#对比度 -3~3 7个调节
sensor.set_brightness(0)       		#亮度
sensor.set_saturation(0)                #饱和度

uart = UART(3,115200)                   #设置串口
led = pyb.LED(3)                        #提示灯
clock = time.clock()			#初始化时钟

#颜色识别区域的中心坐标
x_distance = y_distance = 0

#路径识别参数
ROIS = [ # [ROI, weight]
        #(0, 110, 160, 10),
        #(0, 100, 160, 10),
        (0, 090, 160, 10),
        (0, 080, 160, 10),
        (0, 070, 160, 10),
        (0, 060, 160, 10),
        (0, 050, 160, 10),
        (0, 040, 160, 10),
        (0, 030, 160, 10),
        (0, 020, 160, 10),
        #(0, 010, 160, 10),
        #(0, 000, 160, 10)
       ]

#标志量
flag_near = 0
flag_load = 0
count = 0

#路径识别的直线
K = 0
R = 0
x_sum_avg = 0
y_sum_avg = 0
x_sqrt_sum = 0
y_sqrt_sum = 0
x_mul_y = 0

line_x = [0]*8
line_y = [0]*8
j = 0

largest_blob = 0

while(True):
    clock.tick()			#开始跟踪运行时间
    #flag_near = uart.readchar()
    if(flag_near > 2):
        flag_load = 0                   #复位openmv
    print("flag_near",flag_near)
    #if(flag_near == 0 and flag_load == 0):
    if(1):
        flag_near = -1
        sensor.set_pixformat(sensor.RGB565)	#设置图片格式（彩色/灰度图）
        sensor.set_framesize(sensor.QVGA)	#设置图像大小
        img = sensor.snapshot()
        #对图片进行分析
        blobs = img.find_blobs([green_threshold])
        stop_blobs = img.find_blobs([white_threshold])
        if blobs:
            max_blob = find_max(blobs)
            x_error = max_blob[5]-img.width()/2
            y_error = max_blob[6]-img.height()/2

            img.draw_rectangle(max_blob.rect())
            img.draw_cross(max_blob.cx(), max_blob.cy())

            #对坐标进行低通滤波
            x_distance_new = x_error
            x_distance *= 0.8
            x_distance += x_distance_new*0.2

            y_distance_new = y_error
            y_distance *= 0.8
            y_distance += y_distance_new*0.2
        else:
            x_distance = y_distance =0

        print("x_distance,y_distance",x_distance,y_distance)
        Data = Datatype_Change(x_distance,y_distance)
        s1.pulse_width(1900)
        UART_SEND_DATA(Data[0],Data[1])
        #flag_near = uart.readchar()
        #print(flag_near)

    #elif(flag_near == 1 or flag_load == 1):
    elif(0):
        flag_load = 1         #锁定摄像头
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_framesize(sensor.QQVGA)
        img = sensor.snapshot()
        #利用颜色识别分别寻找三个矩形区域内的线段
        for r in ROIS:
            blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi=r[0:4], merge=True)
            blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi=r[0:4], merge=True)
            if blobs:
               #目标区域找到的颜色块最大的一个，作为本区域内的目标直线
                most_pixels = 0
                largest_blob = 0
                for i in range(len(blobs)):
                    if blobs[i].pixels() > most_pixels:
                        most_pixels = blobs[i].pixels()
                        largest_blob = i
                #img.draw_rectangle(blobs[largest_blob].rect())
                img.draw_cross(blobs[largest_blob].cx(),
                               blobs[largest_blob].cy())
                line_y[j] = blobs[largest_blob].cx()
                line_x[j] = -((blobs[largest_blob].cy()-59)/100)
                j = j+1
                if(j == 9):
                    j=0
        j = 0
        x_sum_avg = Sum_Average(line_x,8)
        y_sum_avg = Sum_Average(line_y,8)
        x_sqrt_sum = Square_Sum(line_x,8)
        x_mul_y = X_Y_Multiple(line_x,line_y,8)
        K = (x_mul_y - 8*x_sum_avg*y_sum_avg)/(x_sqrt_sum - (8*x_sum_avg*x_sum_avg+1))
        R = y_sum_avg + K*x_sum_avg - 80
        Data = Datatype_Change(K,R)
        UART_SEND_TURN_DATA(Data[0],Data[1])
        print("line_x",line_x,"line_y",line_y)
        print("K",K,"R",R)

        s1.pulse_width(2250)
        #time.sleep(100)

    else:
        s1.pulse_width(1500)
        UART_SEND_TURN_DATA(0,0)            #这里发送为了和主控的程序相应避免解锁发生
