import sys
from PyQt5 import QtWidgets
from pyQt_test import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox, QGraphicsView, QGraphicsScene
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF
import json


class RunDesigner:
    def __init__(self):
        self.now_turn = 0
        self.winner = 'WHITE'
        self.log_board = self.reading_json_file()
        ###
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        ###
        self.ui.pushButton_3.setEnabled(False)
        self.ui.actionexit.triggered.connect(self.close_GUI)
        self.ui.pushButton.pressed.connect(self.go_next)
        self.ui.pushButton_2.pressed.connect(self.go_endgame)
        self.ui.pushButton_3.pressed.connect(self.go_back)
        # graphics
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.red)
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)
        self.pen = QPen(Qt.red)
        self.ui.graphicsView.setScene(self.scene)
        self.drawGame(self.now_turn)
        self.counter(self.now_turn)
        # show
        self.MainWindow.show()
        sys.exit(app.exec_())

    def close_GUI(self):
        self.MainWindow.close()

    def go_next(self):
        # QMessageBox.question(self.MainWindow, 'PyQt5 message', "Do you like PyQt5?",
        #                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        self.scene.clear()
        self.now_turn += 1
        self.drawGame(self.now_turn)
        self.check_enabled()
        self.counter(self.now_turn)

    def go_endgame(self):
        self.scene.clear()
        self.now_turn = len(self.log_board) - 1
        self.drawGame(self.now_turn)
        self.ui.pushButton.setEnabled(False)
        self.counter(self.now_turn)
        self.check_enabled()
        msg = QMessageBox()
        msg.information(self.MainWindow, 'result', 'Winner is : ' + self.winner, QMessageBox.Ok)

    def go_back(self):
        self.scene.clear()
        self.now_turn -= 1
        self.drawGame(self.now_turn)
        self.check_enabled()
        self.counter(self.now_turn)

    def drawGame(self, turn: int):
        turn_str = 'turn'+str(turn)
        board = self.log_board[turn_str]
        for i in range(8):
            for j in range(8):
                if board[i][j] == 0:
                    brush = QBrush(Qt.green)
                elif board[i][j] == 1:
                    brush = QBrush(Qt.white)
                else :
                    brush = QBrush(Qt.black)
                self.scene.addEllipse(j*60, i*60, 50, 50, self.pen, brush)

    def reading_json_file(self):
        with open('log.json') as f:
            data_board = json.load(f)
        print(len(data_board))
        return data_board

    def check_enabled(self):
        if self.now_turn == 0:
            self.ui.pushButton_3.setEnabled(False)
        else :
            self.ui.pushButton_3.setEnabled(True)
        if self.now_turn == len(self.log_board) - 1:
            self.ui.pushButton.setEnabled(False)
        else :
            self.ui.pushButton.setEnabled(True)

    def counter(self, turn: int):
        turn_str = 'turn' + str(turn)
        board = self.log_board[turn_str]
        white_counter = 0
        black_counter = 0
        for i in board:
            for j in i:
                if j == 1:
                    white_counter += 1
                elif j == 2:
                    black_counter += 1
        if white_counter > black_counter:
            self.winner = 'WHITE'
        elif white_counter < black_counter:
            self.winner = 'BLACK'
        else :
            self.winner = 'TIE'
        self.ui.label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:white;\">"
                              + str(white_counter) + "</span></p></body></html>")
        self.ui.label_2.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:black;\">"
                              + str(black_counter) + "</span></p></body></html>")

if __name__ == "__main__":
    RunDesigner()
