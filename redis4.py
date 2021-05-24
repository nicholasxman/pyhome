# -*-coding:utf-8 -*-
# 继承Process类
from multiprocessing import Process
import time
import os
# print("------------继承Process类--------------")


class SubProcess(Process):
    # 由于Process类本身也有__init__初始犯法，这个子类相当是重写了父类这个方法
    def __init__(self, interval, name=""):
        Process.__init__(self)  # 调用父类初始化方法
        self.interval = interval
        if name:
            self.name = name

    # 重写了Process类的run()方法
    def run(self):
        print("子进程（%s） 开始执行，父进程为（%s）" % (os.getpid(), os.getppid()))
        t_start = time.time()
        time.sleep(self.interval)
        t_stop = time.time()
        print("子进程(%s)执行结束，耗时%0.2f秒" % (os.getpid(), t_stop - t_start))


if __name__ == "__main__":
    print("---------父进程开始执行--------")
    print("父进程PID:%s" % os.getpid())
    p1 = SubProcess(interval=1, name='mrsoft')
    p2 = SubProcess(interval=2)
    # 对一个不帮韩target属性的Process类执行start方法，就会运行这个类中的run方法
    # 故这里会执行p1.run()
    p1.start()
    p2.start()
    # 输出p1和p2的进程的执行状态，如果真正进行，返回True
    print("p1.is_alive=%s" % p1.is_alive())
    print("p2.is_alive=%s" % p2.is_alive())
    # 输出p1和p2进程的别名和PID
    print("p1.name=%s" % p1.name)
    print("p1.pid=%s" % p1.pid)
    print("p2.name=%s" % p2.name)
    print("p2.pid=%s" % p2.pid)
    print("----------等待子进程----------")
    p1.join()
    p2.join()
    print("-----------父进程结束----------")
