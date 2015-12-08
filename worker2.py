#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import random
import requests
import time

THREAD_NUM = 8
# ENDPOINT = '149.156.9.143:8888/image/v0/api/bbic?fname=/srv/data'
ENDPOINT = 'dcache-dot12.desy.de:8888/image/v0/api/bbic?fname=/srv/data/HBP'

def do_request((stack, level, slice, x, y)):
    url = 'http://{endpoint}/image/v0/api/bbic?fname=' \
    '/srv/data/BigBrain_jpeg.h5&mode=ims&prog=' \
    'TILE%200%20{stack}%20{level}%20{slice}%20{x}%20{y}%20none%2010%201'.format(
        endpoint = ENDPOINT,
        stack = stack,
        level = level,
        slice = slice,
        x = x,
        y = y
    )
    r = requests.get(url)
    # print('stack = {stack}, level = {level}, slice = {slice}, x = {x}, y = {y}, '\
    #   'code = {code}'.format(
    #       stack = stack,
    #       level = level,
    #       slice = slice,
    #       x = x,
    #       y = y,
    #       code = r.status_code
    #       )
    #   )
    return r.status_code

def random_params():
    level = random.randint(0, 2)
    if level == 0:
        return (0, 0, 3699, random.randint(0, 20), random.randint(0, 20))
    elif level == 1:
        return (0, 1, 3700, random.randint(0, 10), random.randint(0, 10))
    else:
        return (0, 2, 3694, random.randint(0, 5), random.randint(0, 5))

def main():
    params = map(lambda _: random_params(), xrange(THREAD_NUM))
    threads = []
    start = time.time()
    for param in params:
        thread = threading.Thread(target=do_request, args=(param,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    end = time.time()
    diff = int((end - start) * 1000)

    print('time: {0} ms'.format(diff))

if __name__ == '__main__':
    main()