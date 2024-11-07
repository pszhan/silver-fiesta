import cv2  # 导入OpenCV库，用于图像处理
import numpy as np  # 导入NumPy库，用于数组和矩阵操作
import collections  # 导入collections库，提供额外的容器数据类型
import Usual  # 导入自定义模块Usual，可能包含一些常用的函数或类

x_buf = 0  # 初始化x轴缓冲变量
y_buf = 0  # 初始化y轴缓冲变量
def Get_Center(mat: cv2.Mat):
    # 定义边框的宽度和颜色  
    border_width = 100
    border_color = (255, 255, 255)  # 白色  

    # 获取图像的宽度和高度
    wide, heigth = mat.shape[:2]

    # 将图像转换为灰度图
    grayImg: cv2.Mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)

    # 对灰度图进行高斯模糊处理，以减少噪声
    grayImg = cv2.GaussianBlur(grayImg, (3, 3), 0)
    # 使用霍夫圆变换检测图像中的圆形
    circles = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1, 100, param1=150, param2=45, minRadius=200, maxRadius=400)
    resx = None
    resy = None
    # 如果检测到圆形
    if circles is not None:
        # 将检测到的圆形坐标四舍五入并转换为整数类型
        circles = np.round(circles[0, :]).astype("int")
        # 遍历检测到的圆形
        for (x, y, r) in circles:
            # 在原图上画出检测到的圆形
            cv2.circle(mat, (int(x), int(y)), r, (0, 255, 0), 3)
            # 计算圆心位置
            resx = int(x)
            resy = int(y + r * (2 / 3))
            # 在原图上画出圆心位置
            cv2.circle(mat, (resx, resy), 3, (255, 255, 0), 3)
            # 返回圆心位置的坐标
    return resx, resy


def GetRingColor(mat: cv2.Mat):
    wide = 2  # 定义一个宽度变量，用于确定ROI的范围
    rings = Discriminate_Ring(mat, 5, 100)  # 调用Discriminate_Ring函数，获取环的坐标列表
    for x, y in rings:  # 遍历环的坐标列表
        iy = int(y)  # 将y坐标转换为整数
        ix = int(x)  # 将x坐标转换为整数
        roi = mat[iy - wide:iy + wide, ix - wide:ix + wide]  # 获取以环为中心的ROI区域

        print(x, y, GetRoiColor(roi))  # 打印环的坐标和颜色信息

        cv2.circle(mat, (int(ix), int(iy)), 3, (0, 255, 0), 3)  # 在原图上画出绿色的圆点，表示环的位置
    if (len(rings) == 3):  # 如果检测到三个环
        cx, cy = Get_Center(rings)  # 计算环的中心坐标
        cv2.circle(mat, (int(cx), int(cy)), 3, (0, 0, 255), 3)  # 在原图上画出红色的圆点，表示环的中心位置
def ring_classify(examples:list, datas:list) -> list:
    # 初始化结果列表，每个元素都是一个空列表
    res = []
    for e in examples:
        res.append([])

    # 遍历数据点，计算每个数据点到示例点的最小距离，并将其归类到相应的示例点列表中
    for (x, y, r) in datas:
        temp = ()
        d_min = 65534
        for i in range(len(res)):
            dx = x - examples[i][0]
            dy = y - examples[i][1]
            distance = dx * dx + dy * dy
            if distance < d_min:
                d_min = distance
                temp = ((x, y, r), i)
        c = res[temp[1]]
        c.append(temp[0])

    return res

    
# 定义两个参数
PARAM1 = 150  # 第一个参数，值为150
PARAM2 = 100  # 第二个参数，值为100


