# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
from cgi import parse_qs
import urlparse
import hashlib
import re

perm = ''

class UrlRouter():

	def __init__(self):
		self.codes = dict()

	def is_valid_url(self,url):
		res = urlparse.urlparse(url)
		return res.scheme in ('http','https')

	def encode(self,url):
		key = hashlib.sha224(url).hexdigest()
		key = key[0:6]
		self.codes[key] = url
		return 'Enter please in your url : http://localhost:1234/?key='+key

	def decode(self,key):
		try:
			return self.codes[key]
		except (ValueError):
			return 'Error'

	def take_me_dict(self,env):
		return {
			'method' : env['REQUEST_METHOD'],
			'path' : env['PATH_INFO']
		}

	def dispatch(self,env):
		global perm
		req_dat = self.take_me_dict(env)
		query = env['QUERY_STRING']
		try:
			body_size = int(env.get('CONTENT_LENGTH',0))
		except (ValueError):
			body_size = 0

		if (req_dat['method'] == 'GET' and req_dat['path'] == '/'):
			if (query == ''):
				html = '<html><head><meta charset="utf-8"><title>Enter your url</title></head><body><form action="/post" method="POST"><input type="text" name="shortly" /><button type="submit">Send</button></form></body></html>'
				return {
						'content' : html,
						'code' : '200'
						}
			else :
				simple = re.findall(r'(\w+)=(\w+)',query)
				answer = self.decode(simple[0][1])
				if (answer != 'Error'):
					return {
					'content' : answer,
					'code' : '200'
					}
				else :
					return {
					'content' : 'Error',
					'code' : '200'
					}
		

		elif (req_dat['method'] == 'GET' and req_dat['path'] == '/post'):
			return {
					'content' : perm,
					'code' : '200'
					}


		elif (req_dat['method'] == 'POST'):
			request = env['wsgi.input'].read(body_size)
			data = parse_qs(request)
			if (self.is_valid_url(data['shortly'][0])):
				perm = self.encode(data['shortly'][0])
				return {
						'content' : perm,
						'code' : '301'
						}
			else :
				perm = 'Error'
				return {
					'content' : perm,
					'code' : '302'
					}

class Shortly():

	def __init__(self):
		self.router = UrlRouter()

	def __call__(self,env,start_response):	
		data = self.router.dispatch(env)
		if (data['code'] == '200'):
			start_response('200 OK',[('Content-type','text/html'),('Content-Length', str(len(data['content'])))])
		elif (data['code'] == '301'):
			start_response('301 Moved Permanently',[('Content-type','text/html'),('Location','/post'),('Content-Length', str(len(data['content'])))])
		elif (data['code'] == '302'):
			start_response('302 Moved Temporarily ',[('Content-type','text/html'),('Location','/'),('Content-Length', str(len(data['content'])))])
		return data['content']

if __name__ == "__main__":
	server = make_server('localhost',1234,Shortly())
	server.serve_forever()
