from PyQt5 import uic

import sys

import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, \
     QTableWidgetItem, QTableWidget, QFileDialog, QPushButton, QMainWindow, QDialog, \
     QMessageBox, QStatusBar
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QPoint, Qt

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
        
        self.update()
        
        self.pushButton.clicked.connect(self.openaddform)
        self.pushButton_2.clicked.connect(self.openredform)
        
    def openaddform(self):
        form.mode = 0
        form.clear()
        form.show()
        
    def openredform(self):
        self.statusBar.clearMessage()
        if len(self.tableWidget.selectedItems()) != 1:
            self.statusBar.showMessage("Пожауйста, выберите одно поле")
        else:
            form.mode = 1
            form.clear()
            form.setvalues()
            form.show()
            
    def update(self):
        res = self.cur.execute("""
        SELECT * FROM coffee
        """).fetchall()
        lr = len(res)
        self.tableWidget.setRowCount(lr)
        for i in range(lr):
            for j in range(7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(res[i][j])))    
        self.tableWidget.resizeColumnsToContents()        
        

class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.statusbar = QStatusBar(self)
        self.statusbar.move(0, 420)
        self.statusbar.resize(494, 20)   
        
        self.comboBox.addItem("Молотый")
        self.comboBox.addItem("В зернах")
        
        self.pushButton.clicked.connect(self.coffee)
        
        self.mode = 0
        
    def clear(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        
    def coffee(self):
        if self.mode == 0:
            if self.lineEdit.text():
                try:
                    name = self.lineEdit.text()
                    degree = self.lineEdit_2.text()
                    bg = self.comboBox.currentText()
                    desc = self.lineEdit_3.text()
                    price = int(self.lineEdit_4.text())
                    vol = int(self.lineEdit_5.text())
                    win.cur.execute(f"""
                    INSERT INTO coffee(name, degree, bg, description, price, volume) 
                    VALUES('{name}', '{degree}', '{bg}', '{desc}', {price}, {vol})
                    """)
                    win.con.commit()
                    self.statusbar.clearMessage()
                    win.update()
                    self.close()                    
                except Exception:
                    self.statusbar.showMessage("Неправильный формат ввода")
        elif self.mode == 1:
            if self.lineEdit.text():
                try:
                    cid = int(self.row[0].text())
                    name = self.lineEdit.text()
                    degree = self.lineEdit_2.text()
                    bg = self.comboBox.currentText()
                    desc = self.lineEdit_3.text()
                    price = int(self.lineEdit_4.text())
                    vol = int(self.lineEdit_5.text())
                    win.cur.execute(f"""
                    UPDATE coffee
                    SET name = '{name}'
                    WHERE id = {cid}
                    """)
                    win.cur.execute(f"""
                    UPDATE coffee
                    SET degree = '{degree}'
                    WHERE id = {cid}
                    """)
                    win.cur.execute(f"""
                    UPDATE coffee
                    SET bg = '{bg}'
                    WHERE id = {cid}
                    """)
                    win.cur.execute(f"""
                    UPDATE coffee
                    SET description = '{desc}'
                    WHERE id = {cid}
                    """)
                    win.cur.execute(f"""
                    UPDATE coffee
                    SET price = {price}
                    WHERE id = {cid}
                    """)
                    win.cur.execute(f"""
                    UPDATE coffee
                    SET volume = {vol}
                    WHERE id = {cid}
                    """)
                    win.con.commit()
                    self.statusbar.clearMessage()
                    win.update()
                    self.close()                    
                except Exception as error:
                    self.statusbar.showMessage("Неправильный формат ввода")
                    print(error)
        
    def setvalues(self):
        self.row = []
        rn = win.tableWidget.selectedItems()[0].row()
        for i in range(7):
            self.row.append(win.tableWidget.item(rn, i))
        self.lineEdit.setText(self.row[1].text())
        self.lineEdit_2.setText(self.row[2].text())
        self.lineEdit_3.setText(self.row[4].text())
        self.lineEdit_4.setText(self.row[5].text())
        self.lineEdit_5.setText(self.row[6].text())
        if self.row[3].text() == "Молотый":
            self.comboBox.setCurrentIndex(0)
        else:
            self.comboBox.setCurrentIndex(1)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    win.show()
    form = Form()
    sys.exit(app.exec())