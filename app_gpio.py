import PyQt4.Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_gpio import *
from app_monitor import *

class GpioDialog(Ui_GpioDialog, QDialog):

	def __init__(self, parent=None):
		super(QDialog,self).__init__(parent)
		self.setupUi(self)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.wThread=[]
		self.wMonitor=[]
		self.labels=[self.num1Label,self.num2Label, self.num3Label]
		self.buttons=[self.num1Button,self.num2Button, self.num3Button]

		for num,gpio in enumerate([ 18, 23, 24]):
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

if __name__ == "__main__":
	import sys
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QtGui.QApplication(sys.argv)
	ui=GpioDialog()
	ui.show()
	sys.exit(app.exec_())

