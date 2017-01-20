import os
import PyQt4.Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_gpio import *
from app_monitor import *

import os

topdir="/sys/class/gpio"
topdir="/tmp/class/gpio"

class OutletButton(QPushButton):
        def __init__(self, number):
                super(QPushButton,self).__init__()
                self.number = number
                self.setCheckable(True)
                self.setText("Outlet %d"%(number))
                self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
                self.connect(self, SIGNAL("toggled(bool)"), self.toggled)
		self.toggled(False)

        def toggled(self, state):
		print self.number, state
                f = open("%s/gpio%d/value"%(topdir,496+self.number),"w")
                f.write("%d\n"%(0 if state else 1))
                f.close()
		self.setText("Outlet %d %s"%(self.number,"OFF" if state else "ON"))


	
class GpioDialog(Ui_GpioDialog, QDialog):

	def __init__(self, parent=None):
		super(QDialog,self).__init__(parent)
		self.setupUi(self)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.wThread=[]
		self.wMonitor=[]

		for i in range(8):
			gpiodir = "%s/gpio%d"%(topdir,496+i)
			if not os.path.isdir(gpiodir):
				f = open("%s/export"%(topdir),"w")
				f.write("%d\n"%(496+1))
				f.close()
				f = open("%s/direction"%(gpiodir),"w")
				f.write("out\n")
				f.close()
				f = open("%s/value"%(gpiodir),"w")
				f.write("1\n")
				f.close()

			button = OutletButton(i)
			self.powerGrid.addWidget(button,i%4,i/4)

			
		for num,gpio in enumerate([]):
			print "num %d gpio %d"%(num,gpio)
			self.wThread.append(QThread())
			self.wMonitor.append(GpioMonitor(gpio))

			self.wMonitor[num].moveToThread(self.wThread[num])
			self.wThread[num].start()

			self.connect(self.wMonitor[num], SIGNAL("status(QString)"),
				self.setLabel(num))
			self.connect(self.buttons[num], SIGNAL("clicked()"),
				self.wMonitor[num].work)


	def setLabel(self, num):
		print "setLabel %d: "%num, self
		def setNumLabel(gpio):
			print "setNumLabel %d: ",num, self
			print "gpio:           ",gpio
			self.labels[num].setText(QString(gpio))
		return setNumLabel

	def reject(self):
		os.system("/sbin/halt")

def main():
	import sys
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QtGui.QApplication(sys.argv)
	ui=GpioDialog()
	ui.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
