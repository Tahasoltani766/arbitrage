import multiprocessing as mp
from functools import partial
from itertools import repeat


def worker(a):
    print(a)


def pool_handler():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = mp.Pool(mp.cpu_count() - 2)
    pool.map(worker, data)


if __name__ == '__main__':
    mp.freeze_support()
    print(mp.cpu_count())
    pool_handler()
