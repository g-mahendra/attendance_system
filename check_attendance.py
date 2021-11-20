from PyQt4 import QtGui,QtCore
import mysql.connector
import datetime

class CheckAttendance(QtGui.QMainWindow):
    def __init__(self,sub, year):
        self.subject=sub
        self.year = year
        print(self.subject, self.year)
        super(CheckAttendance, self).__init__()
        self.setGeometry(300,50,800,600)
        self.setWindowTitle("Check Attendance")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))

        #Heading
        h=QtGui.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(250,20,300,40))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font=QtGui.QFont("Times",16,QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("CHECK ATTENDANCE")

        #Label and Date Entry Spinbox
        l2=QtGui.QLabel(self)
        l2.setAlignment(QtCore.Qt.AlignCenter)
        l2.setGeometry(QtCore.QRect(230,100,80,30))
        l2.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        font1=QtGui.QFont("Times",14,QtGui.QFont.Bold)
        l2.setFont(font1)
        l2.setText("DATE")

        self.dd=QtGui.QSpinBox(self)
        self.dd.setAlignment(QtCore.Qt.AlignCenter)
        self.dd.setGeometry(330,100,50,30)
        self.dd.setFont(font1)
        self.dd.setRange(1,31)
        self.dd.setValue(datetime.date.today().day)

        self.mm=QtGui.QSpinBox(self)
        self.mm.setAlignment(QtCore.Qt.AlignCenter)
        self.mm.setGeometry(380,100,50,30)
        self.mm.setFont(font1)
        self.mm.setRange(1,12)
        self.mm.setValue(datetime.date.today().month)

        self.yyyy=QtGui.QSpinBox(self)
        self.yyyy.setGeometry(430,100,70,30)
        self.yyyy.setFont(font1)
        self.yyyy.setRange(2014,2050)
        self.yyyy.setValue(datetime.date.today().year)

        #Go Button to check specific Date's Attendance
        b=QtGui.QPushButton(self)
        b.setText("GO!")
        b.setFont(font1)
        b.setGeometry(510,100,60,30)
        b.setStyleSheet("QPushButton { background-color : green;color : white ; }")
        b.clicked.connect(self.show_database)
        
        #Text Area To display database
        self.text=QtGui.QTextEdit(self)
        self.text.setGeometry(40,170,720,350)
        self.text.setFont(font1)

        self.text.insertPlainText('Roll\Attendance Status\tName\n')

    def show_database(self):
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="6989",
                database="attendance"
            )
        mycursor = mydb.cursor()
        #To display attendance on specific date 
        date= str(self.dd.value()) + "/" + str(self.mm.value()) + "/" + str(self.yyyy.value())
        self.text.clear()
        temp = 'Roll\t'+date+"\tName"
        self.text.insertPlainText(temp+'\n')
        
        query='SELECT Roll, Name FROM Year{}'.format(self.year)
        mycursor.execute(query)
        rolls = []
        names = []
        res = mycursor.fetchall()
        for row in res:
            rolls.append(row[0])
            names.append(row[1])
                         
        for i in range(len(rolls)):
            query='SELECT Status  FROM {} where Date = "{}" and Roll = {}'.format(self.subject, date, '\'"{}"\''.format(rolls[i]))
            print (query)
            res = []
            try:
                mycursor.execute(query)
                res = mycursor.fetchall()
                print(res)
            except mysql.connector.DatabaseError as e:
                print(F"Accured Error: {e}")

            temp = str(rolls[i])+'\t'
            for row in res:
                print(row)
                temp += (row[0])
                temp+="\t"
            temp += str(names[i])
            self.text.insertPlainText(temp+'\n')
            
if __name__ == '__main__':
    app = QtGui.QApplication([])
    gui = CheckAttendance()
    gui.show()
    app.exec_()
    c.close()
    conn.close()

