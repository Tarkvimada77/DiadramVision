import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PIL import Image

def is_pol(val):
    if val < 0:
        return abs(val)
    elif val > 0:
        return -val
    else:
        return 0

class Rotate(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Rotate, self).__init__(parent)

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
        im_rotate.save('guido_45.png', quality=95)
        im.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаём экземпляp созданного изменённого файла
    main = Rotate()

    # Рисуем окно виджетов
    main.show()


    # Бесконечный цикл (луп) 

    sys.exit(app.exec_())

