#Notwendige Bibliotheken importieren
#Hier wird bestimmt noch etwas für die GPIO-Pins des RadxaRock3 benötigt
import sys
import datetime
import time
from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime, QTimer
from PyQt5 import QtCore as qtc
# Hier wird die SubKlasse der Benutzeroberfläche (UI) importiert
from RPi import GPIO
from heisserDraht_Subclass import DrahtWindow

GPIO.setmode(GPIO.BOARD)

class HWButton(qtc.QObject):

    button_press = qtc.pyqtSignal()

    def __init__(self, pin, type):
        super().__init__()
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pin = pin
        if (type == "NO"):
          self.pressed = GPIO.input(self.pin) == GPIO.HIGH
        elif (type == "NC"):
          self.pressed = GPIO.input(self.pin) == GPIO.LOW
        # Using a timer to Poll
#        self.timer24 = qtc.QTimer(interval=50, timeout=self.check)
#        self.timer24.start()

        # Using a threaded event handler
        if (type == "NO"):
          GPIO.add_event_detect(
            self.pin,
            GPIO.RISING,
            callback=self.on_event_detect)
        elif (type == "NC"):
          GPIO.add_event_detect(
            self.pin,
            GPIO.FALLING,
            callback=self.on_event_detect)

    def on_event_detect(self, *args):
        self.button_press.emit()

    def check(self):
        pressed = GPIO.input(self.pin) == GPIO.LOW
        if pressed != self.pressed:
            if pressed:
                self.button_press.emit()
            self.pressed = pressed

class HeisserDraht(DrahtWindow):

    def __init__(self, parent=None):
    #Die Initialisierung (Konstruktor in Java) für HeisserDraht. Dies wird einmal beim ersten Aufruf ausgeführt.
        super().__init__(parent)
        self.setupUi(self)
        self.sysZeit = QTime.currentTime() #Wir speichern uns einen Zeitstempel. Alles was unter "self" angelegt wird ist in der ganzen Klasse verfügbar
        self.strafzeit=1000 #Strafzeit in Millisekunden für eine Berührung festlegen
        self.label_3.setText('Eine Berührung verursacht '+ str(self.strafzeit/1000) + ' Strafsekunden!') #Hier wird der Text in der UI festgelegt. Geht auch in QtDesigner, aber sollte sich eben mit Änderung der Strafzeit ändern.
        self.timer = QTimer() #Ein neuer Timer der KLasse QTimer (Bibliothek) wird angelegt.
        self.timer.timeout.connect(self.displayzeit) #Hier wird die Methode festgelegt, die aufgerufen wird, wenn der TImer gerade abgelaufen ist. Bisher haben wir noch keine Dauer für den Timer festgelegt.
        self.beruehrungen=0 #Der Zähler der Berührungen wird initialisiert
        ###Die Methoden timer_Startet(), timer_stoppt() und beruehrung_erkannt() werden hier nicht aufgerufen, aber weiter unten definiert. Diese werden in der heisserDraht_Subclass aufgerufen, weil Tastatureingaben Teil der UI sind.
        self.startknopf = HWButton(10,"NC")
        self.startknopf.button_press.connect(self.timer_startet)
        self.readTimer = QTimer(interval=10, timeout=self.readGPIO)
        self.readTimer.start()
#        self.readTimer.timeout.connect(self.readGPIO)
        self.touchPin = 24
        GPIO.setup(self.touchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.endPin = 26
        GPIO.setup(self.endPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #    self.touchknopf = HWButton(24,"NO")
   #     self.touchknopf.button_press.connect(self.beruehrung_erkannt)
  #      self.endknopf = HWButton(26,"NO")
 #       self.endknopf.button_press.connect(self.timer_stoppt)
        self.touch_i = 0
        self.displayzeit() #Die MEthode zum Anzeigen der Werte wird einmal aufg>

    def displayzeit(self):
        if (GPIO.input(10)==GPIO.LOW):
          self.az = self.sysZeit.elapsed() + (self.beruehrungen * self.strafzeit) #Anzeigezeit berechnen aus vergangener Zeit seit GO und Anzahl der Berührungen multipliziert mit der Strafzeit
        else:
          self.az =self.sysZeit.elapsed()*0.0
        text = str(datetime.timedelta(milliseconds=self.az)) #Aus dem Zahlenwert wird ein String (Text) gemacht. datetime.timedelta(millis) wandelt millis in die Form HH:MM:SS:msms:mcsmcsmcs
        text = text[2:-4] #'HH:' und ':mcsmcsmcs' werden abgeschnitten
        self.lcdNumber.display(text) #Der gekürzte Text wird an die LED-Anzeige gesendet
        self.lcdNumber_2.display(self.beruehrungen) #Die LED-Anzeige in der UI für BErührungen wird auf den neuen Wert gesetzt.
        #print text #Um während der Laufzeit des Programms Ausgaben zu erhalten, kann print() genutzt werden. Die Ausgaben erscheinen auf der Konsole.

    def beruehrung_erkannt(self):
        self.touch_i+=1
        if self.touch_i == 1:
          self.beruehrungen=self.beruehrungen+1 #Wenn eine Berührung (b gedrückt) erkannt wurde, wird der Zähler um 1 erhöht
          self.touchtime = time.time()
        if (time.time() - self.touchtime) > .5:
          self.touch_i=0
        print(self.touch_i) #Debug-Ausgabe


    def timer_startet(self):
        self.timer.start(10) #Wenn der Startkontakt verlassen (g gedrückt) wird. Wird der Timer zum Erneuern der ANzeige mit 10 Millisekunden gestartet. Das bedeutet diplayzeit() wird alle 10 Millisekunden aufgerufen (Zeile 32).
        self.sysZeit = QTime.currentTime() #Der Startpunkt wird auf die aktuelle Systemzeit gesetzt. Von hieraus wird die anzuzeigende Zeit berechnet.
        self.beruehrungen = 0 #Die Berührugnen aus dem letzten Lauf werden auf 0 gesetzt.

    def timer_stoppt(self):
        self.timer.stop() #Der Timer wird gestoppt. Die Anzeige der UI bleibt konstant und wird nicht mehr erneuert.

    def readGPIO(self):
        if (GPIO.input(self.touchPin) == GPIO.HIGH):
          self.beruehrung_erkannt()
        if (GPIO.input(self.endPin) == GPIO.HIGH):
          self.timer_stoppt()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    hotWIre = HeisserDraht()

    hotWIre.show()

    sys.exit(app.exec())
