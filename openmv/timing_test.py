# Untitled - By: 黄惠泽 - 周六 6月 2 2018

from pyb import Timer
import sensor, image, time, math, pyb, gc
import micropython

micropython.alloc_emergency_exception_buf(100)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False)

img = sensor.snapshot()
code=img.find_qrcodes()

find_code = False # 初始化为没有数据读入

def is_code_finded():

    global find_code

    if img.find_qrcodes():
        find_code = True
    else:
        find_code = False


timer = Timer(4)
timer.init(freq=10)
timer.callback(is_code_finded())


while True:

    if find_code:
        print("finded")
    time.sleep(1000)
