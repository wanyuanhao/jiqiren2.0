import threading
# 多线程

class MyThread(threading.Thread):
    sum = 0
    # 锁
    lock = threading.Lock()

    def run(self):
        # 进来后加锁，执行完在释放
        with MyThread.lock:
            for i in range(1000000):
                MyThread.sum += 1


thread = MyThread()
thread1 = MyThread()
thread.start()
thread1.start()
thread.join()
thread1.join()

print(MyThread.sum)
