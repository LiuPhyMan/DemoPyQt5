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
import numpy as np
from PyQt5 import QtWidgets as QW
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont, QCursor
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


class BetterButton(QW.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        _font = QFont('Ubuntu', 11)
        self.setFont(_font)
        self.setStyleSheet(':hover {background-color: #87CEFA ;}')


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
        self._entry.setFont(QFont("Ubuntu", 10))
        self._browse = BetterButton("Browse")
        self._browse.setCursor(QCursor(Qt.PointingHandCursor))
        self._set_layout()
        self._set_connect()
        self._set_slot()

    def _set_layout(self):
        _layout = QW.QHBoxLayout()
        _layout.addWidget(self._entry)
        _layout.addWidget(self._browse)
        _layout.addStretch(1)
        self.setLayout(_layout)

    def _set_connect(self):
        self._browse.clicked.connect(self._browse_callback)

    def _browse_callback(self):
        print('button_pressed')
        _path = QW.QFileDialog.getOpenFileName(caption='Open File',
                                               filter="spec file (*.asc)")[0]
        shorten_path = re.fullmatch(r".*(/[^/]+/[^/]+/[^/]+.asc)", _path).groups()[0]
        self.path = _path
        self._entry.setText(shorten_path)

    def _set_slot(self):
        def slot_emit():
            print('emit')
            self.pathChanged.emit()

        self._entry.textChanged.connect(slot_emit)


class SpectraPlot(QPlot):

    def __init__(self, parent=None):
        super().__init__(parent, figsize=(12, 6))
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel('Wavelength [nm]')
        self.axes.set_ylabel("Intensity [a.u.]")
        self.axes.grid(linestyle='--')
        self._cursor = Cursor(self.axes, color='green', linewidth=.5)
        self.figure.tight_layout()
        self._spec_data = []
        self._lines = []
        # self._set_connect()

    def add_spec(self, wavelength, intensity):
        print('add_spec')
        self._spec_data.append(SpecData(wavelength, intensity))
        _ln, = self.axes.plot(wavelength, intensity, linewidth=.5, marker='.', alpha=0.5)
        self._lines.append(_ln)
        self.canvas_draw()

    def delete_spec(self, index_to_delete):
        self._spec_data.pop(index_to_delete)
        self._lines.pop(index_to_delete)
        self.canvas_draw()

    def highlight_line(self, index_to_highlight):
        for _i, _ln in enumerate(self._lines):
            if _i == index_to_highlight:
                _ln.set_linewidth(1.5)
                _ln.set_alpha(1)
            else:
                _ln.set_linewidth(.5)
                _ln.set_alpha(.5)
        self.canvas_draw()

    def canvas_draw(self):
        self.canvas.draw()
    # def plot_spectra(self):
    #     sel


class TheQListWidget(QW.QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.
        # self.currentRowChanged


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

class BetterQDoubleSpinBox(QW.QDoubleSpinBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = QFont("Ubuntu", 10)
        self.setFont(font)


class SettingQWidget(QW.QWidget):
    settingChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._box = TheComboBox()
        self._text = QW.QLineEdit()
        self._text.setFont(QFont("Ubuntu", 10))
        _layout = QW.QGridLayout()
        _layout.addWidget(BetterQLabel('1. Plot properties'), 0, 0, 1, 2)
        _layout.addWidget(BetterQLabel('Color'), 1, 0, alignment=Qt.AlignRight)
        _layout.addWidget(self._box, 1, 1)
        _layout.addWidget(BetterQLabel("Text"), 2, 0, alignment=Qt.AlignRight)
        _layout.addWidget(self._text, 2, 1)
        _layout.addWidget(BetterQLabel("2. Adjustment"), 3, 0, 1, 2)
        # _layout.addWidget(BetterQLabel("x0"), 4, 0, alignment=Qt.AlignRight)
        # _layout.addWidget(QW.QDoubleSpinBox(), 4, 1)
        # _layout.addWidget(BetterQLabel("k0"), 5, 0, alignment=Qt.AlignRight)
        # _layout.addWidget(QW.QDoubleSpinBox(), 5, 1)
        _layout.addWidget(BetterQLabel("baseline"), 4, 0, alignment=Qt.AlignRight)
        _layout.addWidget(BetterQDoubleSpinBox(), 4, 1)
        _layout.addWidget(BetterQLabel("*I0"), 5, 0, alignment=Qt.AlignRight)
        _layout.addWidget(BetterQDoubleSpinBox(), 5, 1)
        _layout.setRowStretch(6, 1)
        self.setLayout(_layout)
        self._set_connect()

    def _set_connect(self):
        def slot_emit():
            self.settingChanged.emit()

        self._text.textChanged.connect(slot_emit)


class TheWindow(QW.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.resize(800, 600)
        # self.showMaximized()
        self.cenWidget = QW.QWidget()
        self.spectra_plot = SpectraPlot()
        self.exp_list = TheQListWidget()
        self.setting = SettingQWidget()
        self.read_file = ReadFileQWidget()
        self.setCentralWidget(self.cenWidget)
        self.setWindowIcon(QIcon("matplotlib_large.png"))

        _layout2 = QW.QVBoxLayout()
        _layout2.addWidget(self.exp_list)
        _layout2.addWidget(self.setting)
        _layout1 = QW.QHBoxLayout()
        _layout1.addWidget(self.spectra_plot)
        _layout1.addLayout(_layout2)
        _layout1.addStretch(1)
        _layout0 = QW.QVBoxLayout()
        _layout0.addLayout(_layout1)
        _layout0.addWidget(self.read_file)
        _layout0.addStretch(1)
        self.cenWidget.setLayout(_layout0)
        self._set_connect()

    def _set_connect(self):
        self.read_file.pathChanged.connect(self.read_spec_data)

        def exp_list_row_changed_callback():
            self.spectra_plot.highlight_line(self.exp_list.currentRow())
            self.setting._text.setText(self.exp_list.currentItem().text())

        def setting_changed_callback():
            self.exp_list.currentItem().setText(self.setting._text.text())

        self.exp_list.currentRowChanged.connect(exp_list_row_changed_callback)
        self.setting.settingChanged.connect(setting_changed_callback)

    def read_spec_data(self):
        # .asc file appends setting info.
        output = np.genfromtxt(self.read_file.path, skip_footer=41)
        wavelength = output[:, 0]
        intensity = output[:, 1]
        self.spectra_plot.add_spec(wavelength, intensity)
        _pixmap = QPixmap(20, 20)
        _current_line_color = self.spectra_plot._lines[-1].get_color()
        _pixmap.fill(QColor(_current_line_color))
        item_to_add = QW.QListWidgetItem()
        item_to_add.setText(self.read_file._entry.text())
        item_to_add.setIcon(QIcon(_pixmap))
        self.exp_list.addItem(item_to_add)


# ----------------------------------------------------------------------------------------------- #
if not QW.QApplication.instance():
    app = QW.QApplication(sys.argv)
else:
    app = QW.QApplication.instance()
app.setStyle(QW.QStyleFactory.create("Fusion"))
window = TheWindow()
window.show()
app.aboutToQuit.connect(app.deleteLater)
