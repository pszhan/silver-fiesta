import cv2
import numpy as np
import math
import time
def get_cross_point_linesegment(line1, line2):
    """
    求两条线段的交点， 兼容水平线和垂直线
    :param line1: ((x1,y1),(x2,y2))
    :param line2: ((x1,y1),(x2,y2))
    """
    # x = (b0*c1 – b1*c0)/D
    # y = (a1*c0 – a0*c1)/D
    # D = a0*b1 – a1*b0， (D为0时，表示两直线重合)

    line0_x1y1, line0_x2y2 = line1
    line1_x1y1, line1_x2y2 = line2
    line0_a = line0_x1y1[1] - line0_x2y2[1]
    line0_b = line0_x2y2[0] - line0_x1y1[0]
    line0_c = line0_x1y1[0] * line0_x2y2[1] - line0_x2y2[0] * line0_x1y1[1]
    line1_a = line1_x1y1[1] - line1_x2y2[1]
    line1_b = line1_x2y2[0] - line1_x1y1[0]
    line1_c = line1_x1y1[0] * line1_x2y2[1] - line1_x2y2[0] * line1_x1y1[1]

    d = line0_a * line1_b - line1_a * line0_b
    if d == 0:
        # 重合的边线没有交点
        return None,None
    x = (line0_b * line1_c - line1_b * line0_c) * 1.0 / d
    y = (line0_c * line1_a - line1_c * line0_a) * 1.0 / d
    return x, y


def fliter(gray:cv2.Mat, mode=1):
    # 对输入的灰度图像进行阈值处理，将像素值大于等于100的设置为255（白色），小于100的设置为0（黑色）
    if(mode==1):
        _, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        # 创建一个10x10的全1矩阵，用于腐蚀操作
        kernel = np.ones((10, 10), np.uint8)
        # 对灰度图像进行腐蚀操作，减小白色区域的大小
        gray = cv2.erode(gray, kernel)
        # 创建一个5x5的全1矩阵，用于膨胀操作
        kernel = np.ones((5, 5), np.uint8)
        # 对灰度图像进行膨胀操作，增大白色区域的大小
        gray = cv2.dilate(gray, kernel)
        gray = cv2.dilate(gray, kernel)
    # 对输入的灰度图像进行阈值处理，将像素值小于等于140的设置为255（白色），大于140的设置为0（黑色）
    if(mode==2):
        _, gray = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)
        # 创建一个20x20的全1矩阵，用于膨胀操作
        kernel = np.ones((20, 20), np.uint8)
        # 对灰度图像进行膨胀操作，增大白色区域的大小
        gray = cv2.dilate(gray, kernel)
    # 显示处理后的灰度图像
    cv2.imshow("gray", gray)
    # 返回处理后的灰度图像副本
    return gray.copy()


def findMaxlength(line_t_list: list):
    """
    该函数接收一个列表，其中每个元素是一个包含至少5个元素的子列表。
    函数的目的是找到具有最大第五个元素的子列表的索引。

    参数：
    line_t_list (list): 一个包含子列表的列表，每个子列表至少有5个元素。

    返回：
    int: 具有最大第五个元素的子列表的索引。
    """
    maxVal = 0  # 初始化最大值变量为0
    resIndex = 0  # 初始化结果索引变量为0
    i = 0  # 初始化循环变量i为0
    for i in range(len(line_t_list)):  # 遍历输入列表的所有元素
        if line_t_list[i][4] > maxVal:  # 如果当前子列表的第五个元素大于已知的最大值
            maxVal = line_t_list[i][4]  # 更新最大值
            resIndex = i  # 更新结果索引为当前子列表的索引
    return resIndex  # 返回具有最大第五个元素的子列表的索引


