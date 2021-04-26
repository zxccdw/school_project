# created by klstepan67 | support: zxccdw@mail.ru | vk.com/klstepan67
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem
from PyQt5 import uic


class Theory(QMainWindow):
    def __init__(self, page=1):
        super().__init__()
        self.page = page
        self.test = 1
        self.initUI()

    def initUI(self):
        uic.loadUi('lessons.ui', self)
        self.menu.clicked.connect(self.to_menu)
        self.next.clicked.connect(self.nxt)
        self.pred.clicked.connect(self.prd)
        self.tasks.clicked.connect(self.to_content)
        f = open('lesson_{}.txt'.format(self.page), 'r', encoding="UTf8")
        self.label.setText(f.readline().strip())
        k = f.read()
        self.textBrowser.setText(k)
        self.sch.display(self.page)

    def to_menu(self): # Возврат в главное меню
        self.q = MainWindow()
        self.q.show()
        self.close()

    def nxt(self): # Следующая страница
        if self.page < 2:
            self.page += 1
        self.initUI()

    def prd(self): # Предыдущая страница
        if self.page > 1:
            self.page -= 1
        self.initUI()

    def to_content(self):
        self.q = Content()
        self.q.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.page = 0
        self.test = 1
        self.initUI()
        self.exit.clicked.connect(self.off) # Подключение кнопок к функциям
        self.theory.clicked.connect(self.to_th)
        self.practic.clicked.connect(self.to_pract)

    def initUI(self):
        uic.loadUi('main_window.ui', self)

    def off(self): # Выход из программы
        sys.exit()

    def to_th(self): # Переходим в класс "Theory"
        self.cont = Content()
        self.cont.show()
        self.close()

    def to_pract(self): # Переходим в класс "Practic
        self.prac = Practic()
        self.prac.show()
        self.close()


class Practic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.test = 1
        self.ind_task = 0
        self.mx = -1
        self.ar = []
        self.read_f()
        self.flag = 0

    def initUI(self):
        uic.loadUi('testing.ui', self)
        self.menu.clicked.connect(self.to_menu) # Подключение кнопок
        self.pushButton_0.clicked.connect(self.check)
        self.pushButton_1.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.check)
        self.pushButton_3.clicked.connect(self.check)
        self.print_tasks()

    def to_menu(self): # В главное меню
        self.q = MainWindow()
        self.q.show()
        self.close()

    def read_f(self): # Считывание заданий из файла
        f = open("pract_{}.txt".format(self.test), 'r', encoding="UTF8")
        self.mx = int(f.readline().strip())
        for i in range(self.mx):
            tsk = f.readline().strip()
            ans = f.readline().strip()
            p1 = f.readline().strip()
            p2 = f.readline().strip()
            p3 = f.readline().strip()
            p4 = f.readline().strip()
            self.ar.append([p1, p2, p3, p4, tsk, ans])
        self.initUI()

    def print_tasks(self): # Создание тестовой части
        self.label.setText(self.ar[self.ind_task][5])
        self.pushButton_0.setText(self.ar[self.ind_task][0])
        self.pushButton_1.setText(self.ar[self.ind_task][1])
        self.pushButton_2.setText(self.ar[self.ind_task][2])
        self.pushButton_3.setText(self.ar[self.ind_task][3])

    def check(self): # Проверка ответа пользователя
        answ = self.sender().text()

        if answ == self.ar[self.ind_task][int(self.ar[self.ind_task][4]) - 1]:
            if self.ind_task == 2:
                if self.flag:
                    self.to_menu()
                self.label_2.setText("Верно! Вы решили все задания! Чтобы перейти в главное меню нажмите на "
                                     "правильный ответ еще раз или на кнопку 'главное меню'")
                self.flag = 1

            else:
                self.ind_task += 1
                self.label_2.setText("Верно! Переходим к следующему заданию")
                self.print_tasks()

        else:
            self.label_2.setText("Подумай еще")


class Content(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ar = dict()
        self.initUI()

    def initUI(self):
        uic.loadUi('content.ui', self)
        self.pushButton.clicked.connect(self.to_menu)
        self.add_contents()
        self.listWidget.currentRowChanged.connect(self.to_theme)

    def add_contents(self):
        self.f = open("contents.txt", "r", encoding="UTF8")
        a = int(self.f.readline().rstrip())
        for i in range(a):
            k = self.f.readline().rstrip()
            listWidgetItem = QListWidgetItem(k)
            self.ar[k] = i + 1
            self.listWidget.addItem(listWidgetItem)
        self.f.close()
        return

    def to_menu(self):  # Возврат в главное меню
        self.q = MainWindow()
        self.q.show()
        self.close()

    def to_theme(self):
        # print(self.listWidget.currentItem().text())
        self.q = Theory(page=int(self.ar[self.listWidget.currentItem().text()]))
        self.q.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
