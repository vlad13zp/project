# -*- coding: utf-8 -*-
from time import time

# Global decorator for local decorator
def global_decorator(function):
    def global_decorator_wrapper(func):
    	print '~~~~~~ Global decorator ~~~~~~'
        return function(func)
    return global_decorator_wrapper

# Local decorator
@global_decorator
def function_timer(func): 
    def timer_wrapper():
        start = time()
        result = func()
        print "Function %s took %.5f ms" % (func.__name__, (time()-start)*1000)
        print '~~~~~~ End function action ~~~~~~'
        return result
    return timer_wrapper

# Function for decorator
@function_timer
def squr():
	for i in xrange(10000):
		i * i

squr()