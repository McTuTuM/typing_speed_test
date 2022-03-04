from PyQt5 import QtWidgets, QtCore
from typing_speed_test_gui import Ui_MainWindow
import random, time, difflib, threading
from creator_wiki_sentence import CreatorSent


class Window(Ui_MainWindow, QtWidgets.QMainWindow):
    sig = QtCore.pyqtSignal()
    sig_time = QtCore.pyqtSignal(str)
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.pas)
        self.sig.connect(self.compl)
        self.sig_time.connect(self.real_time)
        self.pushButton_2.setEnabled(False)
        self.rest = False
        self.first = True

    def start(self):
        self.rest = False + 2
        self.show_sentence()
        threading.Thread(target=self.equal, daemon=True).start()
        self.lineEdit.setEnabled(True)
        self.pushButton.setEnabled(False)


    def real_time(self, times):
        self.pushButton.setEnabled(False)
        time = float(times)
        m = 0
        if time > 60:
            m = int(time // 60)
            s = int(time - m * 60 )
            if m < 10:
                self.label_time_res.setText(f'0{m}:{s}')
            else:
                self.label_time_res.setText(f'{m}:{s}')
        else:
            s = time
            if s < 10:
                self.label_time_res.setText(f'0{s}')
            else:
                self.label_time_res.setText(f'{s}')
        # self.label_time_res.setText(time)
        try:
            self.label_wpm_res.setText(str(round((len(self.lineEdit.text()[:-1]) * 60 )/ (float(times)), 2)))
        except ZeroDivisionError:
            self.label_wpm_res.setText('0')
        acc = difflib.SequenceMatcher(None,self.label_2.text()[:len(self.label_2.text())], self.lineEdit.text())
        a = int(acc.ratio() * 100)
        self.progressBar.setValue(a)

    def show_sentence(self):
        step = 0
        length_line = 70
        line_compl = ''
        line = CreatorSent.text_get()
        try:
            line_compl += line[:length_line] 
            for i in range(length_line, len(line), length_line):
                step = 0
                while line[i + step] != " ":
                    step += 1
                line_compl += line[i: i + step ] + '\n'
                line_compl += line[i + step + 1:i + length_line]
        except IndexError:
            line_compl += line[i:]
        self.label_2.setText(line_compl)
    
    def pas(self):
        self.rest = True
        self.pushButton_2.setEnabled(False)
        self.pushButton.setEnabled(True)


    def compl(self):
        self.lineEdit.setDisabled(True)
        self.pushButton.setText("Повторить")
        self.lineEdit.setText('')


    def equal(self):
        while True:
            self.pushButton_2.setEnabled(True)
            start_time = time.time()
            while len(self.label_2.text()) > len(self.lineEdit.text()):
                times = str(round(time.time() - start_time, 1))
                self.sig_time.emit(times)
                time.sleep(0.1)
                if self.rest == True:
                    break
            else:
                self.sig_time.emit(times)
            self.sig.emit()

            return
        
