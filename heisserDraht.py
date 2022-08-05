#Notwendige Bibliotheken importieren
#Hier wird bestimmt noch etwas für die GPIO-Pins des RadxaRock3 benötigt
import sys
import datetime

from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime, QTimer
# Hier wird die SubKlasse der Benutzeroberfläche (UI) importiert
from heisserDraht_Subclass import DrahtWindow


class HeisserDraht(DrahtWindow):

    def __init__(self, parent=None):
    #Die Initialisierung (Konstruktor in Java) für HeisserDraht. Dies wird einmal beim ersten Aufruf ausgeführt.
        super().__init__(parent)

        self.setupUi(self)

        self.sysZeit = QTime.currentTime() #Wir speichern uns einen Zeitstempel. Alles was unter "self" angelegt wird ist in der ganzen Klasse verfügbar

        self.strafzeit=2000#Strafzeit in Millisekunden für eine Berührung festlegen
        self.label_3.setText('Eine Berührung verursacht '+ str(self.strafzeit/1000) + ' Strafsekunden!') #Hier wird der Text in der UI festgelegt. Geht auch in QtDesigner, aber sollte sich eben mit Änderung der Strafzeit ändern.

        self.timer = QTimer() #Ein neuer Timer der KLasse QTimer (Bibliothek) wird angelegt.
        self.timer.timeout.connect(self.displayzeit) #Hier wird die Methode festgelegt, die aufgerufen wird, wenn der TImer gerade abgelaufen ist. Bisher haben wir noch keine Dauer für den Timer festgelegt.

        self.beruehrungen=0 #Der Zähler der Berührungen wird initialisiert
        self.displayzeit() #Die MEthode zum Anzeigen der Werte wird einmal aufgerufen.
        ###Die Methoden timer_Startet(), timer_stoppt() und beruehrung_erkannt() werden hier nicht aufgerufen, aber weiter unten definiert. Diese werden in der heisserDraht_Subclass aufgerufen, weil Tastatureingaben Teil der UI sind.


    def displayzeit(self):

        self.az = self.sysZeit.elapsed() + (self.beruehrungen * self.strafzeit) #Anzeigezeit berechnen aus vergangener Zeit seit GO und Anzahl der Berührungen multipliziert mit der Strafzeit
        text = str(datetime.timedelta(milliseconds=self.az)) #Aus dem Zahlenwert wird ein String (Text) gemacht. datetime.timedelta(millis) wandelt millis in die Form HH:MM:SS:msms:mcsmcsmcs
        text = text[2:-4] #'HH:' und ':mcsmcsmcs' werden abgeschnitten
        self.lcdNumber.display(text)#Der gekürzte Text wird an die LED-Anzeige gesendet
        self.lcdNumber_2.display(self.beruehrungen) #Die LED-Anzeige in der UI für BErührungen wird auf den neuen Wert gesetzt.
        #print text #Um während der Laufzeit des Programms Ausgaben zu erhalten, kann print() genutzt werden. Die Ausgaben erscheinen auf der Konsole.

    def beruehrung_erkannt(self):
        self.beruehrungen=self.beruehrungen+1 #Wenn eine Berührung (b gedrückt) erkannt wurde, wird der Zähler um 1 erhöht
        #print(self.beruehrungen) #Debug-Ausgabe


    def timer_startet(self):
        self.timer.start(10) #Wenn der Startkontakt verlassen (g gedrückt) wird. Wird der Timer zum Erneuern der ANzeige mit 10 Millisekunden gestartet. Das bedeutet diplayzeit() wird alle 10 Millisekunden aufgerufen (Zeile 32).
        self.sysZeit = QTime.currentTime() #Der Startpunkt wird auf die aktuelle Systemzeit gesetzt. Von hieraus wird die anzuzeigende Zeit berechnet.
        self.beruehrungen = 0 #Die Berührugnen aus dem letzten Lauf werden auf 0 gesetzt.

    def timer_stoppt(self):
        self.timer.stop() #Der Timer wird gestoppt. Die Anzeige der UI bleibt konstant und wird nicht mehr erneuert.


if __name__ == "__main__":

    app = QApplication(sys.argv)

    hotWIre = HeisserDraht()

    hotWIre.show()

    sys.exit(app.exec())
