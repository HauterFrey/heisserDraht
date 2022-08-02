from heisserDraht_ui import Ui_mw_draht
from PyQt5.QtWidgets import QMainWindow

class DrahtWindow(QMainWindow, Ui_mw_draht):
    def __init__(self, parent=None):
        super(DrahtWindow, self).__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, event):
        # implement the method here
        #print(event.key())
        if event.key() == 66: # 66 ist ASCII-Code für b
            self.beruehrung_erkannt()
        if event.key() == 71:
            self.timer_startet()
        if event.key() == 83:
            self.timer_stoppt()


