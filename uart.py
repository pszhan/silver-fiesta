import serial  # 导入串口通信库
import threading  # 导入线程库

Uart_interface = None  # 初始化串口接口变量为None，用于后续创建串口对象

class Uart:
    S4_Uart: serial.Serial  # 定义一个串口对象，用于与串口设备通信
    close_flag = True  # 定义一个关闭标志，用于控制线程的运行状态
    __thread = threading.Thread  # 定义一个线程对象，用于处理串口通信任务
    Task_id = 0x00  # 定义一个任务ID，用于标识不同的任务

    def __init__(self, task_id=0x00) -> None:
        global Uart_interface  # 声明全局变量Uart_interface
        # self.QR_Uart = serial.Serial("/dev/ttyACM0", 115200)  # 注释掉的代码，可能是用于连接另一个串口设备的
        try:
            self.S4_Uart = serial.Serial("/dev/ttyS4", 115200)  # 尝试连接名为"/dev/ttyS4"的串口设备，波特率为115200
        except:
            print("未检测到串口！")  # 如果连接失败，打印提示信息
            self.S4_Uart = None  # 将串口对象设置为None
        self.__thread = threading.Thread(name="UartThread", target=Uart_function, args=(self,))  # 创建一个名为"UartThread"的线程，目标函数为Uart_function，参数为当前对象
        # self.QR_buffer=''  # 注释掉的代码，可能是用于存储从串口读取的数据
        # self.__QR_code=''  # 注释掉的代码，可能是用于存储解析后的二维码数据
        Uart_interface = self  # 将当前对象赋值给全局变量Uart_interface
        self.Task_id = task_id  # 设置任务ID

    def start(self):
        # 启动线程
        self.__thread.start()
        # 设置关闭标志为True，表示允许线程运行
        self.close_flag = True

    def close(self):
        # 设置关闭标志为False，表示不允许线程继续运行
        self.close_flag = False

    def writeStr(self, s: str):
        # 将字符串编码为字节串后写入串口
        self.S4_Uart.write(s.encode())


def Uart_function(uart:Uart):
    global TASK_ID
    # 当uart的关闭标志为True时，执行循环
    while(uart.close_flag):
        # 从uart的S4_Uart中读取数据到buffer
        buffer=uart.S4_Uart.read()
        # 获取buffer中的最后一个元素作为任务ID
        uart.Task_id=buffer[-1]
        # 打印任务ID
        print(uart.Task_id)
        # 注释掉的代码表示向uart的S4_Uart写入"y"编码后的数据
        # uart.S4_Uart.write("y".encode())
        # 注释掉的代码表示更新uart的QR线程
        # uart.QR_thread_update()