def DiscriminateRing_Pro(mat:cv2.Mat,lastmat:cv2.Mat,r_min=10,r_max=70)->list:
    example=[]  # 存储第一次检测到的圆的信息
    datas=[]    # 存储第二次检测到的圆的信息
    res_list=[] # 存储最终筛选出的圆的中心坐标
    frames=[]   # 存储帧图像
    frames.append(lastmat)  # 将上一帧图像添加到帧列表中
    grayImg:cv2.Mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)  # 将输入图像转换为灰度图
    grayImg = cv2.GaussianBlur(grayImg, (5, 5), 0)  # 对灰度图进行高斯模糊处理
    # 使用霍夫圆变换检测圆，参数PARAM1和PARAM2需要根据实际情况调整
    circles_pre = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1, 100, param1=PARAM1, param2=PARAM2, minRadius=r_min, maxRadius=r_max)
    # 第一次检测
    if circles_pre is not None:
        circles_pre = np.round(circles_pre[0, :]).astype("int")  # 将检测到的圆的信息四舍五入并转换为整数类型
        # 得到第一次的粗略坐标
        for (x, y, r) in circles_pre:
            example.append((x,y,r))
        if(True):
            grayImg1:cv2.Mat = cv2.cvtColor(lastmat, cv2.COLOR_BGR2GRAY)  # 将上一帧图像转换为灰度图
            grayImg1 = cv2.GaussianBlur(grayImg1, (5, 5), 0)  # 对灰度图进行高斯模糊处理
            # 使用霍夫圆变换检测圆，参数PARAM1和PARAM2需要根据实际情况调整
            circles = cv2.HoughCircles(grayImg1, cv2.HOUGH_GRADIENT, 1, 3, param1=PARAM1, param2=PARAM2, minRadius=10, maxRadius=70)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")  # 将检测到的圆的信息四舍五入并转换为整数类型
                for(x,y,r) in circles:
                    datas.append((x,y,r))
                # 对两次检测到的圆进行分类
                circles_list=ring_classify(example,datas)
                for i in range(len(example)):
                    x_sum=0
                    y_sum=0
                    size=len(circles_list[i])
                    #print(size)
                    for x,y,r in circles_list[i]:
                        cv2.circle(mat, (x, y), r, (0, 0, 255), 1)  # 在原图上画出检测到的圆
                        x_sum+=x
                        y_sum+=y
                    x_avg=x_sum/size
                    y_avg=y_sum/size
                    res_list.append((x_avg,y_avg))  # 计算并存储筛选出的圆的中心坐标
                    cv2.circle(mat, (int(x_avg), int(y_avg)), 3, (0, 255, 0), 3)  # 在原图上画出筛选出的圆的中心点
    return res_list  # 返回筛选出的圆的中心坐标列表

#识别圆环    
def Discriminate_Ring(mat: cv2.Mat, r_min=10, r_max=70) -> list:
    # 将输入的彩色图像转换为灰度图像
    grayImg: cv2.Mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    # 对灰度图像进行高斯模糊处理，以减少噪声
    grayImg = cv2.GaussianBlur(grayImg, (5, 5), 0)
    # 初始化变量
    circle_size = 0
    pre_list = []
    circles_list = []
    res_list = []
    # 使用霍夫圆变换检测圆形，得到初步的圆心坐标和半径
    circles_pre = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1, 100, param1=PARAM1, param2=PARAM2, minRadius=r_min,
                                   maxRadius=r_max)
    # 第一次检测
    if circles_pre is not None:
        # 将检测到的圆的信息四舍五入并转换为整数类型
        circles_pre = np.round(circles_pre[0, :]).astype("int")
        circle_size = len(circles_pre)
        # 得到第一次的粗略坐标
        for (x, y, r) in circles_pre:
            pre_list.append((x, y, r))
            circles_list.append([])

        # 进行第二次精确检测
        circles = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1, 3, param1=PARAM1, param2=PARAM2, minRadius=10,
                                   maxRadius=70)

        if circles is not None:
            # 将检测到的圆的信息四舍五入并转换为整数类型
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:

                temp = ()
                d_min = 65534
                for i in range(circle_size):
                    dx = x - pre_list[i][0]
                    dy = y - pre_list[i][1]

                    distance = dx * dx + dy * dy
                    if (distance < d_min):
                        d_min = distance
                        temp = ((x, y, r), i)
                c: list = circles_list[temp[1]]
                c.append(temp[0])
                # print(d_min)
            # 滤波得到精细坐标
            for i in range(circle_size):
                x_sum = 0
                y_sum = 0
                size = len(circles_list[i])
                # print(size)

                for x, y, r in circles_list[i]:
                    cv2.circle(mat, (x, y), r, (0, 0, 255), 1)
                    x_sum += x
                    y_sum += y
                if (size != 0):
                    x_avg = x_sum / size
                    y_avg = y_sum / size
                    res_list.append((x_avg, y_avg))
                    cv2.circle(mat, (int(x_avg), int(y_avg)), 3, (0, 255, 0), 3)
    return res_list


