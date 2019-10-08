import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(400, 200)
        self.edit_label = QLabel('QTextEdit', self)
        self.browser_label = QLabel('QTextBrowser', self)
        self.text_edit = QTextEdit(self)
        self.text_browser = QTextBrowser(self)

        self.edit_v_layout = QVBoxLayout()
        self.browser_v_layout = QVBoxLayout()
        self.all_h_layout = QHBoxLayout()

        self.layout_init()
        self.text_edit_int()

    def layout_init(self):
        self.edit_v_layout.addWidget(self.edit_label)
        self.edit_v_layout.addWidget(self.text_edit)
        self.browser_v_layout.addWidget(self.browser_label)
        self.browser_v_layout.addWidget(self.text_browser)

        self.all_h_layout.addLayout(self.edit_v_layout)
        self.all_h_layout.addLayout(self.browser_v_layout)

        self.setLayout(self.all_h_layout)

    def text_edit_int(self):
        self.text_edit.textChanged.connect(self.show_text_func)

    def show_text_func(self):
        self.text_browser.setText(self.text_edit.toPlainText())


class Demo1(QWidget):
    def __init__(self):
        super(Demo1, self).__init__()
        self.resize(100, 100)
        self.text_button = QToolButton(self)
        self.text_button.setCheckable(True)
        self.text_button.setIcon(QIcon('button.png'))
        self.text_button.toggled.connect(self.button_state_func)

    def button_state_func(self):
        print(self.text_button.isChecked())

class Demo2(QWidget):
    def __init__(self):
        super(Demo2, self).__init__()
        self.off_button = QRadioButton('off', self)
        self.on_button = QRadioButton('on', self)
        self.pic_label = QLabel(self)

        self.button_h_layout = QHBoxLayout()
        self.pic_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        self.layout_init()
        self.radio_button_init()
        self.label_init()

    def layout_init(self):
        self.button_h_layout.addWidget(self.off_button)
        self.button_h_layout.addWidget(self.on_button)
        self.pic_h_layout.addStretch(1)
        self.pic_h_layout.addWidget(self.pic_label)
        self.pic_h_layout.addStretch(1)
        self.all_v_layout.addLayout(self.pic_h_layout)
        self.all_v_layout.addLayout(self.button_h_layout)

        self.setLayout(self.all_v_layout)

    def radio_button_init(self):
        self.off_button.setChecked(True)
        self.off_button.toggled.connect(self.on_off_bulb_func)
        # self.on_button.toggled.connect(self.on_off_bulb_func)

    def label_init(self):
        self.pic_label.setPixmap(QPixmap('off.png'))

    def on_off_bulb_func(self):
        if self.off_button.isChecked():
            self.pic_label.setPixmap(QPixmap('off.png'))
        else:
            self.pic_label.setPixmap(QPixmap('on.png'))


class Demo3(QWidget):
    def __init__(self):
        super(Demo3, self).__init__()
        self.checkbox1 = QCheckBox('ckeckbox1', self)
        self.checkbox2 = QCheckBox('checkbox2', self)
        self.checkbox3 = QCheckBox('checkbox3', self)

        self.v_layout = QVBoxLayout()

        self.check_init()
        self.layout_init()

    def layout_init(self):
        self.v_layout.addWidget(self.checkbox1)
        self.v_layout.addWidget(self.checkbox2)
        self.v_layout.addWidget(self.checkbox3)

        self.setLayout(self.v_layout)

    def check_init(self):
        self.checkbox1.setChecked(True)
        # self.checkbox1.setCheckState(Qt.Checked)
        self.checkbox1.stateChanged.connect(lambda: self.on_state_change_func(self.checkbox1))

        self.checkbox2.setChecked(True)
        # self.checkbox2.setCheckState(Qt.Checked)
        self.checkbox2.stateChanged.connect(lambda: self.on_state_change_func(self.checkbox2))

        self.checkbox3.setTristate(True)
        self.checkbox3.setCheckState(Qt.PartiallyChecked)
        self.checkbox3.stateChanged.connect(lambda: self.on_state_change_func(self.checkbox3))

    def on_state_change_func(self, checkbox):
        print('{} was clicked , and its current state is {}'.format(checkbox.text(), checkbox.checkState()))


