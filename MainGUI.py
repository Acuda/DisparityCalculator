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
        #self.box.setGeometry(0, 0, 600, 80)
        self.box.setLayout(self.grid_layout)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider_nk = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider_nk.setMinimum(0)
        self.slider_nk.setMaximum(999)

        self.minValue = QtGui.QLineEdit()
        self.maxValue = QtGui.QLineEdit()
        self.value = QtGui.QLineEdit()

        for i in range(5):
            self.grid_layout.setColumnStretch(i, 1)

        self.grid_layout.addWidget(self.minValue, 0, 0)
        self.grid_layout.addWidget(self.value, 0, 1, 1, 3)
        self.grid_layout.addWidget(self.maxValue, 0, 4)

        self.grid_layout.addWidget(self.slider, 2, 0, 1, 5)
        self.grid_layout.addWidget(self.slider_nk, 3, 0, 1, 5)

        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self.sliderChanged)
        self.connect(self.slider_nk, QtCore.SIGNAL('valueChanged(int)'), self.sliderChanged)
        self.connect(self.minValue, QtCore.SIGNAL('textChanged(QString)'), self.minValueChanged)
        self.connect(self.maxValue, QtCore.SIGNAL('textChanged(QString)'), self.maxValueChanged)

        self.initValues()
        self.show()

    def sliderChanged(self, value):
        self.value.setText('%d.%03d' % (self.slider.value(), self.slider_nk.value()))

    def minValueChanged(self, value):
        self.slider.setMinimum(int(self.minValue.text()))

    def maxValueChanged(self, value):
        self.slider.setMaximum(int(self.maxValue.text()))

    def initValues(self, value=50, min=0, max=100, title='???'):
        self.value.setText(str(value))
        self.minValue.setText(str(min))
        self.maxValue.setText(str(max))

        ival = int(value)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(ival)

        self.slider_nk.setValue(int(value*1e3 - ival*1e3))

        self.box.setTitle(title)

    def updateValue(self, value):


        ival = int(value)
        nkval = int(value*1e3 - ival*1e3)

        print 'UPDATE VALUE', value, ival, nkval
        self.value.setText('%d.%03d' % (ival, nkval))
        self.slider.setValue(ival)
        self.slider_nk.setValue(nkval)


class EquationBox(QtGui.QWidget):
    def __init__(self, name, equation_data):
        super(EquationBox, self).__init__()
        self.name = name
        self.equation_data = equation_data
        self.initUI()

    def initUI(self):
        self.grid_layout = QtGui.QGridLayout()

        num_symbols = len(self.equation_data['DATA'].symbol_dict)

        self.box = QtGui.QGroupBox(self)
        self.box.setGeometry(0, 0, 475, num_symbols*110+85)


        self.box.setTitle('%s [%s]' % (self.name, self.equation_data['DATA'].sympy_equation))
        self.box.setLayout(self.grid_layout)

        self.grid_layout.setColumnStretch(0, 1)

        idx = 0
        scale = 8
        self.equation_data['ValueBar'] = list()
        self.equation_data['radio'] = list()
        self.equation_data['name_order'] = list()
        for symbol_name, equation_symbol in self.equation_data['DATA'].symbol_dict.items():
            self.equation_data['name_order'].append(symbol_name)

            bar = ValueBar()
            bar.initValues(title='%s [%s]' % (symbol_name, equation_symbol.unit),
                           value=equation_symbol.value, min=equation_symbol.min, max=equation_symbol.max)
            self.grid_layout.addWidget(bar, idx*scale, 0, scale, 1)
            self.equation_data['ValueBar'].append(bar)

            radio = QtGui.QRadioButton()
            radio.setChecked(equation_symbol.isResult)
            self.grid_layout.addWidget(radio, idx*scale, 1, scale, 1)
            self.equation_data['radio'].append(radio)

            idx += 1

        lblResult = QtGui.QLabel()
        lblResult.setText('Result: ???')
        self.equation_data['lblResult'] = lblResult
        self.grid_layout.addWidget(lblResult, idx*scale, 0)

        button = QtGui.QPushButton('CALC')
        QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), self.calculateEquation)
        self.grid_layout.addWidget(button, (idx+1)*scale, 0)


        self.show()

    def calculateEquation(self):
        target_idx = -1
        for idx, symbol_name in enumerate(self.equation_data['name_order']):
            new_value = float(self.equation_data['ValueBar'][idx].value.text())
            new_value *= self.equation_data['DATA'].symbol_dict[symbol_name].factor
            self.equation_data['DATA'].symbol_dict[symbol_name].value = new_value

            if self.equation_data['radio'][idx].isChecked():
                target_idx = idx

        target_symbol = self.equation_data['name_order'][target_idx]
        result = self.equation_data['DATA'].calculate(target_symbol)
        self.equation_data['lblResult'].setText('Result: %07.3f' % result)

        target_factor = 1.0/self.equation_data['DATA'].symbol_dict[target_symbol].factor
        self.equation_data['ValueBar'][target_idx].updateValue(result*target_factor)



class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tooltips')

        self.hlayout = QtGui.QHBoxLayout(self)
        self.vlayout = QtGui.QVBoxLayout()
        self.hlayout.addLayout(self.vlayout)

        for name, data in EQUATION_DATA.items():
            eqb = EquationBox(name, data)
            self.hlayout.addWidget(eqb)
            eqb.calculateEquation()

        self.show()
        return


if __name__ == '__main__':
    #dueto bug on ubuntu with i3
    os.environ['QT_GRAPHICSSYSTEM'] = 'native'

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

