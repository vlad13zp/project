# -*- coding: utf-8 -*-
import time

class Timer(object):

	def __init__(self, func):
		self.func = func
		self.sum_time = 0

	def __call__(self, *args, **kwargs):
		start = time.clock()
		result = self.func(*args, **kwargs)
		elapsed = time.clock() - start
		self.sum_time += elapsed
		print ('%s : %.5f, %.5f' % (self.func.__name__, elapsed, self.sum_time))
		return result

@Timer
def squr():
	for i in xrange(10000):
		i * i
for i in xrange(10):
	squr()