class Demo4(QWidget):
    choice = 'a'
    choice_list = ['b', 'c', 'd', 'e']

    def __init__(self):
        super(Demo4, self).__init__()
        self.combobox_1 = QComboBox(self)
        self.combobox_2 = QFontComboBox(self)
        self.lineedit = QLineEdit(self)
        self.v_layout = QVBoxLayout()

        self.layout_init()
        self.combobox_init()

    def layout_init(self):
        self.v_layout.addWidget(self.combobox_1)
        self.v_layout.addWidget(self.combobox_2)
        self.v_layout.addWidget(self.lineedit)

        self.setLayout(self.v_layout)

    def combobox_init(self):
        self.combobox_1.addItem(self.choice)
        self.combobox_1.addItems(self.choice_list)
        self.combobox_1.currentIndexChanged.connect(lambda: self.on_combobox_func(self.combobox_1))
        self.combobox_2.currentFontChanged.connect(lambda: self.on_combobox_func(self.combobox_2))

    def on_combobox_func(self, combobox):
        if combobox == self.combobox_1:
            QMessageBox.information(self, 'Combobox_1',  '{}:{}'.format(combobox.currentIndex(), self.combobox_1.currentText()))
        else:
            self.lineedit.setFont(combobox.currentFont())

class Demo5(QWidget):
    def __init__(self):
        super(Demo5, self).__init__()
        self.spinbox = QSpinBox(self)
        self.spinbox.setRange(-99, 99)
        self.spinbox.setSingleStep(1)
        self.setVisible(66)
        self.spinbox.valueChanged.connect(self.value_change_func)

        self.double_spinbox = QDoubleSpinBox(self)
        self.double_spinbox.setRange(-99.99, 99.99)
        self.double_spinbox.setSingleStep(0.01)
        self.double_spinbox.setValue(66.66)
        self.double_spinbox.valueChanged.connect(self.value_change_func)

        self.layout_init()

    def layout_init(self):
        self.all_h_layout = QHBoxLayout()
        self.all_h_layout.addWidget(self.spinbox)
        self.all_h_layout.addWidget(self.double_spinbox)

        self.setLayout(self.all_h_layout)

    def value_change_func(self):
        decimal_part = self.double_spinbox.value() - int(self.double_spinbox.value())
        self.double_spinbox.setValue(self.spinbox.value() + decimal_part)


class Demo6(QWidget):
    def __init__(self):
        super(Demo6, self).__init__()
        self.slider_1 = QSlider(Qt.Horizontal, self)
        self.slider_1.setRange(0, 100)
        self.slider_1.valueChanged.connect(lambda: self.on_change_func(self.slider_1))

        self.slider_2 = QSlider(Qt.Vertical, self)
        self.slider_2.setMinimum(0)
        self.slider_2.setMaximum(100)
        self.slider_2.valueChanged.connect(lambda: self.on_change_func(self.slider_2))

        self.label = QLabel('0', self)
        self.label.setFont(QFont('Arial Black', 20))

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.h_layout.addWidget(self.slider_2)
        self.h_layout.addStretch(1)
        self.h_layout.addWidget(self.label)
        self.h_layout.addStretch(1)

        self.v_layout.addWidget(self.slider_1)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def on_change_func(self, slider):
        if slider == self.slider_1:
            self.slider_2.setValue(self.slider_1.value())
            self.label.setText(str(self.slider_1.value()))
        else:
            self.slider_1.setValue(self.slider_2.value())
            self.label.setText(str(self.slider_2.value()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo6()
    demo.show()
    sys.exit(app.exec_())