def GetRoiColor(roi: cv2.Mat) -> str:
    # 对输入的图像进行高斯模糊处理，减少噪声影响
    roi = cv2.GaussianBlur(roi, (9, 9), 0)
    # 将图像从BGR颜色空间转换为Lab颜色空间
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2Lab)

    # 将图像分割成三个通道（L, a, b）
    channels = cv2.split(roi)
    # 计算每个通道的平均值
    averages = [np.mean(channel) for channel in channels]
    # 初始化颜色字符串为'N'（无色）
    color_str = 'N'
    # 根据a和b通道的平均值判断颜色
    if (abs(averages[1] - 128) < 10 and abs(averages[2] - 128) < 10):
        color_str = 'N'
    elif (averages[1] > 128 and averages[2] > 128):
        color_str = 'R'
    elif (averages[1] < 128 and averages[2] > 128):
        color_str = 'G'
    elif (averages[1] > 128 and averages[2] < 128):
        color_str = 'B'
    # 返回颜色字符串
    return color_str
def GetThreeColor(mat:cv2.Mat,dx=0,dy=-40,wide=220):
    rect_wide=30  # 定义矩形区域的宽度
    border_wide=wide  # 定义边界宽度
    height, width = mat.shape[:2]  # 获取图像的高度和宽度
    cx=int(width / 2 +dx)  # 计算中心点的x坐标
    cy=int(height / 2+dy)  # 计算中心点的y坐标
    lx=cx-border_wide  # 计算左侧边界的x坐标
    rx=cx+border_wide  # 计算右侧边界的x坐标

    # 提取三个区域的颜色信息
    x = cx
    y = cy
    roi2 = mat[y:y+rect_wide, x:x+rect_wide]

    x = lx
    y = cy
    roi1 = mat[y:y+rect_wide, x:x+rect_wide]

    x = rx
    y = cy
    roi3 = mat[y:y+rect_wide, x:x+rect_wide]
    color_str1=GetRoiColor(roi1)  # 获取第一个区域的颜色字符串
    color_str2=GetRoiColor(roi2)  # 获取第二个区域的颜色字符串
    color_str3=GetRoiColor(roi3)  # 获取第三个区域的颜色字符串

    # 在图像上绘制矩形框
    x = cx
    y = cy
    cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)
    x = rx
    y = cy
    cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)
    x = lx
    y = cy
    cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)

    print(color_str1+color_str2+color_str3)  # 打印颜色字符串
    res=Usual.GetReturnType(color_str1+color_str2+color_str3)  # 获取返回类型
    return res  # 返回结果


def GetThreeColor_Auto(mat: cv2.Mat):
    res = 'g'  # 初始化结果为'g'
    rings_temp = Discriminate_Ring(mat.copy(), 5, 50)  # 调用Discriminate_Ring函数，获取环的坐标列表
    if (len(rings_temp) == 3):  # 如果环的数量为3
        rings = rings_temp  # 将环的坐标列表赋值给rings
    rings = rings_temp  # 将环的坐标列表赋值给rings
    wide = 2  # 设置ROI的宽度
    for x, y in rings:  # 遍历环的坐标列表
        iy = int(y)  # 将y坐标转换为整数
        ix = int(x)  # 将x坐标转换为整数
        roi = mat[iy - wide:iy + wide, ix - wide:ix + wide]  # 获取ROI区域

        print(x, y, GetRoiColor(roi))  # 打印环的坐标和颜色信息

        cv2.circle(mat, (int(ix), int(iy)), 3, (0, 255, 0), 3)  # 在原图上画出圆点
    return res  # 返回结果
#识别中心颜色
def DiscriminateColor(mat: cv2.Mat):
    # 定义矩形区域的宽度
    rect_wide = 100
    # 获取图像的高度和宽度
    height, width = mat.shape[:2]
    # 计算矩形区域的左上角坐标
    x = int(width / 2 - 50)
    y = int(height / 2 - 50 - 100)
    # 提取矩形区域作为感兴趣区域（ROI）
    roi = mat[y:y + rect_wide, x:x + rect_wide]
    # 获取感兴趣区域的颜色字符串
    color_str = GetRoiColor(roi)

    # 如果颜色字符串不为"N"，则打印颜色字符串
    if (color_str != "N"):
        print(color_str)
    # 在原始图像上绘制矩形区域
    cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)
    # 返回颜色字符串
    return color_str
