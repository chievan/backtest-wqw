import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

USER_PWD = {
    'wuqiwen':'password'
    }

# 信息框布局
class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(250, 100)
        self.user_label = QLabel('username', self)
        self.pwd_label = QLabel('password', self)
        self.user_line = QLineEdit(self)
        self.pwd_line = QLineEdit(self)
        self.login_button = QPushButton('Log in', self)
        self.signin_button = QPushButton('Sign in', self)

        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

    def layout_init(self):
        self.grid_layout.addWidget(self.user_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.user_line, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.pwd_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.pwd_line, 1, 1, 1, 1)
        self.h_layout.addWidget(self.login_button)
        self.h_layout.addWidget(self.signin_button)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def lineedit_init(self):
        self.user_line.setPlaceholderText('Please enter your username')
        self.pwd_line.setPlaceholderText('Please enter your password')
        self.user_line.textChanged.connect(self.check_input_func)
        self.pwd_line.textChanged.connect(self.check_input_func)

    def check_input_func(self):
        if self.user_line.text() and self.pwd_line.text()
            self.login_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)
        self.user_line.clear()
        self.pwd_line.clear()

    def pushbutton_init(self):
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.check_input_func)


# 信息框学习
class Demo1(QWidget):
    def __init__(self):
        super(Demo1, self).__init__()
        self.resize(200, 200)
        self.button = QPushButton('information', self)
        self.button.clicked.connect(self.show_messeagebox)

    def show_messeagebox(self):
        choice = QMessageBox.information(self, 'title', 'Content', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if choice == QMessageBox.Yes:
            self.button.setText("Yes 出现了")
        elif choice == QMessageBox.No:
            self.button.setText("No 出现了")
        elif choice == QMessageBox.Cancel:
            self.button.setText("Cancel 出现了")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())