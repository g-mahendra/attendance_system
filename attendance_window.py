import cv2
import numpy as np
import os
import time
from PIL import Image
import shutil
import sqlite3
from datetime import date, datetime

from check_attendance import CheckAttendance
from PyQt4 import QtGui,QtCore

import mysql.connector

conn=sqlite3.connect('Attendance System.db')
c=conn.cursor()

class AttendanceWindow(QtGui.QMainWindow):
    #Attendance Window
    def __init__(self):
        super(AttendanceWindow, self).__init__()
        self.setGeometry(300,50,800,600)
        self.setWindowTitle("Attendance")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))

        #Heading
        h=QtGui.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(200,40,400,80))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font=QtGui.QFont("Times",20,QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("ATTENDANCE")
        h.setStyleSheet("color:white;""border-style: solid;"
                             "border-width: 5px;"
                             "border-color: #000;"
                             "background-color : blue;")

        #Label and Subject code entry
        l1=QtGui.QLabel(self)
        l1.setAlignment(QtCore.Qt.AlignCenter)
        l1.setGeometry(QtCore.QRect(200,150,130,30))
        l1.setStyleSheet("QLabel { background-color : #DDD;color :black ; }")
        font=QtGui.QFont("Times",14,QtGui.QFont.Bold)
        l1.setFont(font)
        l1.setText("Enter Year")

        self.e1=QtGui.QLineEdit(self)
        self.e1.setGeometry(200,200,300,30)
        self.e1.setAlignment(QtCore.Qt.AlignCenter)
        font1=QtGui.QFont("Arial",14)
        self.e1.setFont(font1)

        #Taking Student's Registration Number
        l2=QtGui.QLabel(self)
        l2.setAlignment(QtCore.Qt.AlignCenter)
        l2.setGeometry(QtCore.QRect(200,250,175,30))
        l2.setStyleSheet("QLabel { background-color : #DDD;color :black ; }")
        l2.setFont(font)
        l2.setText("Enter Subject Code")

        self.e2=QtGui.QLineEdit(self)
        self.e2.setGeometry(200,300,300,30)
        self.e2.setAlignment(QtCore.Qt.AlignCenter)
        self.e2.setFont(font1)
        
        #Recording Button
        b1=QtGui.QPushButton(self)
        b1.setText("RECORD AND MARK")
        b1.setStyleSheet("QPushButton { background-color : #DDD;color : black ; }")
        b1.setFont(font)
        b1.setGeometry(100,500,280,30)
        b1.clicked.connect(self.record_and_mark)

        #Check Attendance button to check specific subject's Attendance
        b2=QtGui.QPushButton(self)
        b2.setText("CHECK ATTENDANCE")
        b2.setStyleSheet("QPushButton { background-color : #DDD;color : black ; }")
        b2.setFont(font)
        b2.setGeometry(400,500,280,30)
        b2.clicked.connect(self.create_check_attendance)

        self.l3=QtGui.QLabel(self)
        self.l3.setAlignment(QtCore.Qt.AlignCenter)
        self.l3.setGeometry(QtCore.QRect(300, 550,250,30))
        self.l3.setStyleSheet("QLabel {  color:green ; }")
        self.l3.setFont(QtGui.QFont('Times',13))
        
    def create_check_attendance(self):
        self._check_attendance = CheckAttendance(self.e2.text(), self.e1.text())
        self._check_attendance.show()

    def record_and_mark(self):
        self.record() #to record the video and save it to folder 'videos'
        self.mark()

    def record(self):
        video = cv2.VideoCapture(0)
        if (video.isOpened() == False): 
            print("Error reading video file")
        
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        
        size = (frame_width, frame_height)
        
        result = cv2.VideoWriter("videos/{}.mp4".format(self.e2.text()), 
                                cv2.VideoWriter_fourcc(*'MJPG'),
                                10, size)
            
        while(True):
            ret, frame = video.read()
        
            if ret == True: 
        
                result.write(frame)
        
                cv2.imshow('Frame', frame)
        
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
        
            else:
                break
        
        video.release()
        result.release()
            
        cv2.destroyAllWindows()
        
        return
    
    def mark(self):
        self.get_snaps() #to get snaps from the recorded video
        self.extract_faces() #to read all faces from the snaps
        self.match() #match extracted faces to those in database and update the database

    def get_snaps(self):
        shutil.rmtree("temp",ignore_errors=True)
        os.mkdir("temp")
        os.mkdir("temp/presentFaces")
        video_name = str(self.e2.text())
        crop_time = 2
        time_gap = 2

        cap = cv2.VideoCapture("videos/"+video_name+".mp4")
        fps    = int(cap.get(cv2.CAP_PROP_FPS))
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        count = fps*(crop_time)
        i = 0
        cap.set(1,68)
        while (cap.isOpened()):
            ret , frame = cap.read()
            if(count>length):
                break   
            cv2.waitKey(3)
            if( (count == (crop_time*fps + i*time_gap*fps)) &(count < length)):
                cv2.imwrite('temp/frame'+str(i)+'.jpg',frame)
                i = i+1
            count = count + 1
        cap.release()
        cv2.destroyAllWindows()
        
    def extract_faces(self):
        i=0
        face_cascade = cv2.CascadeClassifier("support_files/haarcascade_frontalface_default.xml")
        for eachImg in os.listdir("temp"):
            img = cv2.imread("temp/" + eachImg, 0)
            faces = face_cascade.detectMultiScale(img) 
            x=0
            for(x,y,w,h) in faces:
                sub_face = img[y:y+h, x:x+w]

                face_file_name = "temp/presentFaces/face_" + str(i) + ".jpg"
                cv2.imwrite(face_file_name,sub_face)
                i=i+1
                x+=1
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def match(self):
        subject = str(self.e2.text())

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector= cv2.CascadeClassifier("support_files/haarcascade_frontalface_default.xml")

        faceSamples=[]
        Ids=[]

        def getImagesAndLabels(path, faceSamples, Ids):
            imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
            for imagePath in imagePaths:
                pilImage=Image.open(imagePath).convert('L')
                imageNp=np.array(pilImage,'uint8')
                Id=int(os.path.split(imagePath)[1].split(".")[0])
                faces=detector.detectMultiScale(imageNp)
                for (x,y,w,h) in faces:
                    faceSamples.append(imageNp[y:y+h,x:x+w])
                    Ids.append(Id)
                cv2.waitKey(100)
            return faceSamples,Ids

        def faceDetector(path):
            recognizer.read("trainer/trainer.yml")
            present = []
            imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
            for imagePath in imagePaths:
                img = cv2.imread(imagePath)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                id, conf = recognizer.predict(gray)
                present.append(id)
            present = set(present)
            return list(present)

        shutil.rmtree("trainer",ignore_errors=True)
        os.mkdir("trainer")
        faces, Ids = getImagesAndLabels("registration_images/Year{}".format(self.e1.text()), faceSamples, Ids)
        recognizer.train(faces, np.array(Ids))
        recognizer.write('trainer/trainer.yml')
        present = faceDetector("temp/presentFaces")

        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="6989",
                database="attendance"
        )
        mycursor = mydb.cursor()
        query='SELECT Roll FROM YEAR{};'.format(self.e1.text())
        try:
            mycursor.execute(query)
        except mysql.connector.DatabaseError as e:
            print(F"Accured Error: {e}")

        rolls = []
        result = mycursor.fetchall()
        for row in result:
            rolls.append(row[0])
        print(rolls)
        temp = []
        for r in rolls:
            if (r in present):
                temp.append('P')
            else:
                temp.append('A')
        
        rolls = list(map(str, rolls))
        
        rolls = ['"' + i + '"' for i in rolls]
        temp = ['"' + i + '"' for i in temp]

        mycursor.execute("SHOW TABLES")
        exist = 0
        current_table = str(self.e2.text())
        for table in mycursor:
            if current_table == str(table):
                exist = 1
                break
        
        length = len(rolls)
        new_date = str(date.today().strftime("%d/%m/%Y"))
        new_time = str(datetime.now()).split(" ")[1].split(".")[0]

        res = [(new_date, new_time, rolls[i], temp[i]) for i in range(length)]
        mycursor.execute("SHOW TABLES")
        exists = 0
        for i in mycursor:
            if str(i) == str(self.e2.text()):
                exists = 1
                break
        
        if exists == 0:
            try:
                mycursor.execute("CREATE TABLE {} (Date TEXT, Time TEXT, Roll TEXT, Status TEXT)".format(str(self.e2.text())),)
            except mysql.connector.DatabaseError as e:
                pass

        statement = 'INSERT INTO {} (Date, Time, Roll, Status) VALUES (%s, %s, %s, %s);'.format(current_table)
        try:
            mycursor.executemany(statement, res)
            mydb.commit()
            self.l3.setText("Attendance was marked successfully!")
        except mysql.connector.DatabaseError as e:
            print(F"Accured Error: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close() 
    
if __name__ == '__main__':
    app = QtGui.QApplication([])
    gui = AttendanceWindow()
    gui.show()
    app.exec_()
