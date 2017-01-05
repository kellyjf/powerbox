#!/usr/bin/python
import time
import select
from PyQt4.QtCore import *

class GpioMonitor(QObject):

	def __init__(self, num=None):
		super(QObject,self).__init__()
		self.gpionum=num

	def work(self):
		if self.gpionum==None:
	
			cnt=1
			while True:
				self.emit(SIGNAL("status(QString)"), str(cnt))
				time.sleep(2)
				print cnt
				cnt=cnt+1
		else :
			gfd=open("/sys/class/gpio/gpio%d/value"%(self.gpionum),"r")
			p=select.poll()
			p.register(gfd, select.POLLPRI|select.POLLERR)
			while True:
				self.value=gfd.read()
				self.emit(SIGNAL("status(QString)"), self.value)
				res=p.poll()
				gfd.seek(0)	


if __name__ == "__main__":
	q=GpioMonitor()		
	q.work()

