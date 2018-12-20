#!/usr/bin/python3
# -*- coding: utf-8 -*-

from editor import QCodeEditor
from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QAction, QTabWidget,
                             QVBoxLayout, QWidget, QFileDialog)
import Interpret as Ipt
from stackdisp import StackDisplayer
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create menu bar
        compileAct = QAction('&Compile', self)
        compileAct.setShortcut('Ctrl+C')
        compileAct.setStatusTip('Compile the program')
        compileAct.triggered.connect(self.compile)
        runAct = QAction('&Run', self)
        runAct.setShortcut('Ctrl+R')
        runAct.setStatusTip('Run the program')
        runAct.triggered.connect(self.run)
        debugAct = QAction('&Debug', self)
        debugAct.setShortcut('Ctrl+D')
        debugAct.setStatusTip('Debug the program')
        debugAct.triggered.connect(self.debug)
        fileAct = QAction('&Open file', self)
        fileAct.setShortcut('Ctrl+F')
        fileAct.setStatusTip('Choose file')
        fileAct.triggered.connect(self.chooseFile)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(fileAct)
        runMenu = menubar.addMenu('&Run')
        runMenu.addAction(compileAct)
        runMenu.addAction(runAct)
        runMenu.addAction(debugAct)

        # Set style
        self.setStyleSheet("QMainWindow{\
                                background:rgb(43, 43, 43);\
                            }\
                            QMenuBar{\
                                background:rgb(43, 43, 43);\
                                color:rgb(163, 163, 163);\
                            }\
                            QMenuBar::item:selected{\
                                background-color:rgb(75,110,175);\
                            }\
                            QMenu{\
                                background-color:rgb(43, 43, 43);\
                            }\
                            QMenu::item{\
                                color:rgb(163, 163, 163);\
                                background-color:rgb(50, 50, 50);\
                            }\
                            QMenu::item:selected{\
                                background-color:rgb(75,110,175);\
                            }\
                            QStatusBar{\
                                color:rgb(163, 163, 163);\
                            }")

        self.GUI = GUI()
        self.setCentralWidget(self.GUI)
        self.resize(1200, 800)
        self.center()
        self.statusBar()
        self.setWindowTitle('X0-Compiler')

    # centers the window on the screen
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def compile(self):
        self.GUI.output.setPlainText('Compiling with X0-Compiler\n')
        self.GUI.isDebug = 0

        # write the content of code editor into input.txt
        import os
        if not os.path.exists('./data'):
            os.makedirs('./data')
        with open("./data/input.txt", "w") as file:
            file.write(self.GUI.codeEdit.toPlainText())

        # invoke X0-Compiler.exe to produce intermediate code and load it.
        process = subprocess.Popen("X0-Compiler.exe", stdout=subprocess.PIPE)
        process.wait()
        Ipt.loadData()

        # display intermediate code
        fctCodeString = ["lit", "opr", "lod", "sto", "cal", "ini", "jmp", "jpc", "add", "sub", "tad"]
        s = ""
        for i in range(Ipt.codeNum):
            temp = Ipt.code[i]
            if temp.fct == 0 and temp.opr2 != 0:
                s = s + '%s %s %s\n' % (fctCodeString[temp.fct], temp.opr1, round(temp.opr2, 2))
            else:
                s = s + '%s %s %s\n' % (fctCodeString[temp.fct], temp.opr1, int(temp.opr2))
        self.GUI.INTCode.setPlainText(s.strip())

        self.GUI.output.appendPlainText('Compiled successfully!\n')

    def run(self):
        self.GUI.output.appendPlainText('Output of your program:')
        Ipt.interpretAllStep(self.GUI.output)

    def debug(self):
        if self.GUI.isDebug == 0:
            self.GUI.isDebug = 1
            self.GUI.stackDisplayer.update()
            self.GUI.output.appendPlainText('Output of your program:')
        else:
            Ipt.interpretOneStep(self.GUI.output)
            self.GUI.stackDisplayer.update()

    def chooseFile(self):
        filePath, _ = QFileDialog.getOpenFileName(None, "Choose file",
                                                  "C:/",
                                                  "All Files (*);;Text Files (*.txt)")
        if filePath == "":
            return
        s = ""
        with open(filePath, "r") as file:
            lines = file.readlines()
            for line in lines:
                s = s + line
        self.GUI.codeEdit.setPlainText(s)

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.isDebug = 0

        # Add code editor
        self.codeEdit = QCodeEditor(self)
        self.codeEdit.setStyleSheet("color:rgb(163, 163, 163);\
                                     background:rgb(43, 43, 43);\
                                     font-family:Consolas;\
                                     font-size:10pt")
        tabWidth = 4 * self.codeEdit.fontMetrics().width(' ')
        self.codeEdit.setTabStopWidth(tabWidth)

        # Add output displayer
        self.output = QCodeEditor(self)
        self.output.setStyleSheet("color:rgb(163, 163, 163);\
                                   background:rgb(43, 43, 43);\
                                   font-family:Consolas;\
                                   font-size:10pt;")
        self.output.setReadOnly(1)

        # Add intermediate code displayer
        self.INTCode = QCodeEditor(self)
        self.INTCode.setStyleSheet("color:rgb(163, 163, 163);\
                                    background:rgb(43, 43, 43);\
                                    font-family:Consolas;\
                                    font-size:10pt;")
        self.INTCode.setReadOnly(1)

        # Add data stack displayer
        self.stackDisplayer = StackDisplayer(self)
        self.stackDisplayer.setStyleSheet("background:rgb(43, 43, 43);")


        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.output, "Output")
        self.tabWidget.addTab(self.INTCode, "Intermediate code")
        self.tabWidget.addTab(self.stackDisplayer, "Data stack")
        self.tabWidget.setStyleSheet("QTabWidget::pane{\
                                        background-color:rgb(43, 43, 43);\
                                      }\
                                      QTabBar::tab{\
                                        min-width:100px;\
                                        min-height:25px;\
                                        font:15px consolas;\
                                      }\
                                      QTabBar::tab:!selected{\
                                        color:rgb(163, 163, 163);\
                                        background:rgb(43, 43, 43)\
                                      }\
                                      QTabBar::tab:selected{\
                                        color:rgb(163, 163, 163);\
                                        background:rgb(70, 70, 70)\
                                      }")

        vbox = QVBoxLayout()
        vbox.addWidget(self.codeEdit)
        vbox.addWidget(self.tabWidget)
        self.setLayout(vbox)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
