import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import Login_Widget,Paint_Widget, Message_Frame, Userlist_Widget
import socket
import threading

global conn
global catbus
global pix_pool
global mess_pool
global user_pool
global PIX_pt
global MESS_pt
global USER_pt
global pix_pt
global mess_pt
global user_pt
pix_pt = 0
PIX_pt = 0
mess_pt = 0
MESS_pt = 0
user_pt = 0
USER_pt = 0
pix_pool = []
mess_pool = []
user_pool = []

class Main_Window(QWidget):
	
	def __init__(self, catbus):
		super().__init__()
		global conn
		self.catbus = catbus
		self.W = 1200
		self.H = 700
		self.paint_widget = Paint_Widget.Paint_Widget(self, conn)
		self.message_frame = Message_Frame.Message_Frame(self)
		self.userlist_widget = Userlist_Widget.Userlist_Widget(self)
		self.chat_widget = QTextEdit(self)
		self.changeco_btn = QPushButton('选择颜色', self)
		self.send_btn = QPushButton('发送消息', self)
		self.send_btn.clicked.connect(self.send_mess)
		self.brush_label = QLabel('笔刷大小: 5', self)
		self.init_UI()
	
	def init_UI(self):
		self.setWindowTitle('Catbus')
		self.setGeometry(0, 0, self.W, self.H)
		self.paint_widget.setGeometry(10, 10, self.W - 350, self.H - 20)
		self.message_frame.setGeometry(870, 10, 320, 350)
		self.chat_widget.setGeometry(870, 370, 320, 100)
		self.changeco_btn.move(870, 480)
		self.send_btn.setStyleSheet("font-size: 15px")
		self.send_btn.move(970, 480)
		self.brush_label.setStyleSheet("font-size: 15px")
		self.brush_label.move(1070, 480)
		self.userlist_widget.setGeometry(870, 520, 320, 170)

		self.show()
	
	def resizeEvent(self, e) :
		biasx = self.width() - self.W
		biasy = self.height() - self.H
		self.paint_widget.setGeometry(
			self.paint_widget.pos().x(),
			self.paint_widget.pos().y(), 
			biasx + self.paint_widget.width(), 
			biasy + self.paint_widget.height()
		)
		self.W = self.width()
		self.H = self.height()
		
	def keyPressEvent(self, e):
		# pos change
		if e.key() == Qt.Key_A :
			self.paint_widget.key_left_pressing = True
		elif e.key() == Qt.Key_D :
			self.paint_widget.key_right_pressing = True
		elif e.key() == Qt.Key_W :
			self.paint_widget.key_up_pressing = True
		elif e.key() == Qt.Key_S :
			self.paint_widget.key_down_pressing = True
		# size change
		elif e.key() == Qt.Key_Minus :
			self.paint_widget.key_minus = True
		elif e.key() == Qt.Key_Equal :
			self.paint_widget.key_equal = True
		elif e.key() == Qt.Key_9 :
			self.paint_widget.key_9 = True
		elif e.key() == Qt.Key_0 :
			self.paint_widget.key_0 = True
		self.update()
		
	def keyReleaseEvent(self, e):
		if e.key() == Qt.Key_A :
			self.paint_widget.key_left_pressing = False
		elif e.key() == Qt.Key_D :
			self.paint_widget.key_right_pressing = False
		elif e.key() == Qt.Key_W :
			self.paint_widget.key_up_pressing = False
		elif e.key() == Qt.Key_S :
			self.paint_widget.key_down_pressing = False
		elif e.key() == Qt.Key_Minus :
			self.paint_widget.key_minus = False
		elif e.key() == Qt.Key_Equal :
			self.paint_widget.key_equal = False
		elif e.key() == Qt.Key_9 :
			self.paint_widget.key_9 = False
		elif e.key() == Qt.Key_0 :
			self.paint_widget.key_0 = False
		self.update()

	def add_pix(self, text):
		self.paint_widget.add_pix(text)
	def send_mess(self):
		text = 'MESS:' + self.catbus.user_name + '<-DIV->' + self.chat_widget.toPlainText() + '<-END->'
		global conn
		conn.sendall(bytes(text, encoding = 'utf-8'))

class Catbus():
	def __init__(self, ip, port):
		global conn
		conn = socket.socket()
		conn.connect((ip, port))
		self.login_init()
		self.window = None
		self.user_name = None
		self.timer = QTimer()
		self.timer.timeout.connect(self.flush)
		
	def login_init(self):
		self.login_widget = Login_Widget.Login_Widget(self, conn)

	def login_op(self):
		self.window = Main_Window(self)
		self.timer.start(20)
	def add_pix(self, text):
		self.window.add_pix(text)

	def flush(self):
		global pix_pool
		global mess_pool
		global user_pool
		global PIX_pt
		global MESS_pt
		global USER_pt
		global pix_pt
		global mess_pt
		global user_pt
		#print('flushing')
		while (pix_pt < PIX_pt) :
			self.add_pix(pix_pool[pix_pt])
			pix_pt += 1
		while (user_pt < USER_pt) :
			user_name = user_pool[user_pt]
			user_pt += 1
			if user_name[0] == '+' :
				self.window.userlist_widget.add_user(user_name[1:])
			if user_name[0] == '-' :
				self.window.userlist_widget.del_user(user_name[1:])
		while (mess_pt < MESS_pt) :
			user_name, text_ = mess_pool[mess_pt].split('<-DIV->')
			mess_pt += 1
			self.window.message_frame.add_message(text_, user_name == self.user_name)
			mess_pt += 1
		#print('flushed')

	def fuck(self):
		print('fuck')

def recv(conn) :
	#print('I am in recv')
	#print(conn)
	text = ''
	while True:
		ret_bytes = conn.recv(4096)
		text += str(ret_bytes, encoding = 'utf-8')
		if text[-7:] == '<-END->' :
			break
	return text

def sock() :
	global conn
	global catbus
	global pix_pool
	global mess_pool
	global user_pool
	global PIX_pt
	global MESS_pt
	global USER_pt
	while True :
		text = recv(conn)
		print(text)
		if text[:3] == 'PIX' :
			pix_pool.append(text)
			PIX_pt += 1
			#print('recv pix')
			#catbus.add_pix(text)
		elif text[:4] == 'MESS' :
			mess_pool.append(text[5:-7])
			MESS_pt += 1
			#user_name, text_ = text[5:-7].split('<-DIV->')
			#catbus.window.message_frame.add_message(text_, user_name == catbus.user_name)
			#catbus.fuck()
		elif text[:4] == 'USER' :
			user_name = text[5:-7]
			user_pool.append(user_name)
			USER_pt += 1
			#if user_name[0] == '+' :
				#user_pool.append
				#catbus.window.userlist_widget.add_user(user_name[1:])
			#if user_name[0] == '-' :
				#catbus.window.userlist_widget.del_user(user_name[1:])

if __name__ == '__main__' :	
	app = QApplication(sys.argv)
	catbus = Catbus('127.0.0.1', 5001)
	network = threading.Thread(target = sock)
	network.start()
	app.exec_()
	print('hello')
	conn.sendall(bytes('EXIT<-END->', encoding = 'utf-8'))
	conn.close()