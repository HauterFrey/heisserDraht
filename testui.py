import sys
import datetime


from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime, QTimer


from heisserDraht_Subclass import DrahtWindow


class Window(DrahtWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.sysZeit = QTime.currentTime()
        #print(sysZeit.toString('ss:msms'))
        self.strafzeit=2000#2000 MilliSekunden Strafzeit
        self.label_3.setText('Eine Berührung verursacht '+ str(self.strafzeit/1000) + ' Strafsekunden!')
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayzeit)
        #self.timer.start(10)
        #self.lcdNumber.display(5)
        self.beruehrungen=0
        self.lcdNumber_2.display(self.beruehrungen)
        self.displayzeit()


          #def connectSignalsSlots(self):

     #   self.action_Exit.triggered.connect(self.close)

      #  self.action_About.triggered.connect(self.about)
    def displayzeit(self):
        #zeit = self.lcdnumber
        #strafe = self.lcdnumber2
        self.az = self.sysZeit.elapsed() + (self.beruehrungen * self.strafzeit)
        text = str(datetime.timedelta(milliseconds=self.az))
        text = text[2:-4]
        self.lcdNumber.display(text)
        self.lcdNumber_2.display(self.beruehrungen)
        #print(text)

    def beruehrung_erkannt(self):#Wenn Buchstabe "b" gesendet wird. Muss wahrscheinlich als Signal in QT aktiviert werden. https://stackoverflow.com/questions/18417384/generating-keypressevent-in-a-code-generated-by-pyqt-designer
        self.beruehrungen=self.beruehrungen+1
        #print(self.beruehrungen)


    def timer_startet(self):
        self.timer.start(10)
        self.sysZeit = QTime.currentTime()
        self.beruehrungen = 0

    def timer_stoppt(self):
        self.timer.stop()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
