# Blob Detection Example
#
# This example shows off how to use the find_blobs function to find color
# blobs in the image. This example in particular looks for dark green objects.

import sensor, image, time

# 如果要保证颜色追踪效果的话， 需要对环境的严格控制
# 晚上光源的冷暖色等，都会对颜色追踪造成很大的影响

# 彩色图片颜色的阈值格式组成， 是由LAB颜色空间的各自最小值与最大值组成
# 点击右侧的颜色空间下拉选择按钮， 默认为RGB Color Space
# 参考右侧的LAB Color Space里面的参数
# （minL, maxL, minA, maxA, minB, maxB）
# 灰度图的阈值格式
# (min, max)

# 红色阈值
red_threshold =(49, 70, 41, 84, 0, 70)
# 绿色阈值
green_threshold = (39, 93, -71, -28, -22, 67)

# 颜色阈值的设定可以在 工具(Tools) -> 机器视觉(Machine Vision) -> 阈值编辑器(Threshold Editor) 中调试

# 颜色代码是find_blobs返回的blob对象中的一个成分， 用于标识，该色块是由在哪个阈值下选择的
# 颜色1: 红色的颜色代码
red_color_code = 1 # code = 2^0 = 1
# 颜色2: 绿色的颜色代码
green_color_code = 2 # code = 2^1 = 2
# 颜色3的代码
# color_code_3 = 2^2 = 4
# 颜色4的代码
# color_code_4 = 2^3 = 8


sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 选择像素模式 RGB565.
sensor.set_framesize(sensor.QVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) #关闭白平衡。白平衡是默认开启的，在颜色识别中，需要关闭白平衡。

clock = time.clock() # Tracks FPS.

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # 拍照，返回图像
    # 在图像中寻找满足颜色阈值约束(color_threshold, 数组格式), 像素阈值pixel_threshold， 色块面积大小阈值(area_threshold)的色块
    blobs = img.find_blobs([red_threshold, green_threshold], area_threshold=100)
    if blobs:
    #如果找到了目标颜色
        for blob in blobs:
        #迭代找到的目标颜色区域
            x = blob[0]
            y = blob[1] #
            width = blob[2] # 色块矩形的宽度
            height = blob[3] # 色块矩形的高度

            center_x = blob[5] # 色块中心点x值
            center_y = blob[6] # 色块中心点y值

            color_code = blob[8] # 颜色代码

            # 添加颜色说明
            if color_code == red_color_code:
                img.draw_string(x, y - 10, "red", color = (0xFF, 0x00, 0x00))
            elif color_code == green_color_code:
                img.draw_string(x, y - 10, "green", color = (0x00, 0xFF, 0x00))

            #用矩形标记出目标颜色区域
            img.draw_rectangle([x, y, width, height])
            #在目标颜色区域的中心画十字形标记
            img.draw_cross(center_x, center_y)



    print(clock.fps())
    # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
