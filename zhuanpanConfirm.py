import cv2  # 导入OpenCV库，用于图像处理
import numpy as np  # 导入NumPy库，用于数组和矩阵操作
from discrimination import Discriminate_Ring  # 导入自定义模块中的Discriminate_Ring函数
from uart import Uart  # 导入自定义模块中的Uart类

TOP_BORDER = 0  # 设置顶部边界值
BOTTOM_BORDER = 100  # 设置底部边界值
RING_BUFFER = np.zeros((640, 480 - TOP_BORDER), np.uint32)  # 初始化环形缓冲区
RING_CHECK = np.zeros((64, 48 - TOP_BORDER // 10), np.uint32)  # 初始化环形检查区域

def clearBuffer():
    """清空环形缓冲区和环形检查区域"""
    global RING_BUFFER, RING_CHECK, TOP_BORDER
    RING_BUFFER = np.zeros((640, 480 - TOP_BORDER), np.uint32)
    RING_CHECK = np.zeros((64, 48 - TOP_BORDER // 10), np.uint32)

def ZhuanPanConfirm(mat: cv2.Mat):
    """检测环形并返回其坐标"""
    global TOP_BORDER, RING_BUFFER, RING_CHECK
    rings_temp = Discriminate_Ring(mat, 30, 60)  # 调用Discriminate_Ring函数检测环形
    rings = []
    for ring in rings_temp:
        if (ring[1] > TOP_BORDER and ring[0] > 0 and ring[0] < 640 and ring[1] > 0 and ring[1] < 480):
            rings.append(ring)
    if len(rings) == 1:
        ring = rings[0]
        print(ring)
        RING_CHECK[int(ring[0] / 10)][int(ring[1] / 10)] += 1
        RING_BUFFER[int(ring[0])][int(ring[1])] += 1
        if RING_CHECK[int(ring[0] / 10)][int(ring[1] / 10)] > 10:
            t = np.where(RING_BUFFER == np.max(RING_BUFFER))
            x, y = 0, 0
            if len(t[0]) == 1:
                x, y = t[0], t[1]
            else:
                x, y = t[0][0], t[1][0]
            return x, y
    return None, None

def Task_ZhuanPanConfirm(mat: cv2.Mat, u: Uart):
    """执行环形确认任务"""
    x, y = ZhuanPanConfirm(mat)
    if x is not None:
        clearBuffer()
        cv2.circle(mat, (int(x), int(y)), 5, (0, 255, 255), 7)
        print(x, y)
        for i in range(10):
            u.writeStr(str([int(x), int(y)]))
        u.Task_id = 0x00
