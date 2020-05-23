import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle
from pymongo import MongoClient
from content import SetContent
from football import Ui_MainWindow


class CreateChooseWidget(QtWidgets.QWidget):

    def __init__(self, match):
        super(CreateChooseWidget, self).__init__()
        self.match_info = match
        self.name = self.match_info['match']
        self.lbl = QtWidgets.QPushButton(self.name.replace("_", " "))
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)
        self.lbl.clicked.connect(partial(SetContent, self.match_info, MainWindow.ui))


class ScrollMatches(QtWidgets.QMessageBox):

    def __init__(self, all_matches, *args, **kwargs):
        QtWidgets.QMessageBox.__init__(self, *args, **kwargs)
        self.setWindowTitle("Выбор матча")
        self.setWindowIcon(QtGui.QIcon("icons/match-16.png"))
        self.setStandardButtons(QtWidgets.QMessageBox.Close)

        self.widgets = []
        self.content = QtWidgets.QWidget()

        self.searchbar = QtWidgets.QLineEdit()
        self.searchbar.setStyleSheet("background-image: "
                                     "url(icons/search-16.png);"
                                     "background-repeat: no-repeat; "
                                     "background-position: right;")
        self.searchbar.setPlaceholderText("Поиск по матчам")
        self.searchbar.textChanged.connect(self.update_display)

        scroll = QtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.content)

        self.lay = QtWidgets.QVBoxLayout(self.content)
        self.lay.addWidget(self.searchbar)
        self.completer = QtWidgets.QCompleter([x["match"].replace("_", " ")
                                               for x in all_matches])
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)
        for match in all_matches:
            item = CreateChooseWidget(match)
            self.lay.addWidget(item)
            self.widgets.append(item)
        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum,
                                       QtWidgets.QSizePolicy.Expanding)
        self.lay.addItem(spacer)
        self.content.setLayout(self.lay)

        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setStyleSheet("QScrollArea{min-width:300 px; min-height: 400px}")

    def update_display(self, text):
        """
        сокрытие или показ матчей в соответствии с текстом в поисковой стркое
        """
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()


def choose_matches_clicked():

    client = MongoClient("mongodb://34.91.248.129:27017/")
    db_conn = client["football"]
    col_conn = db_conn["gameIndicators"]
    matches = [x for x in col_conn.find({}, {"_id": 0})]
    result = ScrollMatches(matches, None)
    result.exec_()


def dark_mode():
    """
    изменение цветовой темы окна
    :yield: - тема
    """
    while True:
        MainWindow.ui.graphWidget.setBackground('#1C1C1C')
        MainWindow.ui.graphWidget2.setBackground('#1C1C1C')
        yield MainWindow.setStyleSheet("background: #1C1C1C")  # brown
        MainWindow.ui.graphWidget.setBackground('#011F36')
        MainWindow.ui.graphWidget2.setBackground('#011F36')
        yield MainWindow.setStyleSheet("background: #011F36;")  # blue
        MainWindow.ui.graphWidget.setBackground('#121e29')
        MainWindow.ui.graphWidget2.setBackground('#121e29')
        yield MainWindow.setStyleSheet("background: #121e29")  # dark_new


