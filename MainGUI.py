#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
#Author: Björn Eistel
#Contact: <eistel@gmail.com>
#
# THIS SOURCE-CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED. IN NO  EVENT WILL THE AUTHOR BE HELD LIABLE FOR ANY DAMAGES ARISING FROM
# THE USE OF THIS SOURCE-CODE. USE AT YOUR OWN RISK.

import sys
import os
from PyQt4 import QtGui, QtCore

from configuration import *


class ValueBar(QtGui.QWidget):
    def __init__(self):
        super(ValueBar, self).__init__()
        self.initUI()

    def initUI(self):

        self.grid_layout = QtGui.QGridLayout()

        self.box = QtGui.QGroupBox(self)
        self.box.setGeometry(0, 0, 600, 80)
        self.box.setLayout(self.grid_layout)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)

        self.minValue = QtGui.QLineEdit()
        self.maxValue = QtGui.QLineEdit()
        self.value = QtGui.QLineEdit()

        for i in range(5):
            self.grid_layout.setColumnStretch(i, 1)

        self.grid_layout.addWidget(self.minValue, 0, 0)
        self.grid_layout.addWidget(self.value, 0, 1, 1, 3)
        self.grid_layout.addWidget(self.maxValue, 0, 4)

        self.grid_layout.addWidget(self.slider, 2, 0, 1, 5)

        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self.sliderChanged)
        self.connect(self.minValue, QtCore.SIGNAL('textChanged(QString)'), self.minValueChanged)
        self.connect(self.maxValue, QtCore.SIGNAL('textChanged(QString)'), self.maxValueChanged)

        self.initValues()
        self.show()

    def sliderChanged(self, value):
        self.value.setText(str(value))

    def minValueChanged(self, value):
        self.slider.setMinimum(int(self.minValue.text()))

    def maxValueChanged(self, value):
        self.slider.setMaximum(int(self.maxValue.text()))

    def initValues(self, value=50, min=0, max=100, title='???'):
        self.value.setText(str(value))
        self.minValue.setText(str(min))
        self.maxValue.setText(str(max))

        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(value)

        self.box.setTitle(title)


class EquationBox(QtGui.QWidget):
    def __init__(self, name, equation_data):
        super(EquationBox, self).__init__()
        self.name = name
        self.equation_data = equation_data
        self.initUI()

    def initUI(self):

        self.grid_layout = QtGui.QGridLayout()

        self.box = QtGui.QGroupBox(self)
        self.box.setGeometry(0, 0, 650, 380)
        self.box.setLayout(self.grid_layout)

        for symbol_name, equation_symbol in self.equation_data['DATA'].symbol_dict.items():
            bar = ValueBar()
            bar.initValues(title='%s [%s]' % (symbol_name, equation_symbol.unit),
                           value=equation_symbol.value, min=equation_symbol.min, max=equation_symbol.max)
            self.grid_layout.addWidget(bar)

        self.show()


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tooltips')

        self.vlayout = QtGui.QVBoxLayout(self)

        for name, data in EQUATION_DATA.items():
            eqb = EquationBox(name, data)
            self.vlayout.addWidget(eqb)

        self.show()
        return


if __name__ == '__main__':
    #dueto bug on ubuntu with i3
    os.environ['QT_GRAPHICSSYSTEM'] = 'native'

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

