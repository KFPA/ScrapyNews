# coding:utf-8
from multiprocessing import Queue

try:
    q = Queue()
    q.get(timeout=5)
except BaseException as e:
    print
    '--' + str(e)

