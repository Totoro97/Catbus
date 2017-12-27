import socket
import threading
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

global pix_lock, mess_lock, user_lock
global pix_pool, mess_pool, user_pool
global PIX_pt, MESS_pt, USER_pt
global t_cnt
t_cnt = 0
PIX_pt = 0
MESS_pt = 0
USER_pt = 0
pix_pool = []
mess_pool = []
user_pool = []
pix_lock = threading.Lock()
mess_lock = threading.Lock()
user_lock = threading.Lock()

def pix2str(self, pix) :
	R, G, B, W, X, Y = pix
	text = str(R) + ',' + str(G) + ',' + str(B) + ',' + str(W) + ',' + str(X.x()) + ',' + str(X.y()) + ',' + str(Y.x()) + ',' + str(Y.y())
	return text

def update_pix_pool(text) :
	texts = text.split(':')
	pix_lock.acquire()
	global PIX_pt, pix_pool
	for _ in texts :
		print(_)
		R, G, B, W, XX, XY, YX, YY = _.split(',')
		pix_pool.append((int(R), int(G), int(B), int(W), QPoint(int(XX), int(XY)), QPoint(int(YX), int(YY))))
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

def thread_recv(conn) :
	text = ''
	print('I am in thread_recv')
	while True:
		ret_bytes = conn.recv(4096)
		text += str(ret_bytes, encoding = 'utf-8')
		while True :
			index = text.find('<-END->')
			if (index > -1) :
				new_text = text[:index]
				text = text[index + 7:]
				if new_text[:4] == 'EXIT' :
					return
				add_pool(new_text)
			else : 
				break

def sing(conn, addr) :
	global pix_pool, mess_pool, user_pool
	global PIX_pt, MESS_pt, USER_pt
	global t_cnt
	t_cnt += 1
	t_id = t_cnt
	print('I am in')
	user_pt = 0
	mess_pt = 0
	pix_pt = 0
	#text = recv(conn)
	#time.sleep(0.1)
	#user_name = text[:-7]
	#print(user_name)
	#user_pool.append('+' + user_name)
	#USER_pt += 1
	sing_t = threading.Thread(target = thread_recv, args = (conn,))
	sing_t.start()
	while True :
		#print(t_id)
		#time.sleep(0.5)
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
		
		if not sing_t.isAlive() :
			print('close')
			conn.close()
			return

if (len(sys.argv) < 2) :
	myip = '127.0.0.1'
	myport = 5000
else :
	myip, myport = sys.argv[1].split(':')
	myport = int(myport)
	
sk = socket.socket()
sk.bind((myip, myport))
sk.listen(10)

while True :
	conn, addr = sk.accept()
	_ = threading.Thread(target = sing, args = (conn, addr))
	_.start()
