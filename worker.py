#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import random
import requests
import time

THREAD_NUM = 8
# ENDPOINT = '149.156.9.143:8888/image/v0/api/bbic?fname=/srv/data'
#ENDPOINT = 'dcache-dot12.desy.de:8888/image/v0/api/bbic?fname=/srv/data/HBP'
ENDPOINT = 'hbp-image.desy.de:8888/image/v0/api/bbic?fname=/srv/data/HBP/'

def do_request((stack, level, slice, x, y)):
	url = 'http://{endpoint}/BigBrain_jpeg.h5&mode=ims&prog=' \
	'TILE%200%20{stack}%20{level}%20{slice}%20{x}%20{y}%20none%2010%201'.format(
		endpoint = ENDPOINT,
		stack = stack,
		level = level,
		slice = slice,
		x = x,
		y = y
	)
#        url = 'http://{endpoint}/stacks/rat/Golgi/golgi_rat_sections.h5&mode=ims&prog=' \
#        'TILE%200%20{stack}%20{level}%20{slice}%20{x}%20{y}%20none%2010%201'.format(
#                endpoint = ENDPOINT,
#                stack = stack,
#                level = level,
#                slice = slice,
#                x = x,
#                y = y
#        )
        start = time.time()
	r = requests.get(url)
        end = time.time()
        diff = int((end - start) * 1000)
	# print('stack = {stack}, level = {level}, slice = {slice}, x = {x}, y = {y}, '\
	# 	'code = {code}'.format(
	# 		stack = stack,
	# 		level = level,
	# 		slice = slice,
	# 		x = x,
	# 		y = y,
	# 		code = r.status_code
	# 		)
	# 	)
	return r.status_code, diff, url

def random_params():
	level = random.randint(0, 2)
	if level == 0:
		return (0, 0, 3699, random.randint(0, 20), random.randint(0, 20))
	elif level == 1:
		return (0, 1, 3700, random.randint(0, 10), random.randint(0, 10))
	else:
		return (0, 2, 3694, random.randint(0, 5), random.randint(0, 5))

def main():
	pool = Pool(THREAD_NUM)
	params = map(lambda _: random_params(), xrange(THREAD_NUM))
	start = time.time()
	results = pool.map(do_request, params)
	end = time.time()
	diff = int((end - start) * 1000)
	#errors = len(results) - results.count(200)
	errors = len(results) - len(filter(lambda x: x[0] == 200, results))
	print('time: {0} ms, errors: {1} / {2}'.format(diff, errors, len(results)))
        #for r in results:
        #   print("diff: %d %s" % (r[1], r[2]))

if __name__ == '__main__':
	main()
