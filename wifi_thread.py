import socket
import threading

class Wifi_Thread:
    port:int  # 端口号
    buffer:bytes  # 缓冲区
    message:str  # 消息
    udp_socket:socket.socket  # UDP套接字
    thread:threading.Thread  # 线程对象

    def __init__(self, port=4210) -> None:
        # 创建UDP套接字并绑定到指定端口
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port
        self.udp_socket.bind(("", port))
        # 创建线程对象，目标函数为wifi_thread_fun，参数为当前类的实例
        self.thread = threading.Thread(name="wifi-thread", target=wifi_thread_fun, args=(self,))
        self.buffer = None  # 初始化缓冲区为空
        self.message = ""  # 初始化消息为空字符串

    def start(self):
        # 启动线程
        self.thread.start()

def wifi_thread_fun(wt: Wifi_Thread):
    while True:
        try:
            # 接收数据并存储到缓冲区
            wt.buffer, _ = wt.udp_socket.recvfrom(1024)
            # 如果缓冲区不为空且消息为空且第四个字符为"+"，则将缓冲区内容解码为字符串并赋值给消息
            if wt.buffer != None and wt.message == "" and wt.buffer.decode()[3] == "+":
                wt.message = wt.buffer.decode()
                print("接收到WiFi任务码")
        except:
            pass  # 异常处理，继续循环

