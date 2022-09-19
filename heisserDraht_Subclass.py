from heisserDraht_ui import Ui_mw_draht
from PyQt5.QtWidgets import QMainWindow
#import RPi.GPIO as GPIO

class DrahtWindow(QMainWindow, Ui_mw_draht):
#    def test_event(self, *args):
 #       print("Beruehrung")
  #      self.timer_startet()

    def __init__(self, parent=None):
        super(DrahtWindow, self).__init__(parent)
        self.setupUi(self)
   #     GPIO.setmode(GPIO.BOARD)
    #    GPIO.setup(7, GPIO.IN)
     #   GPIO.add_event_detect(7, GPIO.RISING, self.test_event, bouncetime=500)

    def keyPressEvent(self, event):
        # implement the method here
        #print(event.key())
        if event.key() == 66: # 66 ist ASCII-Code für b
            self.beruehrung_erkannt()
        if event.key() == 71:
            self.timer_startet()
        if event.key() == 83:
            self.timer_stoppt()

