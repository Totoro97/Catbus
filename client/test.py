import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import QWebView

class Example(QWidget):
     
    def __init__(self):
        super().__init__()
         
        self.initUI()
         
         
    def initUI(self):     
 
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)
         
        self.le = QLineEdit(self)
        self.le.move(130, 22)
         
        self.setGeometry(300, 300, 400, 800)
        self.setWindowTitle('Input dialog')
        self.webview = QWebView(self)
        html_file = open('Message_Frame.html', 'r')
        html = html_file.read()
        html_file.close()
        self.webview.setHtml(html)
        self.webview.setGeometry(0, 0, 400, 800)
        self.show()
         
         
    def showDialog(self):
         
        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')
         
        if ok:
            self.le.setText(str(text))
         
         
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
