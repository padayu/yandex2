from PyQt5 import uic

import sys

import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, \
     QTableWidgetItem, QTableWidget, QFileDialog, QPushButton, QMainWindow, QDialog, \
     QMessageBox, QStatusBar

from PyQt5 import QtCore, QtGui, QtWidgets


class window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        
        self.fname = "coffee.sqlite"
                
        self.con = sqlite3.connect(self.fname)
        
        self.cur = self.con.cursor()        
        
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["ID", 
                                                    "Название сорта", 
                                                    "Степень обжарки", 
                                                    "Молотый/в зернах", 
                                                    "Описание вкуса",
                                                    "цена",
                                                    "объем упаковки"])  
        
        res = self.cur.execute("""
        SELECT * FROM coffee
        """).fetchall()
        lr = len(res)
        self.tableWidget.setRowCount(lr)
        for i in range(lr):
            for j in range(7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(res[i][j])))    
        self.tableWidget.resizeColumnsToContents()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())