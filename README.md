# heisserDraht
UI for timing and time penalties while playing on a physical "hot wire game"

#Dateien:
-heisserDraht_main.py: Die Hauptdatei des Programms. Kann noch umbenannt werden.
-heisserDraht_ui.py: In dieser Datei befindet sich die Definition der Benutzeroberfläche. Hier sollen keine direkten Änderungen vorgenommen werden, weil diese durch Änderungen in QtDesigner überschrieben werden.
-heisserDraht_Subclass.py: Diese Klasse erbt von heisserDraht_ui.py. Hier können Methoden für die Benutzeroberfläche erstellt werden, die dauerhaft Bestand haben.
-Im Ordner "LED_Design" finden sich die Dateien, um die Benutzeroberfläche mit QtDesigner zu egstalten. Die .ui-Datei kann mit pyuic5 in Python-Code übersetzt werden: https://pythonbasics.org/qt-designer-python/
