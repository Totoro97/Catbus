from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

class Login_Widget(QWidget):
	
	def __init__(self, catbus = None, conn = None):
		super().__init__()
		self.catbus = catbus
		self.conn = conn
		self.init_UI()
		
	def init_UI(self):
	
		self.setWindowTitle('Catbus 2017')
		self.setGeometry(500, 500, 300, 200)
		
		self.login_line = QLineEdit(self)
		self.login_line.setPlaceholderText('请随便取个用户名')
		self.login_line.setGeometry(30, 30, 200, 30)
		
		self.login_btn = QPushButton('登录', self)
		self.login_btn.clicked.connect(self.login_op)
		
		self.show()
	
	def login_op(self):
		self.conn.sendall(bytes(self.login_line.text() + '<-END->', encoding = 'utf-8'))
		self.close()
		self.catbus.user_name = self.login_line.text()
		self.catbus.login_op()
		

if __name__ == '__main__' :
	app = QApplication(sys.argv)
	example = Login_Widget()
	sys.exit(app.exec_())
