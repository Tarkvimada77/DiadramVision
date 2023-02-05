from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys
from openpyxl import Workbook
from openpyxl.chart import (
    BubbleChart,
    ScatterChart,
    Reference,
    Series,
)
from os import getcwd
from PyQt5 import QtWidgets
import cv2
from PIL import Image
import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PIL import Image

a = 0

def is_pol(val):
    if val < 0:
        return abs(val)
    elif val > 0:
        return -val
    else:
        return 0

class Rotate(QtWidgets.QDialog):
    def __init__(self):
        a = 1
        super(Rotate, self).__init__()

        self.rotation = 0

        self.pixmap = QtGui.QPixmap("crop_graph.png")

        self.label = QLabel()
        self.label.setMinimumSize(600, 600)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setPixmap(self.pixmap)

        button_min = QPushButton("Поворот вправо", self)
        button_min.clicked.connect(self.rotate_pixmap_1)

        button_max = QPushButton("Поворот влево", self)
        button_max.clicked.connect(self.rotate_pixmap_2)

        result = QPushButton("Сохранить")
        result.clicked.connect(self.save)


        grid = QGridLayout(self)
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(button_min, 1, 0)
        grid.addWidget(button_max, 2, 0)
        grid.addWidget(result, 3, 0)

    def rotate_pixmap_1(self):
        pixmap = self.pixmap.copy()
        self.rotation += 3
        print(self.rotation)
        transform = QtGui.QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def rotate_pixmap_2(self):
        pixmap = self.pixmap.copy()
        self.rotation -= 3
        print(self.rotation)
        transform = QtGui.QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def save(self):
        im = Image.open('crop_graph.png')
        im_rotate = im.rotate(is_pol(self.rotation), expand=True)
        im_rotate.save('rotate_image.png', quality=95)



        im.close()




