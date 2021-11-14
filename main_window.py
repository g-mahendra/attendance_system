from PyQt4 import QtGui,QtCore
from registration_window import RegistrationWindow
from attendance_window import AttendanceWindow

class MainWindow(QtGui.QMainWindow):
    #Main Window of Interface
    def __init__(self):
        super(MainWindow, self).__init__()
        self._registration_window = None
        self._attendance_window = None
        self.setGeometry(300,50,800,600)
        self.setWindowTitle("Automated Attendance System")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))

        #Heading
        h=QtGui.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(70,30,630,80))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font=QtGui.QFont("Times",20,QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("AUTOMATED ATTENDANCE SYSTEM")
        h.setStyleSheet("color:white;""border-style: solid;"
                             "border-width: 5px;"
                             "border-color: #000;"
                             "background-color : blue;")

        #Registration Button for opening registration window
        b1=QtGui.QPushButton(self)
        b1.setText("REGISTRATION")
        font1=QtGui.QFont("Times",16,QtGui.QFont.Bold)
        b1.setFont(font1)
        b1.setGeometry(420,200,230,50)
        b1.setStyleSheet("QPushButton { background-color : #DDD;color :black ; }")
        b1.clicked.connect(self.create_registration_window)

        #Attendance Button for opening attendance window
        b2=QtGui.QPushButton(self)
        b2.setText("ATTENDANCE")
        b2.setFont(font1)
        b2.setGeometry(420,350,230,50)
        b2.setStyleSheet("QPushButton { background-color : #DDD;color :black ; }")
        b2.clicked.connect(self.create_attendance_window)    

        #Adding Logo of college 
        pic =QtGui.QLabel(self)
        pic.setGeometry(80,150,230,300)
        pic.setPixmap(QtGui.QPixmap("other_images/logo1.png"))
        pic.setStyleSheet("border-style: solid;"
                             "border-width: 3px;"
                             "border-color: #000;"
                             )

    def create_registration_window(self):
        #Function for opening Registration window
        self._registration_window = RegistrationWindow()
        self._registration_window.show()
        self.close()
        
    def create_attendance_window(self):
        #Function for opening Attendance window
        self._attendance_window = AttendanceWindow()
        self._attendance_window.show()
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    gui = MainWindow()
    gui.show()
    app.exec_()
