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
import sympy
from sympy.core.symbol import Symbol
from PyQt4 import QtGui, QtCore




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

    def __init__(self):
        super(EquationBox, self).__init__()
        self.initUI()

    def initUI(self):

        self.grid_layout = QtGui.QGridLayout()

        self.box = QtGui.QGroupBox(self)
        self.box.setGeometry(0, 0, 650, 380)
        self.box.setLayout(self.grid_layout)


        '''
        self.symbols = 'U R I'
        self.symbols_list = self.symbols.split(' ')




        u, r, i = sympy.symbols(self.symbols)
        self.equation = sympy.Eq(u, r*i)

        for symbol in self.symbols_list:
            bar = ValueBar()
            bar.initValues(title=symbol, value=1, min=1, max=1000)
            self.grid_layout.addWidget(bar)

        self.result = QtGui.QLabel()


        '''
        #self.initValues()
        self.show()

class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tooltips')

        self.vlayout = QtGui.QVBoxLayout(self)

        btn1 = QtGui.QPushButton('Button 1')
        btn2 = QtGui.QPushButton('Button 2')
        btn3 = QtGui.QPushButton('Button 3')
        btn4 = QtGui.QPushButton('Button 4')

        self.vlayout.addWidget(EquationBox())
        #self.vlayout.addWidget(ValueBar())
        self.vlayout.addWidget(QtGui.QWidget())


        self.show()
        return



class EquationSymbol(object):
    def __init__(self, name, min=0, max=1000, value=500):
        self.name = name
        self.symbol = sympy.symbols(name)
        self.min = min
        self.max = max
        self.value = value

    def __repr__(self):
        return '#EquationSymbol %s, %d %d %d#' % (self.name, self.min, self.value, self.max)


class Equation(object):
    def __init__(self, expression, equation_symbol_list=[]):
        self.expression = expression

        expression_left_hand, expression_right_hand = expression.split('=')
        sympy_expression_left_hand = sympy.sympify(expression_left_hand)
        sympy_expression_right_hand = sympy.sympify(expression_right_hand)
        self.sympy_equation = sympy.Eq(sympy_expression_left_hand, sympy_expression_right_hand)

        self.symbols = list(set(self.findSymbols(self.sympy_equation)))

        self.symbol_dict = dict()
        for symbol in self.symbols:
            self.symbol_dict[str(symbol)] = EquationSymbol(name=str(symbol))

        for equation_symbol in equation_symbol_list:
            if equation_symbol.name in self.symbol_dict:
                self.symbol_dict[equation_symbol.name] = equation_symbol


    def findSymbols(self, eq):
        symbols = list()

        if isinstance(eq, Symbol):
            symbols.append(eq)
        else:
            for eqv in eq.args:
                symbols.extend(self.findSymbols(eqv))

        return symbols

    def calculate(self, symbol):
        eq = sympy.solve(self.sympy_equation, symbol)[0]
        for name, value in self.symbol_dict.items():
            eq = eq.subs(value.symbol, value.value)
        return eq.evalf()

if __name__ == '__main__':
    #dueto bug on ubuntu with i3
    os.environ['QT_GRAPHICSSYSTEM'] = 'native'

    eq = Equation('x = y**2 + r', [
        EquationSymbol(name='y', min=2, max=10, value=5),
        EquationSymbol(name='r', min=2, max=10, value=5),
        #EquationSymbol(name='x', min=2, max=10, value=5),
    ])


    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

