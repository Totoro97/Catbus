import socket
import threading
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

global pix_pool
global mess_pool
global user_pool
global PIX_pt
global MESS_pt
global USER_pt
PIX_pt = 0
MESS_pt = 0
USER_pt = 0
pix_pool = []
mess_pool = []
user_pool = []

sk = socket.socket()
sk.bind(("127.0.0.1", 5001))
sk.listen(10)

def pix2str(self, pix) :
	R, G, B, X, Y = pix
	text = str(R) + ',' + str(G) + ',' + str(B) + ',' + str(X.x()) + ',' + str(X.y()) + ',' + str(Y.x()) + ',' + str(Y.y())
	return text

def update_pix_pool(text) :
	texts = text[4:-7].split(':')
	global PIX_pt
	global pix_pool
	for _ in texts :
		print(_)
		R, G, B, XX, XY, YX, YY = _.split(',')
		pix_pool.append((int(R), int(G), int(B), QPoint(int(XX), int(XY)), QPoint(int(YX), int(YY))))
		PIX_pt += 1

def update_mess_pool(text) :
	text = text[5:-7]
	global mess_pool
	global MESS_pt
	mess_pool.append(text)
	MESS_pt += 1

def update_user_pool(text) :
	text = text[5: -7]
	global user_pool
	global USER_pt
	user_pool.append(user_name + '<-DIV->' + text)
	USER_pt += 1

def recv(conn) :
	print('I am in recv')
	#print(conn)
	text = ''
	cnt = 0
	while True:
		ret_bytes = conn.recv(4096)
		ret_text = str(ret_bytes, encoding = 'utf-8')
		text += ret_text
		print('text = %s'%(text))
		if text == '' :
			cnt += 1
		if (cnt > 0) :
			break
		if text[-7:] == '<-END->' :
			break
	return text

global t_cnt
t_cnt = 0
def sing(conn, addr) :
	global pix_pool
	global mess_pool
	global user_pool
	global PIX_pt
	global MESS_pt
	global USER_pt
	global t_cnt
	t_cnt += 1
	t_id = t_cnt
	print('I am in')
	user_pt = 0
	mess_pt = 0
	pix_pt = 0
	text = recv(conn)
	time.sleep(0.1)
	user_name = text[:-7]
	print(user_name)
	user_pool.append('+' + user_name)
	USER_pt += 1
	while True :
		print(t_id)
		time.sleep(0.5)
		text = 'PIX'
		while pix_pt < PIX_pt :
			print('send pix')
			text += ':' + pix2str(conn, pix_pool[pix_pt])
			pix_pt += 1
		if (text != 'PIX') :
			conn.sendall(bytes(text + '<-END->', encoding = 'utf-8'))

		while mess_pt < MESS_pt :
			conn.sendall(bytes('MESS:' + mess_pool[mess_pt] + '<-END->', encoding = 'utf-8'))
			mess_pt += 1

		while user_pt < USER_pt :
			conn.sendall(bytes('USER:' + user_pool[user_pt] + '<-END->', encoding = 'utf-8'))
			user_pt += 1

		recv_str = recv(conn)
		if (recv_str[:3] == 'PIX') :
			update_pix_pool(recv_str)
		elif (recv_str[:4] == 'MESS') :
			update_mess_pool(recv_str)
		elif (recv_str[:4] == 'USER') :
			update_user_pool(recv_str)
		elif (recv_str[:4] == 'EXIT') :
			conn.close()
			break
	user_pool.append('-' + user_name)
	USER_pt -= 1

while True :
	conn, addr = sk.accept()
	_ = threading.Thread(target = sing, args = (conn, addr))
	_.start()