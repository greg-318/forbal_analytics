import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle
from pymongo import MongoClient
from content import SetContent
from football import Ui_MainWindow


class createChooseWidget(QtWidgets.QWidget):

    def __init__(self, match):
        super(createChooseWidget, self).__init__()
        self.match = match
        self.lbl = QtWidgets.QPushButton(self.match["match"].replace("_", " "))
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)
        self.lbl.clicked.connect(partial(SetContent, self.match, ui))


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
            item = createChooseWidget(match)
            self.lay.addWidget(item)
            self.widgets.append(item)
        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum,
                                       QtWidgets.QSizePolicy.Expanding)
        self.lay.addItem(spacer)
        self.content.setLayout(self.lay)

        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setStyleSheet("QScrollArea{min-width:300 px; min-height: 400px}")

    def update_display(self, text):
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()


def chooseMatchesClicked():
    client = MongoClient("mongodb://34.91.248.129:27017/")
    db_conn = client["football"]
    col_conn = db_conn["gameIndicators"]
    matches = [x for x in col_conn.find({}, {"_id": 0})]
    result = ScrollMatches(matches, None)
    result.exec_()


def darkMode():
    while True:
        ui.graphWidget.setBackground('#1C1C1C')
        ui.graphWidget2.setBackground('#1C1C1C')
        yield MainWindow.setStyleSheet("background: #1C1C1C")  # brown
        ui.graphWidget.setBackground('#011F36')
        ui.graphWidget2.setBackground('#011F36')
        yield MainWindow.setStyleSheet("background: #011F36;")  # blue
        ui.graphWidget.setBackground('#121e29')
        ui.graphWidget2.setBackground('#121e29')
        yield MainWindow.setStyleSheet("background: #121e29")  # dark_new


if __name__ == "__main__":

    # start

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    MainWindow.setStyleSheet("background: #121e29")

    # main

    ui.chooiseMatch.clicked.connect(chooseMatchesClicked)
    ui.pushButton_2.clicked.connect(partial(next, (darkMode())))

    # exit

    sys.exit(app.exec_())
