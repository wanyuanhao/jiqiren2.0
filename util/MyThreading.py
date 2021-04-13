# -*- encode = utf-8 -*-
import threading


class MyThreading(threading.Thread):
    lock = threading.Lock()
    def thread(self):
        pass
    