class MyWindow(QtWidgets.QMainWindow):
    """
    класс окна приложения, задает интерфейс и перехватывает события
    """
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setup_ui(self)

    def closeEvent(self, event):
        """
        перехват события закрытия окна, вывод окна с вопросом при
        возникновении события
        :param event: - событие
        """
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Выход")
        msg_icon = QtGui.QIcon()
        msg_icon.addFile('icons/ball-16.png', QtCore.QSize(16, 16))
        msg.setWindowIcon(msg_icon)
        msg.setText("Вы действительно хотите выйти?")
        button_yes = msg.addButton("Да", QtWidgets.QMessageBox.AcceptRole)
        msg.addButton("Нет", QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(button_yes)
        msg.exec_()
        if msg.clickedButton() == button_yes:
            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, event):
        """
        перехват события изменения размера окна, изменение размеров элементов
        :param event: - событие
        """
        self.w = self.size().width()
        self.h = self.size().height()
        self.ui.contacts.setGeometry(QtCore.QRect(0, 5, 160, 50))  # контакты
        self.ui.tabWidget.setGeometry(QtCore.QRect(
            10, 50, self.w * 0.97, self.h * 0.59))  # виджет с графиками
        main_table_w = self.ui.tabWidget.width()
        main_table_h = self.ui.tabWidget.height()
        self.ui.lbl.setGeometry(QtCore.QRect(230, 10, 600, 60))
        self.ui.tableWidget_1.setGeometry(QtCore.QRect(
            0, 0, main_table_w - 10, main_table_h - 30))  # команда 1
        self.ui.tableWidget_2.setGeometry(QtCore.QRect(
            0, 0, main_table_w - 10, main_table_h - 30))  # команда 2
        self.ui.tableWidget_3.setGeometry(QtCore.QRect(
            10, main_table_h + 70, self.w * 0.97, 111))  # показатели команд
        self.ui.groupBox.setGeometry(QtCore.QRect(
            10, main_table_h + 200, self.w * 0.97, 151))  # другие расчеты
        self.ui.pushButton_2.setGeometry(QtCore.QRect(
            main_table_w * 0.78, 30, 130, 25))  # кнопка сменить тему
        self.ui.chooiseMatch.setGeometry(QtCore.QRect(
            main_table_w * 0.78, 60, 130, 25))  # кнопка выбор матча
        self.ui.graphicsView.setGeometry(QtCore.QRect(
            0, 120, main_table_w / 2, main_table_h * 0.64))  # поле для левого графика
        self.ui.graphWidget.setGeometry(QtCore.QRect(
            0, 0, main_table_w / 2, main_table_h * 0.64))  # левый график
        self.ui.graphicsView2.setGeometry(QtCore.QRect(
            main_table_w/2-10, 120, main_table_w / 2, main_table_h * 0.64))  # поле правого графика
        self.ui.graphWidget2.setGeometry(QtCore.QRect(
            0, 0, main_table_w / 2, main_table_h * 0.64))  # правый график
        if main_table_w >= 1020:
            self._centralize_widgets(main_table_w, main_table_h)

    def _centralize_widgets(self, main_table_w, main_table_h):
        """
        расположение всех виджетов по центру окна
        :param main_table_w: - ширина главной таблицы
        :param main_table_h: - высота главной таблицы
        """
        indent = (self.w - main_table_w) / 2
        self.ui.contacts.setGeometry(QtCore.QRect(indent, 5, 160, 50))
        self.ui.lbl.setGeometry(QtCore.QRect(indent + 230, 10, 600, 60))  # заголовок
        self.ui.tabWidget.setGeometry(QtCore.QRect(
            indent, 50, self.w * 0.97, self.h * 0.59))  # виджет с графиками
        self.ui.tableWidget_1.setGeometry(QtCore.QRect(
            0, 0, main_table_w - 10, main_table_h - 30))  # команда 1
        self.ui.tableWidget_2.setGeometry(QtCore.QRect(
            0, 0, main_table_w - 10, main_table_h - 30))  # команда 2
        self.ui.tableWidget_3.setGeometry(QtCore.QRect(
            indent, main_table_h + 70, self.w * 0.97, 111))  # показатели
        self.ui.groupBox.setGeometry(QtCore.QRect(
            indent, main_table_h + 200, self.w * 0.97, 151))  # другие расчет
        self.ui.graphicsView.setGeometry(QtCore.QRect(
            0, 120, main_table_w / 2, main_table_h * 0.64))  # поле для левого графика
        self.ui.graphWidget.setGeometry(QtCore.QRect(
            0, 0, main_table_w / 2, main_table_h * 0.64))  # левый график
        self.ui.graphicsView2.setGeometry(QtCore.QRect(
            main_table_w / 2 - 10, 120, main_table_w / 2, main_table_h * 0.64))  # поле правого графика
        self.ui.graphWidget2.setGeometry(QtCore.QRect(
            0, 0, main_table_w / 2, main_table_h * 0.64))  # правый график


if __name__ == "__main__":

    # start

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    MainWindow.setStyleSheet("background: #121e29")
    MainWindow.show()
    # main

    MainWindow.ui.chooiseMatch.clicked.connect(choose_matches_clicked)
    MainWindow.ui.pushButton_2.clicked.connect(partial(next, (dark_mode())))

    # exit

    sys.exit(app.exec_())
