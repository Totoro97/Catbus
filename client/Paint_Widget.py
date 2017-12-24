import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Paint_Widget(QWidget):
	
	def __init__(self, father = None, conn = None):
		super().__init__(father)
		self.conn = conn
		self.scale = 1.0
		self.brush_size = 5
		self.pressing = False
		self.key_left_pressing = False
		self.key_right_pressing = False
		self.key_up_pressing = False
		self.key_down_pressing = False
		self.key_9 = False
		self.key_0 = False
		self.key_minus = False
		self.key_equal = False
		self.biasx = 0
		self.biasy = 0
		self.A = QPoint(0, 0)
		self.B = QPoint()
		self.color_R = 0
		self.color_G = 0
		self.color_B = 0
		#self.painter = QPainter(self)
		self.points = []
		self.init_UI()
		
		self.pix_width = 2000
		self.pix_height = 1600
		self.canvas = QPixmap(self.pix_width, self.pix_height)
		self.init_canvas()
		
		if (father != None):		
			self.show()


	def init_UI(self):
		self.setGeometry(100, 100, 100, 100)
		return
	
	def init_canvas(self):
		self.canvas.fill(QColor(255, 255, 255))
	
	def bias_proc(self):
		if self.key_left_pressing :
			self.biasx -= 3
		if self.key_right_pressing :
			self.biasx += 3
		if self.key_up_pressing :
			self.biasy -= 3
		if self.key_down_pressing :
			self.biasy += 3
		
	def brush_size_proc(self) :
		if self.key_0 :
			self.brush_size += 1
		if self.key_9 :
			self.brush_size -= 1
	
	def scale_proc(self):
		if self.key_minus :
			self.scale *= 0.8
		if self.key_equal :
			self.scale /= 0.8

	def paintEvent(self, e):
		self.bias_proc()
		self.brush_size_proc()
		self.scale_proc()
		painter = QPainter(self.canvas)
		painter.setRenderHint(QPainter.Antialiasing, True)
		pen = QPen()
		pen.setWidth(self.brush_size)
		#pen.setBrush(QBrush(Qt.RadialGradientPattern))
		pen.setCapStyle(Qt.RoundCap)
		pen.setJoinStyle(Qt.RoundJoin)
		painter.setPen(pen)
		filler = QPainter(self)
		for (cR, cG, cB, A, B) in self.points:
			pen.setColor(QColor(cR, cG, cB))
			painter.drawLine(A, B)
			
		new_canvas = self.canvas.scaled(
			self.pix_width * self.scale, 
			self.pix_height * self.scale, 
			Qt.KeepAspectRatio,
			#Qt.SmoothTransformation
			Qt.FastTransformation
		)
		
		filler.drawPixmap(self.biasx, self.biasy, new_canvas)
		
	def mousePressEvent(self, e):
		self.setCursor(QCursor(Qt.PointingHandCursor))
		self.A = e.pos()
		self.B = e.pos()
		self.pressing = True
	
	def mouseMoveEvent(self, e):
		if (not self.pressing) :
			return
		self.A = self.B
		self.B = e.pos()
		bias = QPoint(self.biasx, self.biasy)
		x = (self.A - bias) / self.scale
		y = (self.B - bias) / self.scale
		self.conn.sendall(bytes('PIX:' + self.pix2str((
			self.color_R,
			self.color_G,
			self.color_B,
			x,
			y
		)) + '<-END->', encoding = 'utf-8'))
		#print(len(self.points))
		self.update()
	
	def add_pix(self, text):
		#text = text[4: -7]
		colors = text.split(':')
		for _ in colors :
			R, G, B, XX, XY, YX, YY = _.split(',')
			self.points.append((int(R), int(G), int(B), QPoint(int(XX),int(XY)), QPoint(int(YX), int(YY))))
		self.update()
		
	def pix2str(self, pix) :
		R, G, B, X, Y = pix
		text = str(R) + ',' + str(G) + ',' + str(B) + ',' + str(X.x()) + ',' + str(X.y()) + ',' + str(Y.x()) + ',' + str(Y.y())
		return text

	def mouseReleaseEvent(self, e):
		self.setCursor(QCursor(Qt.ArrowCursor))
		self.pressing = False


if __name__ == '__main__' :
	app = QApplication(sys.argv)
	window = Paint_Widget()
	sys.exit(app.exec_())