class Croping:
    def __init__(self, path):
        self.path = path
        self.image = cv2.imread(path)
        self.list_rec = []
    
    def window(self):
        cv2.imshow("Croping", self.image)

        cv2.setMouseCallback('Croping', self.mouse_click)

        cv2.waitKey(0)

    def mouse_click(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.list_rec.append(x)
            self.list_rec.append(y)
            
        if event == cv2.EVENT_LBUTTONUP:
            self.list_rec.append(x)
            self.list_rec.append(y)
            print( (self.list_rec[0], self.list_rec[1]), (self.list_rec[2], self.list_rec[3]))
            cv2.rectangle(self.image, (self.list_rec[0], self.list_rec[1]), (self.list_rec[2], self.list_rec[3]), (1, 125, 177), 5)
            
            im = Image.open(self.path)

            min_x = min(self.list_rec[0], self.list_rec[2])
            max_x = max(self.list_rec[0], self.list_rec[2])

            min_y = min(self.list_rec[1], self.list_rec[3])
            max_y = max(self.list_rec[1], self.list_rec[3])

            im.crop((min_x, min_y, max_x, max_y)).save('crop_graph.png', quality=95)
            cv2.imshow("Croping", self.image)
            self.list_rec = []


# Наследование класса PyQt5
class dlgMain(QMainWindow):

    def __init__(self):
        # В конструкторе перемнных через супер получаем все селфы от наследования
        super(dlgMain, self).__init__()

        # Обьявляем пустые переменные
        self.puth = ""
        self.coord = []
        self.val = []
        self.result_y = []
        self.result_x = []
        self.sch = "1"
        self.val1 = []

        self.resize(518, 350)
        # Рисуем элементы окна

        self.button_crop = QPushButton("Обрезать", self)
        self.button_crop.setFont(QFont("Arial", 12))
        self.button_crop.move(160, 175)
        self.button_crop.clicked.connect(self.cropi)

        self.button_crop = QPushButton("Повернуть", self)
        self.button_crop.setFont(QFont("Arial", 12))
        self.button_crop.move(60, 175)
        self.button_crop.clicked.connect(self.rotata)

        self.button = QPushButton("Вычислить значения", self)
        self.button.setFont(QFont("Arial", 12))
        self.button.move(60, 75)
        self.button.clicked.connect(self.save_value)

        self.button = QPushButton("Загрузить изображение", self)
        self.button.setFont(QFont("Arial", 12))
        self.button.move(47, 25)
        self.button.clicked.connect(self.load_img)

    # Хендлер второй кнокпки
    def load_img(self):
        self.puth = QFileDialog.getOpenFileName(self, "open", getcwd(), "IMG (*.png *.jpg)")
        self.img = cv2.imread(self.puth[0])

        # Обнуляем параметры
        self.coord_y = []
        self.coord_x = []
        self.val_y = []
        self.val_x = []
        self.result_y = []
        self.result_x = []
        self.sch = "1"

        f = open('valuey.txt', 'w')
        f.close()

        f = open('valuex.txt', 'w')
        f.close()


        f = open('coordinatey.txt', 'w')
        f.close()

        f = open('coordinatex.txt', 'w')
        f.close()


        #
        # cr = Croping(self.puth[0])
        # cr.window()
        #
        # rot = Rotate()
        # rot.show()


        # self.crp = cv2.imread("crop_graph.png")
        # cv2.imshow('image', self.crp)
        # cv2.setMouseCallback('image', self.mouse_click)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        # Рисуем окошко
            # self.button.setText("Вычислить")



    def cropi(self):
        self.cr = Croping(self.puth[0])
        self.cr.window()

    def rotata(self):
        self.rot = Rotate()
        self.rot.show()


    # Обработчик второй кнопки
    def save_value(self):

        if self.puth != "":
                        
            # Распаковка значений
            with open("coordinatey.txt", "r") as file:
                self.coord_y = file.read().split()

            with open("coordinatex.txt", "r") as file:
                self.coord_x = file.read().split()
            
            with open("valuey.txt", "r") as file:
                self.val_y = file.read().split()

            with open("valuex.txt", "r") as file:
                self.val_x = file.read().split()

            # Разности координат
            difference_coord_x = abs(float(self.coord_x[1]) - float(self.coord_x[0]))
            difference_coord_y = abs(float(self.coord_y[1]) - float(self.coord_y[0]))

            # Разности значений
            differnce_value_x = abs(float(self.val_x[1]) - float(self.val_x[0]))
            differnce_value_y = abs(float(self.val_y[1]) - float(self.val_y[0]))

            # Считаем поинты
            average_x = difference_coord_x / differnce_value_x
            average_y = difference_coord_y / differnce_value_y
            

            # Высчитываем точку относительно послденей координанты, а после отнимаем максимальное значение

            for i in range(2, len(self.coord_x)):
                self.result_x.append(abs(float(self.coord_x[i]) - float(self.coord_x[1])) / average_x)

            for i in range(len(self.result_x)):
                self.result_x[i] = abs(float(self.val_x[1]) - self.result_x[i])
            print(self.result_x)

            for i in range(2, len(self.coord_y)):
                self.result_y.append(abs(float(self.coord_y[i]) - float(self.coord_y[1])) / average_y)

            for i in range(len(self.result_y)):
                self.result_y[i] = abs(float(self.val_y[1]) - self.result_y[i])
            
            
            # Добавляем первые координаты и последние
            self.result_x.insert(0, float(self.val_x[0]))
            self.result_x.append(float(self.val_x[1]))

            self.result_y.insert(0, float(self.val_y[0]))
            self.result_y.append(float(self.val_y[1]))

            dlgMain.norm_func(self)
            
            
    # Записываем график в Excel
    def norm_func(self):
        name = str(random.randint(1, 7634578634))
        wb = Workbook()
        ws = wb.active

        rows = [["a", "b"]]

        for i in range(len(self.result_x)):
            rows.append([self.result_x[i], self.result_y[i]])

        for row in rows:
            ws.append(row)

        c1 = ScatterChart()
        c1.title = name
    
        data = Reference(ws, min_col=1, min_row=2, max_row=len(self.result_x) + 1)
        c1.add_data(data)

        for i in range(3, 4):
            values = Reference(ws, min_col=i, min_row=1, max_row=len(self.result_x) + 1)
            series = Series(values, data, title_from_data=True)
            c1.series.append(series)

        
        ws.add_chart(c1, 'C2')
        wb.save(name + '.xlsx')
        self.inf1()
        return name + '.xlsx'



    def mouse_click(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.crp, self.sch, (x, y), 
                    font, 1, 
                    (0, 255, 255), 
                    2) 
                    
            cv2.imshow('image', self.crp)

            self.sch = int(self.sch) + 1
            self.sch = str(self.sch)

            with open("valuey.txt", "r") as file:
                spis_value = file.read().split()

            with open("coordinatey.txt", "r") as file:
                spis_coord = file.read().split()	


            if len(spis_value) == 0 and len(spis_coord) == 0:
                dlgMain.takeinputsy(self)
                dlgMain.takeinputsx(self)


                with open("coordinatey.txt", "a") as file:
                    file.write(str(y) + " ")

                with open("coordinatex.txt", "a") as file:
                    file.write(str(x) + " ")

            if len(spis_value) == 1 and len(spis_coord) == 1:
                dlgMain.takeinputs1y(self)
                dlgMain.takeinputs1x(self)

                with open("coordinatey.txt", "a") as file:
                    file.write(str(y) + " ")
                with open("coordinatex.txt", "a") as file:
                    file.write(str(x) + " ")

                dlgMain.inf(self)
                    
            
            if len(spis_value) >= 2 and len(spis_coord) >= 2:
                with open("coordinatey.txt", "a") as file:
                    file.write(str(y) + " ")
                with open("coordinatex.txt", "a") as file:
                    file.write(str(x) + " ")



    def takeinputsy(self):
        name, done1 = QtWidgets.QInputDialog.getText(
        self, 'ТЧК', 'Введите первую y точку: ')
        # prfloat(name)

        with open("valuey.txt", "a") as file:
            file.write(name + " ")

    def takeinputs1y(self):
        name, done1 = QtWidgets.QInputDialog.getText(
        self, 'ТЧК', 'Введите последнюю y точку: ')
        # prfloat(name + " ")

        with open("valuey.txt", "a") as file:
            file.write(name + " ")

    def takeinputsx(self):
        name, done1 = QtWidgets.QInputDialog.getText(
        self, 'ТЧК', 'Введите первую  x точку: ')
        # prfloat(name)

        with open("valuex.txt", "a") as file:
            file.write(name + " ")

    def takeinputs1x(self):
        name, done1 = QtWidgets.QInputDialog.getText(
        self, 'ТЧК', 'Введите последнюю x точку: ')
        # prfloat(name + " ")

        with open("valuex.txt", "a") as file:
            file.write(name + " ")

    def inf(self):
        zzz = QMessageBox.information(self, "Информация", "Теперь нажмите на точки, значения которых необходимо вычислить")

    def inf1(self):
        z = QMessageBox.information(self, "Информация", "График успешно сохранён")

# Создаём экземляр программы и запускаем
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаём экземпляp созданного изменённого файла
    main = dlgMain()

    # Рисуем окно виджетов
    main.show()

    # Бесконечный цикл (луп) 

    sys.exit(app.exec_())



