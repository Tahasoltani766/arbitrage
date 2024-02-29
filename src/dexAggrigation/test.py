import random
import threading
import time
from multiprocessing import Process, Queue
def a(num, q: Queue):
    while 1:
        for item in range(num):
            time.sleep(random.randrange(1,3))
            q.put(item)


def th_worker(q: Queue):
    th = threading.Thread(target=worker, args=(q,), daemon=True)
    th.start()
    th.join()


class RespPostRust(threading.Thread):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def run(self):
        time.sleep(5)
        print(f'Finished {self.item}')


def worker(q: Queue):
    while True:
        item = q.get()
        print(f'Working on {item}')
        t = RespPostRust(item)
        t.start()


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=th_worker, args=(q,))
    p1.start()

    p = Process(target=a, args=(5, q))
    p.start()
    # p.join()
    # p1.join()
    # time.sleep(1)
#
