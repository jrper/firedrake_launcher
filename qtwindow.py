import sys
from qtpy.QtWidgets import QMainWindow, QPushButton, QApplication
import jfiredrake

class MyWindow(QMainWindow):

    def __init__(self, app, parent=None):
        super(MyWindow, self).__init__(parent)

        button = QPushButton("Launch Firedrake")
        button.clicked.connect(self.on_button_clicked)
        self.setCentralWidget(button)
        button.show()

        self.app = app
        self.cont = None

    def on_button_clicked(self):
        if not self.cont:
            print("Launching Jupyter Firedrake")
            self.cont, self.port = jfiredrake.start_instance()
        jfiredrake.open_browser(self.cont, self.port)

    def quit(self):
        if self.cont:
            self.cont.stop()
            self.cont.remove()
            self.cont = None
        self.app.exit()


# Create the Qt Application
app = QApplication(sys.argv)
win = MyWindow(app)
win.show()


# Run the main Qt loop
app.exec_()
