import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from football import Ui_MainWindow
import qdarkstyle
from functools import partial
from content import setContent, data


class createChooseWidget(QtWidgets.QWidget):

    def __init__(self, name):
        super(createChooseWidget, self).__init__()
        self.name = name
        self.lbl = QtWidgets.QPushButton(self.name)
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)
        self.lbl.clicked.connect(partial(setContent, self.name, ui))


class ScrollMatches(QtWidgets.QMessageBox):

    def __init__(self, all_matches, *args, **kwargs):
        QtWidgets.QMessageBox.__init__(self, *args, **kwargs)
        self.setWindowTitle("Выбор матча")
        self.setWindowIcon(QtGui.QIcon("icons/match-16.png"))
        self.setStandardButtons(QtWidgets.QMessageBox.Close)

        self.widgets = []
        self.content = QtWidgets.QWidget()

        self.searchbar = QtWidgets.QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)

        scroll = QtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.content)

        self.lay = QtWidgets.QVBoxLayout(self.content)
        self.lay.addWidget(self.searchbar)

        self.completer = QtWidgets.QCompleter(all_matches)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        for match in all_matches:
            item = createChooseWidget(match)
            self.lay.addWidget(item)
            self.widgets.append(item)
        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
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
    result = ScrollMatches([match.replace("_", " ") for match in data], None)
    result.exec_()


def setSettings():
    ...


if __name__ == "__main__":

    # start

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    # main

    ui.chooiseMatch.clicked.connect(chooseMatchesClicked)
    ui.pushButton_2.clicked.connect(setSettings)

    # exit

    sys.exit(app.exec_())
