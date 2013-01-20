'''
Created on 20-01-2013

@author: W
'''
import os, sys
from nussinov import Nussinov
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MainWindow(QtGui.QWidget):
        
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.setGeometry(0,0, 800,650)
        self.setWindowTitle("Nussinov")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.resize(800,650)
        self.setMinimumSize(600,420)
        self.center()
        
        # --- Actions --- #
        openAction = QtGui.QAction("&Open", self)
        openAction.setShortcut( QKeySequence.Open)
        openAction.triggered.connect(self.showOpenFileDialog)
        
        saveAction = QtGui.QAction("&Save", self)
        saveAction.setShortcuts(QKeySequence.Save)
        saveAction.triggered.connect(self.showSaveFileDialog)
        
        exitAction = QtGui.QAction("E&xit", self)
        exitAction.setShortcuts(QKeySequence(self.tr("Ctrl+X,Ctrl+x")))
        exitAction.triggered.connect(QtGui.qApp.quit)
        # --- Menu Run --- #
        runAction = QtGui.QAction("Run", self)
        runAction.setShortcut(QKeySequence(self.tr("F5")))
        runAction.triggered.connect(self.RunAlgorithm)
        
        menu_bar = QtGui.QMenuBar()
        fileMenuBar = menu_bar.addMenu("&File")
        runMenuBar = menu_bar.addMenu("&Run") 
        
        fileMenuBar.addAction(openAction)
        fileMenuBar.addAction(saveAction)
        fileMenuBar.addAction(exitAction)
        runMenuBar.addAction(runAction)
        
        
        # --- Text Box and RunButton --- #
        self.RnaCodeTextEdit = QtGui.QTextEdit()
        self.RnaCodeTextEdit.setGeometry(50,50,500,80)
        self.RnaCodeTextEdit.setMaximumHeight(100)
        
        RnaCodeLabel = QtGui.QLabel()
        RnaCodeLabel.setText(self.tr("Rna code:"))
        RnaCodeLabel.setAlignment(Qt.AlignLeft)
        RnaCodeLabel.setFont(QFont("Times", 12))        
      
        vbox = QtGui.QVBoxLayout()
        RnaCodeHLayout  =QtGui.QHBoxLayout()
        vbox.addWidget(menu_bar)
        vbox.addWidget(RnaCodeLabel)
        vbox.addLayout(RnaCodeHLayout)
        
        RnaCodeHLayout.addWidget(self.RnaCodeTextEdit)
        runButton = QtGui.QPushButton()
        runButton.setText(self.tr("Run"))
        runButton.setMaximumSize(50, 50)
        self.ResultTabView = QtGui.QTableWidget(1,2)
        
        QObject.connect(runButton, SIGNAL("clicked()"), self.RunAlgorithm)
        RnaCodeHLayout.addSpacing(20)
        RnaCodeHLayout.addWidget(runButton)
        RnaCodeHLayout.addSpacing(20)
        
        vbox.addSpacing(40)
        ResultLabel = QtGui.QLabel(self.tr("Result"))
        ResultLabel.setAlignment(Qt.AlignCenter)
        ResultLabel.setFont(QFont("Times", 12))
        vbox.addWidget(ResultLabel)
        ResultsLayout = QtGui.QHBoxLayout()
        
        ResultTabHeaders = QStringList( self.tr("Rna Code"))
        ResultTabHeaders.append(self.tr("Result"))
        self.ResultTabView.setHorizontalHeaderLabels(ResultTabHeaders)
        ResultsLayout.addWidget(self.ResultTabView)
        #ResultsLayout.addWidget(ResultTabView2)
        vbox.addLayout(ResultsLayout)        
        
        self.setLayout(vbox)
        
        
    def showOpenFileDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            self.RnaCodeTextEdit.setText(data) 
            
    def showSaveFileDialog(self):

        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 
                '/home')
        
        f = open(fname, 'w')
        
        text = ""        
        with f:
            #self.ResultTabView.   
            for row in range(self.ResultTabView.rowCount()):
                item1 = self.ResultTabView.item(row,0)
                item2 = self.ResultTabView.item(row,1)
                text += item1.text() + item2.text()
            f.write((text))
            f.close()
            
    def RunAlgorithm(self):
        i = 0
        text = self.RnaCodeTextEdit.toPlainText()
        TextList = text.split(QRegExp("\\s+"))
        if TextList.count() -1 == 0 :
            msgBox = QMessageBox()
            msgBox.setText("Can't run algorithm without data!")
            msgBox.exec_()
            return
        self.ResultTabView.setRowCount(TextList.count())
        for line in TextList:
            nuss = Nussinov(line)
            ret = nuss.compute()
            item1 = QTableWidgetItem(line)
            item2 = QTableWidgetItem(QString(("%s\n" % (ret)) ))
            self.ResultTabView.setItem(i,0,item1)
            self.ResultTabView.setItem(i,1,item2)
            i = i + 1
            #self.ResultTabView. .write("%s %s\n" % (len(ret), ret))
        self.ResultTabView.resizeColumnsToContents()
        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


app = QtGui.QApplication(sys.argv)
frame = MainWindow()
frame.show()
sys.exit(app.exec_())  