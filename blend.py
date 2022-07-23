# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 20:18:19 2022

@author: Mikuś
"""

import cv2
import numpy as np
import matplotlib 
import imutils
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap

#craate object from gui.ui made in qtDesigner
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("gui.ui",self)
        #intialazie empty image table and connect buttons
        self.imgs = ['', '','']
        self.broseImg.clicked.connect(self.broseImageFiles)
        self.broseWatermark.clicked.connect(self.broseWatermarkFiles)
        self.saveButton.clicked.connect(self.saveOutputFile)
        self.viewButton.clicked.connect(self.showOperation)
        #functions to chose an image file bmp, jpg or png 
    def broseImageFiles(self):
        
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/', 'Images (*.jpg),(*.bmp),(*.png)')
        self.imgs[0] = cv2.imread(fname[0])
        self.imgPath.setText(fname[0])
       
    def broseWatermarkFiles(self):
        
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/', 'Images (*.jpg),(*.bmp),(*.png)')
        self.imgs[1] = cv2.imread(fname[0])
        self.watermarkPath.setText(fname[0])
       
        
    def blendImages(self):
        #get width and height of input image
        h = self.imgs[0].shape[0]
        w = self.imgs[0].shape[1]
        #scale watermark to fit input image and scale slider position
        if h<w :
            watermark = imutils.resize(self.imgs[1], height=int(h*self.scaleSlider.value()/100))
        else:
            watermark = imutils.resize(self.imgs[1], width=int(w*self.scaleSlider.value()/100))
       
        (wH, wW) = watermark.shape[:2]
        
        #set max for spinbox h1 and w1 - value in box must be >=0
        h1 = h - wH
        w1 = w - wW
        self.positionYBox.setMaximum(h1)
        self.positionXBox.setMaximum(w1)
        #create mask for watermark 
        overlay = np.zeros((h, w, 3), dtype="uint8")
        overlay[h1 - self.positionYBox.value() :h - self.positionYBox.value(), w1 -self.positionXBox.value() :w - self.positionXBox.value()] = watermark
        #blend images with slider parameters
        self.imgs[2] = cv2.addWeighted(self.imgs[0], self.alphaSlider.value()/100, overlay, self.betaSlider.value()/100, 0)
        
    def saveOutputFile(self):        
        self.blendImages()
        cv2.imwrite('out.jpg', self.imgs[2])
        print('file saved')
    
    def showOperation(self):
        
        self.blendImages()
             
        wait_time = 10
        while 1:
            cv2.imshow("press 'q' on keyboard to close", self.imgs[2])
            self.blendImages()
            keyCode = cv2.waitKey(wait_time)
            if (keyCode & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break

    
    
#run the app        
app = QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(450)
widget.setFixedHeight(300)
widget.show()
sys.exit(app.exec_())