def FindCorner(img:cv2.Mat):

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    y=0
    x=0
    gray=img[y:y+400, x:x+440]
    gray=cv2.GaussianBlur(gray,(9,9),0 )
    b,g,r=cv2.split(gray)
    
    #二值化、膨胀腐蚀去噪
    #gray=fliter(gray,1)
    #_,gray=cv2.threshold(gray,180,255,cv2.THRESH_BINARY_INV)
    #_,gray=cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    #b=cv2.inRange(b,200,255)
    g=cv2.inRange(g,0,100)
    r=cv2.inRange(r,0,100)
    t=cv2.bitwise_and(r,g)
    #gray=cv2.bitwise_or(t,b)
    gray=t
    #cv2.imshow("gray",gray)
    kernel=np.ones((10,10),np.uint8)
    gray=cv2.erode(gray,kernel)
    kernel=np.ones((5,5),np.uint8)
    gray=cv2.dilate(gray,kernel)
    # gray=cv2.dilate(gray,kernel)
    #cv2.imshow("gray",gray)
    #边缘检测
    edge=cv2.Canny(gray,1,2,apertureSize=3)
    kernel=np.ones((3,3),np.uint8)
    edge=cv2.dilate(edge,kernel)
    #cv2.imshow("edge",edge)
    #霍夫变换检测直线
    try:
        lines=cv2.HoughLinesP(edge,1,np.pi/180,100,minLineLength=10,maxLineGap=10)
        if(len(lines)<2):#检测的线小于两条会被滤掉
            return None,None
    except:
        return None,None
    # 获取lines列表中第一个元素的坐标，并将其赋值给x1, y1, x2, y2
    x1, y1, x2, y2 = lines[0][0]
    # 计算线段的角度，并将其与坐标一起存储在line_a元组中
    line_a = (x1, y1, x2, y2, math.atan2(abs(x1 - x2), abs(y1 - y2)))
    # 初始化一个空的线段line_b
    line_b = (0, 0, 0, 0, 0)
    # 遍历lines列表中的每个元素
    for line in lines:
        # 获取当前元素的坐标，并将其赋值给x1, y1, x2, y2
        x1, y1, x2, y2 = line[0]
        # 计算当前线段的角度，并将其与坐标一起存储在line_t元组中
        line_t = (x1, y1, x2, y2, math.atan2(abs(x1 - x2), abs(y1 - y2)))
        # 在图像上绘制当前线段，颜色为绿色，线宽为5
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
        # 如果当前线段的角度与第一个线段的角度之差大于0.2，则将当前线段赋值给line_b并跳出循环
        if abs(line_t[4] - line_a[4]) > 0.2:
            line_b = line_t
            break

        #print(x1,y1,x2,y2,(x1-x2)*(x1-x2)+(y1-y2)*(y1-y2),math.atan2(abs(x1-x2),abs(y1-y2)))
    # if(abs(line_a[4]-line_b[4])>0.6):
    #     return None,None
    # 在图像上绘制两条线段，分别用绿色和黄色表示
    cv2.line(img, (line_a[0], line_a[1]), (line_a[2], line_a[3]), (0, 255, 0), 5)
    cv2.line(img, (line_b[0], line_b[1]), (line_b[2], line_b[3]), (0, 255, 255), 5)

    # 如果只检测到了一条线也会被滤掉
    if line_b == (0, 0, 0, 0, 0):
        return None, None

    # 计算两条线段的交点坐标
    cx, cy = get_cross_point_linesegment(((line_a[0], line_a[1]), (line_a[2], line_a[3])),
                                         ((line_b[0], line_b[1]), (line_b[2], line_b[3])))

    # 如果交点不存在，返回None
    if cx is None:
        return None, None

    # 在图像上绘制交点，用红色圆圈表示
    cv2.circle(img, (int(cx), int(cy)), 30, (0, 0, 255), 30)
    return cx,cy

# 读取图片文件'3.png'
img = cv2.imread('3.png')
# 将图片尺寸调整为640x480像素
img = cv2.resize(img, (640, 480))

# 调用FindCorner函数，获取图片中的角点坐标
cx, cy = FindCorner(img)
# 记录当前时间
s = time.time()
# 在图片上画一个红色的圆，圆心为角点坐标，半径为30像素
cv2.circle(img, (int(cx), int(cy)), 30, (0, 0, 255), 30)
# 打印处理速度（可选）
# print(1 / (time.time() - s))
# 显示处理后的图片
cv2.imshow("img", img)
# 等待用户按键，关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()


