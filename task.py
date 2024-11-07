import cv2
from uart import Uart
from Qr import Task_SaoMa
from discrimination import DiscriminateColor, Discriminate_Ring, Get_Center, GetThreeColor
from Usual import *
from zhijiao import *
from wifi_thread import Wifi_Thread
from zhuanpanConfirm import Task_ZhuanPanConfirm

# 定义任务编号
Task_Color_1 = (1, 2, 3)  # 第一次任务编号
Task_Color_2 = (2, 3, 1)  # 第二次任务编号
Task_Moment = Task_Color_2  # 当前任务编号

def Set_Task_id(u: Uart):
    """
    设置任务ID的函数。
    参数：
        u: Uart对象，用于与硬件通信。
    """
    u.Task_id = 0x00  # 将任务ID设置为0x00



def Task(mat:cv2.Mat,u:Uart,w:Wifi_Thread=None):
    global Task_Color_1,Task_Color_2,Task_Moment
    # 二维码获取任务码
    if(u.Task_id==0x01):
        temp1,temp2=Task_SaoMa(u)
        if(temp1!=None):
            Task_Color_1=temp1
            Task_Color_2=temp2
            u.Task_id=0x00
    # WiFi获取任务码
    if(u.Task_id==0x04):
        temp1,temp2=Task_SaoMa(u,w)
        if(temp1!=None):
            Task_Color_1=temp1
            Task_Color_2=temp2
            u.Task_id=0x00
    # 转盘抓取任务
    elif(u.Task_id//0x10==0x0A):
        check=Task_ZuanPanZhua(mat,u,Task_Color_1,Task_Color_2)
        print(Task_Color_1,Task_Color_2)
        Task_Moment=Task_Color_1
        if(check=='y'):
            u.Task_id=0x00
    # 转盘抓取任务B
    elif(u.Task_id//0x10==0x0B):
        check=Task_ZuanPanZhua_B(mat,u,Task_Color_1,Task_Color_2)
        if(check=='y'):
            u.Task_id=0x00
    # 发送颜色1的任务码
    elif(u.Task_id==0x02):
        res=IntToType(tNum=Task_Color_1)
        print(res)
        u.writeStr(res)
        u.Task_id=0x00
    # 发送颜色2的任务码
    elif(u.Task_id==0x03):
        res=IntToType(tNum=Task_Color_2)
        print(res)
        u.writeStr(res)
        u.Task_id=0x00
    # 获取环的中心位置
    elif(u.Task_id==0x11):
        Task_GetRingCenter(mat,u)
    # 获取转盘的中心位置
    elif(u.Task_id==0x10):
        Task_ZhuanPanCenter(mat,u)
    # 获取三种颜色的识别结果
    elif(u.Task_id==0x05):
        Task_ThreeColor(mat,u,Task_Color_1)
    elif(u.Task_id==0x06):
        Task_ThreeColor(mat,u,Task_Color_2)
    # 获取环的中心位置，限制距离为30
    elif(u.Task_id==0x07):
        Task_GetRingCenter(mat,u,30)
    # 寻找回库的角落
    elif(u.Task_id==0x12):
        Task_FindCorner(mat,u)
    # 转盘确认任务
    elif(u.Task_id==0x21):
        Task_ZhuanPanConfirm(mat,u)


def Task_ThreeColor(mat: cv2.Mat, u: Uart, task_color_1, istop=False):
    # 如果istop为False，获取三色图像的颜色信息
    if not istop:
        t = GetThreeColor(mat)
    # 如果istop为True，获取特定颜色范围内的三色图像颜色信息
    else:
        t = GetThreeColor(mat, 0, -50, 240)

    # 如果检测到的颜色不是绿色
    if t != 'g':
        # 根据任务颜色和检测到的颜色生成发送字符串
        send = Type_Task05(task_color_1, TypetoRGB[t])

        # 打印发送字符串
        print(send)
        # 通过串口发送数据
        u.writeStr(send)
        # 设置任务ID为0x00
        u.Task_id = 0x00
    else:
        # 如果检测到的颜色是绿色，不执行任何操作
        pass


def Task_FindCorner(mat:cv2.Mat, u:Uart):
    # 调用FindCorner函数，传入图像矩阵mat，返回角点的坐标(cx, cy)
    cx, cy = FindCorner(mat)
    # 如果找到了角点（即cx不为None）
    if cx is not None:
        # 将角点坐标转换为整数类型，并存储在列表send中
        send = [int(cx), int(cy)]
        # 打印角点坐标
        print(send)
        # 将角点坐标转换为字符串，并通过串口u发送出去
        u.writeStr(str(send))


def Task_GetRingCenter(mat: cv2.Mat, u: Uart, content_side=120, content_bottom=240):
    # 调用Discriminate_Ring函数，传入图像矩阵mat，返回检测到的环形区域列表rings
    rings = Discriminate_Ring(mat)

    # 如果检测到至少一个环形区域
    if len(rings) > 0:
        # 遍历所有检测到的环形区域
        for r in rings:
            # 判断环形区域的中心是否在指定范围内
            if abs(r[0] - 320) < content_side and r[0] - 240 < content_bottom:
                # 在图像上画出环形区域的中心点
                cv2.circle(mat, (int(r[0]), int(r[1])), 3, (255, 0, 0), 5)
                # 将环形区域的中心坐标转换为整数并存储在send列表中
                send = [int(r[0]), int(r[1])]
                # 打印send列表
                print(send)
                # 通过串口u发送send列表的内容
                u.writeStr(str(send))


def Task_ZhuanPanCenter(mat:cv2.Mat, u:Uart):
    # 获取图像的中心点坐标
    x, y = Get_Center(mat)
    # 如果中心点坐标不为空
    if x is not None:
        # 将中心点坐标存储到send列表中
        send = [x, y]
        # 打印send列表
        print(send)
        # 通过串口发送send列表的字符串形式
        u.writeStr(str(send))


def Task_ZuanPanZhua_B(mat: cv2.Mat, u: Uart, t1: tuple, t2: tuple):
    """
    根据给定的图像矩阵和串口对象，以及两个颜色阈值元组，判断是否需要执行任务。
    如果任务ID为0xB0或0xB7，则进行颜色识别并返回结果；否则，更新任务ID并调用Task_ZuanPanZhua函数。

    参数：
    mat (cv2.Mat): 输入的图像矩阵
    u (Uart): 串口对象
    t1 (tuple): 第一个颜色阈值元组
    t2 (tuple): 第二个颜色阈值元组

    返回：
    res (str): 'n'表示不需要执行任务，'y'表示需要执行任务
    """
    if (u.Task_id == 0xB0 or u.Task_id == 0xB7):
        res = 'n'
        t = t2
        if (u.Task_id == 0xB0):
            t = t1
        # elif(u.Task_id == 0xB7):
        #     t = t2
        colorType = DiscriminateColor(mat)
        if (colorType != RGBT[t[0] - 1]):
            res = 'y'
            u.writeStr(res)

        return res
    else:
        u.Task_id -= 0x10
        return Task_ZuanPanZhua(mat, u, t1, t2)
def Task_ZuanPanZhua(mat:cv2.Mat, u:Uart, t1:tuple, t2:tuple):
    # 初始化计数器n和颜色类型t
    n = 0
    t = t1
    # 获取任务ID
    Task_id = u.Task_id
    # 根据任务ID判断颜色类型t的值
    if Task_id > 0xA3:
        n = Task_id - 0xA0 - 3
        t = t2
    else:
        n = Task_id - 0xA0
        t = t1
    # 识别图像中的颜色类型
    colorType = DiscriminateColor(mat)
    print(colorType)
    # 初始化结果变量res为'n'
    res = 'n'
    # 如果识别到的颜色类型不为'N'，则进行判断
    if colorType != 'N':
        # 如果识别到的颜色类型与目标颜色类型一致，则将结果设为'y'
        if RGBDIR[colorType] == t[n-1]:
            res = 'y'
    # 如果结果为'y'，则通过串口发送结果
    if res == 'y':
        u.writeStr(res)
    # 返回结果
    return res


