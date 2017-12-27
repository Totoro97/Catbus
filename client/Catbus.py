import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import Login_Widget,Paint_Widget, Message_Frame, Userlist_Widget
import socket
import threading

global conn
global catbus
global pix_pool, mess_pool, user_pool
global PIX_pt, MESS_pt, USER_pt
global pix_pt, mess_pt, user_pt
global pix_lock, mess_lock, user_lock
pix_lock = threading.Lock()
mess_lock = threading.Lock()
user_lock = threading.Lock()

pix_pt = 0
PIX_pt = 0
mess_pt = 0
MESS_pt = 0
user_pt = 0
USER_pt = 0
pix_pool = []
mess_pool = []
user_pool = []


class Main_Window(QMainWindow):
	
	def __init__(self, catbus):
		super().__init__()
		global conn
		self.catbus = catbus
		self.W = 1200
		self.H = 700
		#self.paint_area = QScrollArea(self)
		self.paint_widget = Paint_Widget.Paint_Widget(self, conn)
		#self.paint_area.setWidget(self.paint_widget)
		self.message_frame = Message_Frame.Message_Frame(self)
		self.userlist_widget = Userlist_Widget.Userlist_Widget(self)
		self.chat_widget = QTextEdit(self)
		self.changeco_btn = QPushButton('选择颜色', self)
		self.changeco_btn.clicked.connect(self.changeco)
		self.send_btn = QPushButton('发送消息', self)
		self.send_btn.clicked.connect(self.send_mess)
		#self.brush_label = QLabel('笔刷大小: ', self)
		self.brush_slider = QSlider(Qt.Horizontal, self)
		self.brush_slider.setMinimum(1)
		self.brush_slider.setMaximum(20)
		self.brush_slider.setValue(5)
		self.brush_slider.valueChanged.connect(self.changewidth)
		self.init_UI()
	
	def init_UI(self):
		self.setStyleSheet("QMainWindow {background: #4a4a4a;}")
		self.setWindowTitle('Catbus')
		self.setGeometry(0, 0, self.W, self.H)
		#self.paint_area.setGeometry(10, 10, self.W - 350, self.H - 20)
		self.paint_widget.setGeometry(10, 10, self.W - 350, self.H - 20)
		self.paint_widget.setStyleSheet('background: #000000')
		#self.paint_area.verticalScrollBar().setStyleSheet('width: 15px; background: #000000;')
		self.message_frame.setStyleSheet('border: 1px solid #000000')
		self.message_frame.setGeometry(870, 10, 320, 350)
		self.chat_widget.setGeometry(870, 370, 320, 100)
		self.chat_widget.setStyleSheet('background: #404040; border: 0px; color: #FFFFFF')
		self.changeco_btn.setGeometry(870, 480, 75, 30)
		self.changeco_btn.setStyleSheet("background: #303030; color: #FFFFFF; font-size: 12px")
		self.send_btn.setStyleSheet("background: #303030; color: #FFFFFF; font-size: 12px")
		self.send_btn.setGeometry(960, 480, 75, 30)
		#self.brush_label.setStyleSheet("font-size: 15px")
		#self.brush_label.move(1000, 480)
		self.brush_slider.setGeometry(1060, 488, 108, 15)
		#bself.brush_slider.show()
		self.userlist_widget.setGeometry(870, 520, 320, 170)
		self.userlist_widget.setStyleSheet('background: #404040; border: 0px')
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
		self.message_frame.setGeometry(
			self.message_frame.pos().x() + biasx, 
			self.message_frame.pos().y(),
			self.message_frame.width(),
			biasy + self.message_frame.height()
		)
		self.chat_widget.move(self.chat_widget.pos().x() + biasx, self.chat_widget.pos().y() + biasy)
		self.changeco_btn.move(self.changeco_btn.pos().x() + biasx, self.changeco_btn.pos().y() + biasy)
		self.send_btn.move(self.send_btn.pos().x() + biasx, self.send_btn.pos().y() + biasy)
		self.brush_slider.move(self.brush_slider.pos().x() + biasx, self.brush_slider.pos().y() + biasy)
		self.userlist_widget.move(self.userlist_widget.pos().x() + biasx, self.userlist_widget.pos().y() + biasy)
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
		print('I want to send: ' + text)
		global conn
		conn.sendall(bytes(text, encoding = 'utf-8'))
	
	def changeco(self):
		co = QColorDialog.getColor()
		if co.isValid() :
			self.paint_widget.set_color(co)
	
	def changewidth(self):
		self.paint_widget.set_width(self.brush_slider.value())
		
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
		global pix_pool, mess_pool, user_pool
		global PIX_pt, MESS_pt, USER_pt
		global pix_pt, mess_pt, user_pt
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
			self.window.message_frame.add_message(user_name, text_, user_name == self.user_name)
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

def update_pix_pool(text) :
	texts = text.split(':')
	pix_lock.acquire()
	global PIX_pt, pix_pool
	for _ in texts :
		print(_)
		#R, G, B, XX, XY, YX, YY = _.split(',')
		#pix_pool.append((int(R), int(G), int(B), QPoint(int(XX), int(XY)), QPoint(int(YX), int(YY))))
		pix_pool.append(_)
		PIX_pt += 1
	pix_lock.release()

def update_mess_pool(text) :
	mess_lock.acquire()
	global mess_pool, MESS_pt
	mess_pool.append(text)
	MESS_pt += 1
	mess_lock.release()

def update_user_pool(text) :
	user_lock.acquire()
	global user_pool, USER_pt
	user_pool.append(text)
	USER_pt += 1
	user_lock.release()

def add_pool(text) :	
	print('recv: ' + text)
	if (text[:3] == 'PIX') :
		update_pix_pool(text[4:])
	elif (text[:4] == 'MESS') :
		update_mess_pool(text[5:])
	elif (text[:4] == 'USER') :
		update_user_pool(text[5:])

def thread_recv() :
	text = ''
	while True:
		try: 
			ret_bytes = conn.recv(4096)
		except BaseException:
			return
		text += str(ret_bytes, encoding = 'utf-8')
		while True :
			index = text.find('<-END->')
			if (index > -1) :
				new_text = text[:index]
				text = text[index + 7:]
				add_pool(new_text)
			else : 
				break

if __name__ == '__main__' :	
	app = QApplication(sys.argv)
	if (len(sys.argv) < 2) :
		myip = '127.0.0.1'
		myport = 5000
	else :
		myip, myport = sys.argv[1].split(':')
	myport = int(myport)
	catbus = Catbus(myip, myport)
	network = threading.Thread(target = thread_recv)
	network.start()
	app.exec_()
	print('EXIT.')
	conn.sendall(bytes('USER:-' + catbus.user_name + '<-END->', encoding = 'utf-8'))
	conn.sendall(bytes('EXIT<-END->', encoding = 'utf-8'))
	conn.close()
