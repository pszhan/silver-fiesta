import cv2  # 导入OpenCV库，用于图像处理和计算机视觉任务
import window  # 导入自定义的窗口模块，可能包含图形用户界面相关的功能
import time  # 导入时间模块，用于计时和延迟操作
import numpy as np  # 导入NumPy库，用于数组和矩阵操作
from discrimination import *  # 导入自定义的识别模块，可能包含图像识别相关的功能
from zhijiao import *  # 导入自定义的支脚模块，可能包含机器人支脚控制相关的功能
from uart import Uart  # 导入自定义的串口通信模块，可能包含与外部设备通信的功能
from task import Task, Set_Task_id  # 导入自定义的任务模块，可能包含任务管理和调度相关的功能
from wifi_thread import Wifi_Thread  # 导入自定义的Wi-Fi线程模块，可能包含Wi-Fi连接和数据传输相关的功能
Timeout_t = 10  # 设置超时时间为10秒
CAM: cv2.VideoCapture  # 定义一个名为CAM的视频捕获对象，用于从摄像头或其他视频源捕获视频帧
def GetCamera()->cv2.VideoCapture:
    i:int=0  # 初始化摄像头索引
    res:cv2.VideoCapture=None  # 初始化摄像头对象
    start=time.time()  # 记录开始时间
    Timeout_t = 10  # 设置超时时间，单位为秒

    # 在超时时间内尝试获取摄像头
    while(time.time()-start<Timeout_t):
        try:
            res=cv2.VideoCapture(i%10)  # 尝试打开摄像头，使用索引 i%10 避免超出范围
            if(res.isOpened()):  # 如果摄像头成功打开
                print("get the capture[{}]".format(i%10))  # 打印成功信息
                b=False  # 初始化帧读取状态
                i=0  # 重置计数器
                while(i<5):  # 尝试读取5帧图像
                    b,frame=res.read()  # 读取一帧图像
                    #cv2.imshow("tmp",frame)  # 显示图像（注释掉的代码）
                    if(b==True):  # 如果读取成功
                        i+=1  # 计数器加1
                return res  # 返回摄像头对象
        except:
            print("can't find capture[{}]".format(i%10))  # 打印错误信息
        i+=1  # 索引递增
    print("get capture timeout")  # 超时后打印信息
    return None  # 返回空值

GET_IMG_BUF:cv2.Mat=np.zeros((720,480))  # 创建一个空的图像缓冲区，大小为720x480
def GetImg():
    global CAM  # 声明全局变量CAM，用于存储摄像头对象
    global GET_IMG_BUF  # 声明全局变量GET_IMG_BUF，用于存储获取到的图像帧
    frame: cv2.Mat = None  # 初始化frame为None，用于存储从摄像头读取到的图像帧
    b: bool = False  # 初始化布尔变量b为False，用于表示是否成功读取到图像帧

    if CAM is not None:  # 判断摄像头对象是否存在
        print("摄像头打开了")
        b, frame = CAM.read()  # 尝试从摄像头读取图像帧，并将结果存储在frame中
    else:
        print("摄像头未打开")

    if b:  # 如果成功读取到图像帧
        GET_IMG_BUF = frame  # 将读取到的图像帧存储到全局变量GET_IMG_BUF中
        return True, frame  # 返回True和图像帧
    else:
        print("重新加载摄像头中...")
        CAM = GetCamera()  # 调用GetCamera函数重新获取摄像头对象
        return False, GET_IMG_BUF  # 返回False和当前存储的图像帧（可能是上一次成功读取的）

# 创建一个UART对象
u = Uart()
# 启动UART通信
u.start()

# 创建一个Wifi线程对象
w = Wifi_Thread()
# 启动Wifi线程
w.start()

# 设置任务ID
Set_Task_id(u)

# 创建一个480x640的全白色图像矩阵，数据类型为uint8
mat_buf: cv2.Mat = np.zeros((480, 640, 3), dtype=np.uint8)
mat_buf[:] = (255, 255, 255)

# 获取摄像头对象
CAM = GetCamera()

#print("WIDTH",CAM.get(cv2.CAP_PROP_FRAME_WIDTH))
#print("HEIGHT",CAM.get(cv2.CAP_PROP_FRAME_HEIGHT))
#640x480

while(True):  # 无限循环，直到按下ESC键退出
    _, mat_buf = GetImg()  # 获取图像帧
    #DiscriminateColor(mat_buf)  # 对图像进行颜色识别（此行代码被注释掉了）
    t = time.time()  # 记录当前时间
    Task(mat_buf, u, w)  # 执行任务处理函数，传入图像帧、串口对象和Wi-Fi线程对象
    window.showCapture(mat_buf)  # 显示捕获到的图像帧
    #window.showStr("")  # 显示字符串（此行代码被注释掉了）
    c = cv2.waitKey(1)  # 等待键盘输入，参数为延迟时间（单位：毫秒）
    if c == 27:  # 如果按下ESC键（ASCII码为27）
        break  # 跳出循环
u.close()  # 关闭串口连接

