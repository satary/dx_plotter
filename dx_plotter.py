# -*- coding: utf-8 -*-
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Author = Grigoriy Armeev (MSU)
'''
from PyQt4 import QtCore, QtGui
import sys,os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def readlines_reverse(filename):
    with open(filename) as qfile:
        qfile.seek(0, os.SEEK_END)
        position = qfile.tell()
        line = ''
        while position >= 0:
            qfile.seek(position)
            next_char = qfile.read(1)
            if next_char == "\n":
                yield line[::-1]
                line = ''
            else:
                line += next_char
            position -= 1
        yield line[::-1]
        
def open_dx(path):
    i=0
    step=[]
    for line in open(path,'r'):
        dict_line=line.split()
        if (dict_line[0]=='object') and (dict_line[1]=='1'):
            x=int(dict_line[5])
            y=int(dict_line[6])
            z=int(dict_line[7])
        if (dict_line[0]=='origin'):
            orig=np.array(dict_line[1:4]).astype(float)
            print orig
        if (dict_line[0]=='delta'):
            step.append(np.array(dict_line[1:4]).astype(float))
        if (dict_line[0]=='object') and (dict_line[1]=='3'):
            i+=1
            break
        i+=1
    j=0
    for line in readlines_reverse(path):
        if (line!=''):
            if line.split()[0]=='attribute':
                break
        j+=1
    step=np.sum(step,1)
    grid=np.genfromtxt(path,skip_header=i,skip_footer=j).reshape(x,y,z)
    return grid,step,orig

    
        
        

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_imageViewer(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.cmaps=['Blues', 'BuGn', 'BuPu',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd',
                             'BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                             'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                             'seismic']
        self.setupUi(self)
        self.hidden=True
        self.toogletitles()
        
        
    def setupUi(self, imageViewer):
        imageViewer.setObjectName(_fromUtf8("imageViewer"))
        imageViewer.resize(640, 800)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.load_image_btn = QtGui.QPushButton(imageViewer)
        self.load_image_btn.setObjectName(_fromUtf8("load_image_btn"))
        self.verticalLayout.addWidget(self.load_image_btn)
        
        gridlout=QtGui.QGridLayout()
        self.orient_group=QtGui.QButtonGroup(self)
        self.rx=QtGui.QRadioButton("X")
        self.rx.setChecked(True)
        self.orient_group.addButton(self.rx)
        self.orient_group.setId(self.rx,0)
        self.ry=QtGui.QRadioButton("Y")
        self.orient_group.addButton(self.ry)
        self.orient_group.setId(self.ry,2)
        self.rz=QtGui.QRadioButton("Z")
        self.orient_group.addButton(self.rz)
        self.orient_group.setId(self.rz,1)
        
        self.horisontalLayout1 = QtGui.QHBoxLayout()
        start_label = QtGui.QLabel(self)
        start_label.setText("Start Value:")
        self.start_box = QtGui.QDoubleSpinBox()
        self.start_box.setRange(-1000,1000)
        self.start_box.setDecimals(4)
        self.start_box.setValue(-3)
        
        stop_label = QtGui.QLabel(self)
        stop_label.setText("Stop Value:")
        self.stop_box = QtGui.QDoubleSpinBox()
        self.stop_box.setRange(-1000,1000)
        self.stop_box.setDecimals(4)
        self.stop_box.setValue(3)
        
        step_label = QtGui.QLabel(self)
        step_label.setText("Step Value:")
        self.step_box = QtGui.QDoubleSpinBox()
        self.step_box.setRange(0,1000)
        self.step_box.setDecimals(4)
        self.step_box.setValue(0.5)
        self.autoscale_checkbox = QtGui.QCheckBox('Autoscale', self)
        self.autoscale_checkbox.setCheckState(2)
        self.horisontalLayout1.addWidget(start_label)
        self.horisontalLayout1.addWidget(self.start_box)
        self.horisontalLayout1.addWidget(stop_label)
        self.horisontalLayout1.addWidget(self.stop_box)
        self.horisontalLayout1.addWidget(step_label)
        self.horisontalLayout1.addWidget(self.step_box)
        
        self.horisontalLayout1.addWidget(self.autoscale_checkbox)
        gridlout.addLayout(self.horisontalLayout1,1,1)
        gridlout.addWidget(self.rx,0,0)
        gridlout.addWidget(self.ry,1,0)
        gridlout.addWidget(self.rz,2,0)
        self.XSlider = QtGui.QSlider(self)
        self.XSlider.setMinimum(0)
        self.XSlider.setMaximum(100)
        self.XSlider.setOrientation(QtCore.Qt.Horizontal)
        gridlout.addWidget(self.XSlider,0,1)
        
        self.horisontalLayout2 = QtGui.QHBoxLayout()
        self.cmap_combo_box = QtGui.QComboBox(self)
        self.cmap_combo_box.addItems(self.cmaps)
        self.cmap_combo_box.setCurrentIndex(5)
        self.horisontalLayout2.addWidget(self.cmap_combo_box)
        self.contour_checkbox = QtGui.QCheckBox('Draw contours', self)
        self.contour_checkbox.setCheckState(2)
        self.horisontalLayout2.addWidget(self.contour_checkbox)
        self.colorbar_checkbox = QtGui.QCheckBox('Draw colorbar', self)
        self.colorbar_checkbox.setCheckState(2)
        self.horisontalLayout2.addWidget(self.colorbar_checkbox)
        self.origin_checkbox = QtGui.QCheckBox('Use cell origin', self)
        self.origin_checkbox.setCheckState(0)
        self.horisontalLayout2.addWidget(self.origin_checkbox)
        self.title_btn=QtGui.QPushButton()
        self.horisontalLayout2.addWidget(self.title_btn)
        gridlout.addLayout(self.horisontalLayout2,2,1)
       
        self.verticalLayout.addLayout(gridlout)
        
        gridlout1=QtGui.QGridLayout()
        
        self.verticalLayout.addLayout(gridlout1)
        self.title=QtGui.QLineEdit()
        self.title.setText(unicode('Electrostatic Potential Distribution'))
        gridlout1.addWidget(self.title,0,0)
        self.xtitle=QtGui.QLineEdit()
        self.xtitle.setText(unicode('Coordinate, A'))
        gridlout1.addWidget(self.xtitle,0,1)
        self.ytitle=QtGui.QLineEdit()
        self.ytitle.setText(unicode('Coordinate, A'))
        gridlout1.addWidget(self.ytitle,1,0)
        self.ctitle=QtGui.QLineEdit()
        self.ctitle.setText(unicode('Potential, V'))
        gridlout1.addWidget(self.ctitle,1,1)
        
        
        self.figure = plt.figure(figsize=(1,1))
        self.canvas = FigureCanvas(self.figure)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.mpl_toolbar)
        self.verticalLayout.setStretch(1, 1)
        self.retranslateUi(imageViewer)
        self.setLayout(self.verticalLayout)
        QtCore.QMetaObject.connectSlotsByName(imageViewer)

    def retranslateUi(self, imageViewer):
        imageViewer.setWindowTitle(_translate("imageViewer", "ImageViewer", None))
        self.load_image_btn.setText(_translate("imageViewer", "Open Image", None))
        self.title_btn.setText(_translate("imageViewer", "Edit titles", None))
        self.load_image_btn.clicked.connect(self.openImage)
        self.title_btn.clicked.connect(self.toogletitles)
        self.autoscale_checkbox.stateChanged.connect(self.plot_current)
        self.orient_group.buttonClicked.connect(self.change_scale)
        self.orient_group.buttonClicked.connect(self.plot_current)
        self.XSlider.valueChanged.connect(self.plot_current)
        self.cmap_combo_box.currentIndexChanged.connect(self.plot_current)
        self.start_box.valueChanged.connect(self.plot_with_values)
        self.stop_box.valueChanged.connect(self.plot_with_values)
        self.step_box.valueChanged.connect(self.plot_with_values)
        self.colorbar_checkbox.stateChanged.connect(self.plot_current)
        self.contour_checkbox.stateChanged.connect(self.plot_current)
        self.origin_checkbox.stateChanged.connect(self.plot_current)
        self.title.textChanged.connect(self.plot_current)
        self.xtitle.textChanged.connect(self.plot_current)
        self.ytitle.textChanged.connect(self.plot_current)
        self.ctitle.textChanged.connect(self.plot_current)
    


    def toogletitles(self):
        if self.hidden:
            self.title.hide()
            self.xtitle.hide()
            self.ytitle.hide()
            self.ctitle.hide()
            self.hidden=False
        else:
            self.title.show()
            self.xtitle.show()
            self.ytitle.show()
            self.ctitle.show()
            self.hidden=True
        
    def openImage(self):
        self.imagePath=QtGui.QFileDialog.getOpenFileNameAndFilter(filter="*.dx")
        if self.imagePath != "":
            print self.imagePath[0]
            self.grid,self.step,self.orig=open_dx(unicode(self.imagePath[0]))
            print self.grid.shape
            print 'File loaded'
            self.change_scale()
            self.plot_current()
    def plot_with_values(self):
        if not(self.autoscale_checkbox.isChecked()):
            self.plot_current()
    def change_scale(self):
        Z=self.grid.shape
        butid=self.orient_group.checkedId()
        self.XSlider.setMaximum(Z[butid]-1)
       
    
    def plot_current(self,event=None):
        self.plot(orient=self.orient_group.checkedId(),
                    pos=self.XSlider.value(),
                    start=self.start_box.value(),
                    stop=self.stop_box.value(),
                    step=self.step_box.value(),
                    colorbar=self.colorbar_checkbox.isChecked(),
                    contours=self.contour_checkbox.isChecked(),
                    color=str(self.cmap_combo_box.currentText()),
                    origin=self.origin_checkbox.isChecked(),
                    autoscale=self.autoscale_checkbox.isChecked(),
                    title=unicode(self.title.text()),
                    xtitle=unicode(self.xtitle.text()),
                    ytitle=unicode(self.ytitle.text()),
                    ctitle=unicode(self.ctitle.text()))
    
    def plot(self,orient=0,pos=0,color='Greys',colorbar=True,contours=True,
             start=-3,stop=3.1,step=0.5,origin=False,autoscale=False,
             title='Title',xtitle='Xtitle',ytitle='Ytitle',ctitle='colorbar'):
        try:
            if orient==0:
                Z=self.grid[pos]
                xstep=self.step[1]
                ystep=self.step[2]
                xorig=self.orig[1]
                yorig=self.orig[2]
            elif orient==1:
                Z=self.grid[:,pos,:].transpose()
                xstep=self.step[0]
                ystep=self.step[1]
                xorig=self.orig[0]
                yorig=self.orig[1]
            elif orient==2:
                Z=self.grid[:,:,pos].transpose()
                xstep=self.step[0]
                ystep=self.step[2]
                xorig=self.orig[0]
                yorig=self.orig[2]
            if autoscale:
                start = Z.min()
                stop = Z.max()
                step =(Z.max()-Z.min())/10.0-0.0001
                self.start_box.setValue(start)
                self.stop_box.setValue(stop)
                self.step_box.setValue(step)
            x=np.arange(0,Z.shape[1])*xstep
            y=np.arange(0,Z.shape[0])*ystep
            if origin:
                x+=xorig
                y+=yorig
            X, Y = np.meshgrid(x, y)
            plt.clf() 
            ax1 = self.figure.add_subplot(111)
            ax1.set_aspect('equal')
            ax1.set_title(title)
            plt.xlabel(xtitle)
            plt.ylabel(ytitle)
            lvls = np.arange(start,stop+0.000001,step) #dirty hack
            if contours:                
                CF = ax1.contourf(X,Y,Z,
                    cmap=color,
                    levels = lvls
                    )
                CS = ax1.contour(X,Y,Z,
                    colors = 'k',
                    levels = lvls
                    )
                if colorbar:
                    cbar = plt.colorbar(CF, ticks=lvls, format='%.2f',label=ctitle)
            else:
                plt.imshow(Z,cmap=color,origin='lower',vmin=start,vmax=stop,extent=[x[0],x[-1],y[0],y[-1]])
                if colorbar:
                    cbar = plt.colorbar(ticks=lvls,format='%.2f',label=ctitle)
            self.canvas.draw()
        except AttributeError:
            print "No image loded"
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Ui_imageViewer()
    main.show()

    sys.exit(app.exec_())
