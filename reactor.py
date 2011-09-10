#coding:utf8
'''
author:shafreeck
date:20110910
license:nothing,you can use it for free
'''
import asyncore,socket

class Reactor(asyncore.dispatcher_with_send):
	def __init__(self,sock=None):
		asyncore.dispatcher_with_send.__init__(self,sock)
		if not sock:
			self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
			self.set_reuse_addr()
		self.__rcallback = None
		self.__wcallback = None
		self.__handlers = []

	def listenon(self,host,port):
		self.bind((host,port))
		self.listen(5)

	def connect(self,host,port):
		asyncore.dispatcher_with_send.connect(self,(host,port))
	def handle_accept(self):
		pair = self.accept()
		if pair is None:
			pass #FIXME: handle this ,raise exception	
		else:
			sock,addr = pair
			handler = Reactor(sock)
			handler.register_read_event(self.__rcallback)
			handler.register_write_event(self.__wcallback)
			self.__handlers.append(handler)

	def register_read_event(self,rcallback):
		self.__rcallback = rcallback
	def register_write_event(self,wcallback):
		self.__wcallback = wcallback

	def read(self,num):
		return self.recv(num)
	def write(self,data):
		return self.send(data)

	def handle_read(self):
		if self.__rcallback:
			self.__rcallback(self)
	def handle_write(self):
		if self.__wcallback:
			self.__wcallback()
	def addreply(self,msg):
		self.send(msg)


def eventloop(timeout=30):
	asyncore.loop(timeout)
'''
callback function format:
def readcallback(IOdispatcher)
def writecallback(IOdispatcher)
'''
