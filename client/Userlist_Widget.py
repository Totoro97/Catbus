from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import sys, time

class Userlist_Widget(QWebEngineView) :
	
	def __init__(self, father = None) :
		super().__init__(father)
		self.users = list()
		self.cnt = 0
		self.setGeometry(0, 0, 100, 200)
		if father == None :
			self.show()
		#self.add_user('nihao')
		
	def add_user(self, user_name) :
		if (user_name not in self.users) :
			self.users.append(user_name)
		self.flush()
	
	def del_user(self, user_name) :
		if (user_name in self.users) :
			self.users.remove(user_name)
		self.flush()
	
	def flush(self) :
		out_str = ''
		for _ in self.users :
			out_str += _ + '\n<br>\n'
		self.setHtml('<body style=\"font-family:Arial,Verdana,Sans-serif\">' + out_str + '</body>')
	
	#def mousePressEvent(self, e) :
	#	self.add_user('hahahha' + str(self.cnt))
	#	self.cnt += 1
	#	self.flush
	
if __name__ == '__main__' :
	app = QApplication(sys.argv)
	example = Userlist_Widget()
	sys.exit(app.exec_())
