from PyQt5 import QtWidgets, QtCore
from typing_speed_test_gui import Ui_MainWindow
import random, time, difflib, threading



class Window(Ui_MainWindow, QtWidgets.QMainWindow):
    sig = QtCore.pyqtSignal()
    sig_time = QtCore.pyqtSignal(str)
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.sig.connect(self.compl)
        self.sig_time.connect(self.real_time)
        self.new = True
        self.rest = False

    def start(self):
        self.show_sentence()
        threading.Thread(target=self.equal, daemon=True).start()
        self.lineEdit.setEnabled(True)

    def real_time(self, time):
        self.label_time_res.setText(time)
        try:
            self.label_wpm_res.setText(str(round((len(self.lineEdit.text()[:-1]) * 60 )/ (float(self.label_time_res.text())), 2)))
        except ZeroDivisionError:
            self.label_wpm_res.setText('0')
        acc = difflib.SequenceMatcher(None,self.label_2.text()[:len(self.label_2.text())], self.lineEdit.text())
        a = int(acc.ratio() * 100)
        self.progressBar.setValue(a)

    def show_sentence(self):
        step = 0
        length_text = 70
        line1 = ''
        with open('НаборПредложений.txt', 'r', encoding='UTF-8') as file:
            lines = file.readlines()
        line = random.choice(lines)[:-1]
        try:
            line1 += line[:length_text] 
            for i in range(length_text, len(line), length_text):
                step = 0
                while line[i + step] != " ":
                    step += 1
                line1 += line[i: i + step ] + '\n'
                line1 += line[i + step + 1:i + length_text]
        except IndexError:
            line1 += line[i:]
        self.label_2.setText(line1)

    def compl(self):
        self.lineEdit.setDisabled(True)
        self.pushButton.setText("Повторить")
        self.lineEdit.setText('')


    def equal(self):
        while True:
            start_time = time.time()
            while len(self.label_2.text()) > len(self.lineEdit.text()):
                times = str(round(time.time() - start_time, 1))
                self.sig_time.emit(times)
                time.sleep(0.1)
            else:
                self.sig_time.emit(times)
            self.sig.emit()
            return
        
