# Untitled - By: 黄惠泽 - 周四 5月 31 2018

import time, sensor, image

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # can be QVGA on M7...
sensor.skip_frames(30) # 修改sensor配置之后， 跳过30帧
sensor.set_auto_gain(False) # must turn this off to prevent image washout...
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr(1.8) # strength of 1.8 is good for the 2.8mm lens.
    for code in img.find_qrcodes():
        print(code.payload())
    print("FPS %f" % clock.fps())
