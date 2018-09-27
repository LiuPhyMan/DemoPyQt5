#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 16:56 2018/9/26

@author:    Liu Jinbao
@mail:      liu.jinbao@outlook.com
@project:   DemoPyQt5
@IDE:       PyCharm
"""
import sys
import re
from PyQt5 import QtWidgets as QW
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont, QCursor
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


class PlotCanvas(FigureCanvas):

    def __init__(self, parent, _figure):
        FigureCanvas.__init__(self, _figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QW.QSizePolicy.Expanding, QW.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class QPlot(QW.QWidget):

    def __init__(self, parent=None, figsize=(5, 4), dpi=100):
        super().__init__(parent)
        self.figure = Figure(figsize=figsize, dpi=dpi)
        self.canvas = PlotCanvas(parent, self.figure)
        self.canvas.setFixedSize(figsize[0] * dpi, figsize[1] * dpi)
        layout = QW.QHBoxLayout(parent)
        toolbar = NavigationToolbar(self.canvas, parent=parent, coordinates=False)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setOrientation(Qt.Vertical)
        toolbar.update()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class ReadFileQWidget(QW.QWidget):
    pathChanged = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = ""
        self._entry = QW.QLineEdit()
        self._entry.setEnabled(True)
        self._entry.setMinimumWidth(600)
        self._entry.setCursor(QCursor(Qt.IBeamCursor))
        self._browse = QW.QPushButton('Browse')
        self._browse.setCursor(QCursor(Qt.PointingHandCursor))
        self._set_layout()

    def _set_layout(self):
        _layout = QW.QHBoxLayout()
        _layout.addWidget(self._entry)
        _layout.addWidget(self._browse)
        _layout.addStretch(1)
        self.setLayout(_layout)
        self._set_connect()

    def _set_connect(self):
        self._browse.clicked.connect(self._browse_callback)

    def _browse_callback(self):
        _path = QW.QFileDialog.getOpenFileName(caption='Open File',
                                               filter="spec file (*.asc)")[0]
        shorten_path = re.fullmatch(r".*(/[^/]+.asc)", _path).groups()[0]
        self.path = _path
        self._entry.setText(shorten_path)

    def _set_slot(self):
        self._entry.chan


class SpectraPlot(QPlot):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel('Wavelength [nm]')
        self.axes.set_ylabel("Intensity [a.u.]")
        self._spec_data = []
        self._lines = []

    def add_spec(self, wavelength, intensity):
        self._spec_data.append(SpecData(wavelength, intensity))
        _ln, = self.axes.plot(wavelength, intensity, linewidth=.5, marker='.')
        self._lines.append(_ln)
        self.canvas_draw()

    def delete_spec(self, index_to_delete):
        self._spec_data.pop(index_to_delete)
        self._lines.pop(index_to_delete)
        self.canvas_draw()

    def canvas_draw(self):
        self.canvas.draw()
    # def plot_spectra(self):
    #     sel


class SpecData(object):

    def __init__(self, wavelength, intensity):
        self.wavelength = wavelength
        self.intensity = intensity


class TheComboBox(QW.QComboBox):
    def __init__(self):
        super().__init__()
        # self.resize(200, 25)
        pixmap = QPixmap(20, 20)
        for color in ("red", "orange", "yellow"):
            pixmap.fill(QColor(color))
            self.addItem(QIcon(pixmap), color)


class BetterQLabel(QW.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = QFont("Ubuntu", 10)
        self.setFont(font)


class SettingQWidget(QW.QWidget):

    def __init__(self):
        super().__init__()
        self._box = TheComboBox()
        self._width_lineedit = QW.QLineEdit()
        _layout = QW.QGridLayout()
        _layout.addWidget(BetterQLabel('1. Plot properties'), 0, 0, 1, 2)
        _layout.addWidget(BetterQLabel('Color'), 1, 0, alignment=Qt.AlignRight)
        _layout.addWidget(self._box, 1, 1)
        _layout.addWidget(BetterQLabel("Width"), 2, 0, alignment=Qt.AlignRight)
        _layout.addWidget(self._width_lineedit, 2, 1)
        _layout.addWidget(BetterQLabel("2. Adjustment"), 3, 0, 1, 2)
        _layout.addWidget(BetterQLabel("x"), 4, 0, alignment=Qt.AlignRight)
        _layout.addWidget(QW.QDoubleSpinBox(), 4, 1)
        _layout.addWidget(BetterQLabel("y"), 5, 0, alignment=Qt.AlignRight)
        _layout.addWidget(QW.QDoubleSpinBox(), 5, 1)
        _layout.addWidget(BetterQLabel("baseline"), 6, 0, alignment=Qt.AlignRight)
        _layout.addWidget(QW.QDoubleSpinBox(), 6, 1)
        _layout.addWidget(BetterQLabel("*I0"), 7, 0, alignment=Qt.AlignRight)
        _layout.addWidget(QW.QDoubleSpinBox(), 7, 1)
        _layout.setRowStretch(8, 1)
        self.setLayout(_layout)


class TheWindow(QW.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 600)
        # self.showMaximized()
        self.cenWidget = QW.QWidget()
        self.setting = SettingQWidget()
        self.spectra_plot = SpectraPlot()
        self.read_file = ReadFileQWidget()
        self.setCentralWidget(self.cenWidget)
        self.setWindowIcon(QIcon("matplotlib_large.png"))

        _layout1 = QW.QHBoxLayout()
        _layout1.addWidget(self.spectra_plot)
        _layout1.addWidget(self.setting)
        _layout0 = QW.QVBoxLayout()
        _layout0.addLayout(_layout1)
        _layout0.addWidget(self.read_file)
        _layout0.addStretch(1)
        self.cenWidget.setLayout(_layout0)


# ----------------------------------------------------------------------------------------------- #
if not QW.QApplication.instance():
    app = QW.QApplication(sys.argv)
else:
    app = QW.QApplication.instance()
app.setStyle(QW.QStyleFactory.create("Fusion"))
window = TheWindow()
window.show()
window.spectra_plot.add_spec([1, 2, 3, 4], [2, 3, 4, 5])
window.spectra_plot.add_spec([2, 3, 4, 5], [9, 8, 3, 4])
# app.exec_()
app.aboutToQuit.connect(app.deleteLater)
