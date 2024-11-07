import cv2
import numpy as np

# 设置窗口大小
WIN_SIZE = (int(720), int(480))

# 创建一个名为"Str"的窗口，设置为可调整大小
Str = cv2.namedWindow("Str", cv2.WINDOW_NORMAL)

# 调整窗口大小为指定的WIN_SIZE
cv2.resizeWindow("Str", WIN_SIZE[0], WIN_SIZE[1])

# 定义一个函数，用于显示捕获到的视频帧
def showCapture(mat: cv2.Mat):
    cv2.imshow("win", mat)

# 创建一个白色的空白图像，大小为WIN_SIZE，颜色为白色（255,255,255）
white_mat = np.zeros((WIN_SIZE[1], WIN_SIZE[0], 3), dtype=np.uint8)
white_mat[:] = (255, 255, 255)

# 定义一个函数，用于在白色背景上显示字符串信息
def showStr(message: str):
    global white_mat
    white_mat = np.zeros((WIN_SIZE[1], WIN_SIZE[0], 3), dtype=np.uint8)
    cv2.putText(
        white_mat,           # 图像
        message,             # 文字
        (0, 200),            # 文字左下角，(w_idx, h_idx)
        cv2.FONT_HERSHEY_SIMPLEX,   # 字体
        5,                    # 字体大小
        (0, 0, 255),          # 字体颜色
        8,                    # 线宽 单位是像素值
        cv2.LINE_AA           # 线的类型
    )
    cv2.imshow("Str", white_mat)

