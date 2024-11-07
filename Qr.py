import serial  # 导入串口通信库
import time    # 导入时间库
import uart    # 导入自定义的uart模块
from uart import Uart  # 从uart模块中导入Uart类
import socket  # 导入套接字库，用于网络通信
from window import showStr  # 从window模块中导入showStr函数，用于显示字符串
from wifi_thread import Wifi_Thread  # 从wifi_thread模块中导入Wifi_Thread类，用于处理WiFi连接和数据传输

def __GetTaskColor(qrstr: str):
    # 将字符串的前三个字符转换为整数，作为第一个颜色元组的RGB值
    t1 = (int(qrstr[0]), int(qrstr[1]), int(qrstr[2]))
    # 将字符串的中间三个字符转换为整数，作为第二个颜色元组的RGB值
    t2 = (int(qrstr[4]), int(qrstr[5]), int(qrstr[6]))
    # 返回两个颜色元组
    return t1, t2

def Task_SaoMa(u: Uart, w: Wifi_Thread = None):
    # 如果Wifi线程不为空，则从Wifi线程获取消息
    if w is not None:
        message = Wifi(w)
    # 否则从UART串口扫描获取消息
    else:
        message = Scan(u)
    # 如果消息为空，则返回None, None
    if message is None:
        return None, None
    # 显示消息内容
    showStr(message)
    # 向UART串口发送确认信号
    u.S4_Uart.write("y".encode())
    # 获取任务的颜色信息
    t1, t2 = __GetTaskColor(message)
    # 返回颜色信息
    return t1, t2

def Wifi(w: Wifi_Thread) -> str:
    s = time.time()  # 记录当前时间
    while True:
        if (time.time() - s > 15):  # 判断是否已经过了15秒
            return "123+321"  # 如果超过15秒，返回固定字符串
        if w.message != "":  # 检查Wifi线程的消息是否为空
            return w.message[:7]  # 如果消息不为空，返回消息的前7个字符


def Scan(u: Uart) -> str:
    """
    扫描二维码并返回结果字符串。

    参数：
        u (Uart): Uart对象，用于检查任务ID。

    返回：
        str: 扫描到的二维码内容，如果超时或任务ID不匹配，则返回"123+321"。
    """
    try:
        # 初始化串口连接
        qr_uart = serial.Serial("/dev/ttyACM0", 115200)

        res = ""  # 初始化结果字符串
        s = time.time()  # 记录开始时间
        while True:
            temp = qr_uart.read().decode()  # 读取串口数据并解码
            if (time.time() - s > 15):  # 判断是否超时（15秒）
                raise Exception
            if (u.Task_id != 0x01):  # 检查任务ID是否匹配
                return None
            if (temp == '\r'):  # 遇到回车符结束扫描
                break
            res += temp  # 将读取到的数据添加到结果字符串中
    except:
        res = "123+321"  # 发生异常时返回预设字符串
    print(res)  # 打印结果字符串
    return res  # 返回结果字符串


