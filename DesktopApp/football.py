from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


class Ui_MainWindow(object):
    """
    настройки графического интерфейса окна
    """
    def setup_ui(self, MainWindow):
        """
        начальные настройки интерфейса
        :param MainWindow: - окно приложения
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(830,620)
        app_icon = QtGui.QIcon()
        app_icon.addFile('icons/ball-16.png', QtCore.QSize(16, 16))
        app_icon.addFile('icons/ball-24.png', QtCore.QSize(24, 24))
        app_icon.addFile('icons/ball-32.png', QtCore.QSize(32, 32))
        MainWindow.setWindowIcon(app_icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setObjectName('scroll_area')
        self.scroll_area.setStyleSheet('#scroll_area{border:none}')
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setGeometry(QtCore.QRect(15, 0, 820, 620))
        self.scroll_area.setMaximumHeight(810)
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setGeometry(QtCore.QRect(0, 0, 800, 800))
        self.scroll_area.setWidget(self.main_widget)

        self.contacts = QtWidgets.QWidget(self.main_widget)
        self.contacts.setGeometry(QtCore.QRect(0, 5, 160, 50))
        self.vk = QtWidgets.QLineEdit(self.contacts)  # ссылка вк
        self.vk.setReadOnly(True)
        self.vk.setStyleSheet("QLineEdit{border:none}")
        self.vk.setText('tab_betting')
        self.vk.setGeometry(QtCore.QRect(25, 0, 130, 20))
        self.vk_icon = QtWidgets.QLabel(self.contacts)  # иконка вк
        self.vk_icon.setPixmap(QtGui.QPixmap("icons/vk.png"))
        self.vk_icon.setGeometry(QtCore.QRect(10, 0, 20, 20))
        self.tg = QtWidgets.QLineEdit(self.contacts)  # ссылка телега
        self.tg.setReadOnly(True)
        self.tg.setStyleSheet("QLineEdit{border:none}")
        self.tg.setText("@football_analytics_RD")
        self.tg.setGeometry(QtCore.QRect(25, 20, 130, 20))
        self.tg_icon = QtWidgets.QLabel(self.contacts)  # иконка телега
        self.tg_icon.setPixmap(QtGui.QPixmap("icons/tg.png"))
        self.tg_icon.setGeometry(QtCore.QRect(10, 20, 20, 20))

        self.pixmap = QtGui.QPixmap("icons/image.png")
        self.lbl = QtWidgets.QLabel(self.main_widget)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setGeometry(QtCore.QRect(230, 10, 600, 60))

        self.tableWidget_3 = QtWidgets.QTableWidget(self.main_widget)
        self.tableWidget_3.setGeometry(QtCore.QRect(10, 480, 780, 111))
        self.tableWidget_3.setMaximumSize(1020, 200)
        self.tableWidget_3.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget_3.setFont(font)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(19)
        width_col_tableWidget_3 = (100, 45, 30, 45, 45, 45, 50, 30, 30, 30,
                                   30, 30, 45, 45, 30, 45, 30, 30, 30)
        tuple(self.tableWidget_3.setColumnWidth(index, value) for index, value
              in enumerate(width_col_tableWidget_3))
        self.tableWidget_3.setRowCount(2)
        for index in range(2):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setVerticalHeaderItem(index, item)

        tooltip_team = ("Название команды", "Количество сыгранных матчей",
                        "Победы", "Ничьи", "Поражения", "Забитых голов",
                        "Пропущенных голов", "Разница в голах", "Очки",
                        "Ожидаемых забитых голов",
                        "Ожидаемых забитых голов без учета пенальти",
                        "Ожидаемых пропущенных голов",
                        "Ожидаемых пропущенных голов без учета пенальти",
                        "Разница между ожидаемыми забитыми/пропущенными голами",
                        "Прессинг (сколько пасов соперник успеет сделать до "
                        "потери мяча)",
                        "Выход из прессинга (сколько соперник позволяет "
                        "команде сделать своих передач после потери)",
                        "Сколько раз команда успешно доставила мяч в радиус 18 "
                        "метров от ворот без навесов",
                        "Сколько раз команда позволяла сопернику делать "
                        "передачи в радиус 18 метров от ворот",
                        "Ожидаемые набранные очки")
        for value in tooltip_team:
            item = QtWidgets.QTableWidgetItem()
            item.setToolTip(value)
            self.tableWidget_3.setHorizontalHeaderItem(
                tooltip_team.index(value), item)

        self.tabWidget = QtWidgets.QTabWidget(self.main_widget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 50, 781, 411))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setMaximumSize(1020, 537)
        self.team_1 = QtWidgets.QWidget()
        self.team_1.setObjectName("team_1")
        self.tableWidget_1 = QtWidgets.QTableWidget(self.team_1)
        self.tableWidget_1.setSortingEnabled(True)
        self.tableWidget_1.setGeometry(QtCore.QRect(0, 0, 771, 381))
        self.tableWidget_1.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget_1.setFont(font)
        self.tableWidget_1.setStyleSheet("color: rgb(42, 187, 155)")
        self.tableWidget_1.setObjectName("tableWidget_1")
        self.tableWidget_1.setColumnCount(23)
        width_col_tableWidget_1_2 = (100, 60, 80, 60, 50, 40, 20, 20, 20, 20, 20
                                     , 20, 60, 70, 50, 60, 20, 70, 80, 80, 80,
                                     50, 20)
        tuple(self.tableWidget_1.setColumnWidth(index, value) for index, value
              in enumerate(width_col_tableWidget_1_2))
        self.tableWidget_1.setRowCount(11)
        list_MF1 = [""]
        list_BF1 = [""]
        list_F1 = [""]
        list_G1 = [""]
        for index in range(11):
            item = QtWidgets.QComboBox()
            if index in tuple(range(4)):
                item.addItems(list_MF1)
            elif index in (4, 5, 6, 7):
                item.addItems(list_BF1)
            elif index in (8, 9):
                item.addItems(list_F1)
            else:
                item.addItems(list_G1)
            self.tableWidget_1.setCellWidget(index, 0, item)

        for index in range(11):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_1.setVerticalHeaderItem(index, item)
        tooltip_player = ("Имя и фамилия игрока", "Игровая позиция",
                          "Количество игр в текущем сезоне",
                          "Количество игровых минут", "Забитых голов",
                          "Забитых голов без пенальти", "Голевые передачи",
                          "В среднем ударов за 90 мин",
                          "Среднее количество пасов за 90 мин, завершившихся "
                          "ударом по воротам",
                          "Ожидаемых забитых голов",
                          "Ожидаемых забитых голов без учета пенальти",
                          "Вес ассиста, после выполненного паса под удар",
                          "Сумма xG всех атак, которые завершились ударом и в "
                          "которых игрок принимал участие",
                          "Сумма xgchain, но без начисления балов за голы и "
                          "ключевые пасы",
                          "Среднее ожидаемое количество голов за 90 минут",
                          "Ожидаемые голы не с пенальти за 90 минут",
                          "Среднее ожидаемое количество голевых передач за "
                          "90 минут", "Сумма xG90 и xA90", "Сумма NPxG90 и xA90"
                          , "xgchain за 90 минут", "xGBuildup за 90 минут",
                          "Желтых карточек в текущем сезоне",
                          "Красных карточек в текущем сезоне")
        for index, value in enumerate(tooltip_player):
            item = QtWidgets.QTableWidgetItem()
            item.setToolTip(value)
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_1.setHorizontalHeaderItem(index, item)
        self.tabWidget.addTab(self.team_1, "")

        self.team_2 = QtWidgets.QWidget()
        self.team_2.setObjectName("team_2")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.team_2)
        self.tableWidget_2.setSortingEnabled(True)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 0, 771, 381))
        self.tableWidget_2.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setStyleSheet("color: rgb(222, 193, 78)")
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(23)
        tuple(self.tableWidget_2.setColumnWidth(index, value) for index, value
              in enumerate(width_col_tableWidget_1_2))
        self.tableWidget_2.setRowCount(11)
        list_MF2 = [""]
        list_BF2 = [""]
        list_F2 = [""]
        list_G2 = [""]
        for index in range(11):
            item = QtWidgets.QComboBox()
            if index in tuple(range(4)):
                item.addItems(list_MF2)
            elif index in (4, 5, 6, 7):
                item.addItems(list_BF2)
            elif index in (8, 9):
                item.addItems(list_F2)
            else:
                item.addItems(list_G2)
            self.tableWidget_2.setCellWidget(index, 0, item)

        for index in range(11):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setVerticalHeaderItem(index, item)
        for index, value in enumerate(tooltip_player):
            item = QtWidgets.QTableWidgetItem()
            item.setToolTip(value)
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_2.setHorizontalHeaderItem(index, item)
        self.tabWidget.addTab(self.team_2, "")

        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 771, 111))
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(27)
        width_col_tableWidget = (100, 50, 30, 45, 55, 55, 50, 50, 50, 30,
                                 50, 50, 55, 45, 45, 50, 45, 45, 45, 45,
                                 45, 50, 45, 45, 45, 50, 30)
        tuple(self.tableWidget.setColumnWidth(index, value) for index, value in
              enumerate(width_col_tableWidget))
        self.tableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        tooltip_gameIndicators = ("Название команды", "Показатели матча",
                                  "Средний % владения мячом", "Всего ударов",
                                  "Всего ударов в створ ворот",
                                  "Всего ударов мимо ворот",
                                  "Заблокированные удары",
                                  "Угловые", "Вне игры", "Фолы",
                                  "Всего желтых карточек",
                                  "Голевые моменты", "Упущено голевых моментов",
                                  "Ударов в штангу", "Удары из штрафной",
                                  "Удары из-за штрафной", "Сейвы вратаря",
                                  "Всего пасы",
                                  "Точные пасы", "Дальние передачи",
                                  "Передачи в штрафную площадь",
                                  "Потеря мяча","Победы в единоборствах",
                                  "Выигранные единоборства в воздухе",
                                  "Отборы", "Перехваты", "Выносы")
        for index, value in enumerate(tooltip_gameIndicators):
            item = QtWidgets.QTableWidgetItem()
            item.setToolTip(value)
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget.setHorizontalHeaderItem(index, item)

        self.graphicsView = QtWidgets.QGraphicsView(self.tab_3)
        self.graphicsView.setGeometry(QtCore.QRect(0, 120, 771, 261))
        self.graphicsView.setObjectName("graphicsView")
        self.graphWidget = pg.PlotWidget(self.graphicsView)
        self.graphWidget.setGeometry(QtCore.QRect(0, 0, 385, 265))
        self.graphWidget.setBackground('#121e29')
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.graphWidget.showGrid(x=1, y=1)
        self.graphWidget.addLegend()
        self.graphWidget.setMenuEnabled(False)
        self.graphWidget.setTitle("Команда №1")
        self.blue = pg.mkPen(color=(222, 193, 78), width=2)
        self.red = pg.mkPen(color=(42, 187, 155), width=2)
        self.probabilities = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        shots = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.graphWidget.plot(self.probabilities, shots, pen=self.red,
                              name="-Вероятность забить X голов",
                              symbol="o", symbolSize=6, symbolBrush="w")

        self.graphicsView2 = QtWidgets.QGraphicsView(self.tab_3)
        self.graphicsView2.setGeometry(QtCore.QRect(388, 120, 771, 261))
        self.graphicsView2.setObjectName("graphicsView")
        self.graphWidget2 = pg.PlotWidget(self.graphicsView2)
        self.graphWidget2.setGeometry(QtCore.QRect(0, 0, 385, 265))
        self.graphWidget2.setBackground('#121e29')
        self.graphWidget2.setMouseEnabled(x=False, y=False)
        self.graphWidget2.showGrid(x=1, y=1)
        self.graphWidget2.addLegend()
        self.graphWidget2.setMenuEnabled(False)
        self.graphWidget2.setTitle("Команда №2")
        g2shots = [50, 35, 44, 22, 38, 32, 27, 38, 32, 44]

        self.graphWidget2.plot(self.probabilities, g2shots, pen=self.blue,
                               name="-Вероятность забить X голов",
                               symbol="o", symbolSize=6, symbolBrush="w")
        self.tabWidget.addTab(self.tab_3, "")

        self.groupBox = QtWidgets.QGroupBox(self.main_widget)
        self.groupBox.setGeometry(QtCore.QRect(10, 610, 781, 151))
        self.groupBox.setMaximumSize(1020, 151)
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 151, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 135, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(190, 30, 71, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(190, 60, 71, 16))
        self.label_4.setObjectName("label_4")
        # self.label_5 = QtWidgets.QLabel(self.groupBox)
        # self.label_5.setGeometry(QtCore.QRect(10, 120, 171, 16))
        # self.label_5.setObjectName("label_5")
        # self.label_6 = QtWidgets.QLabel(self.groupBox)
        # self.label_6.setGeometry(QtCore.QRect(10, 90, 171, 16))
        # self.label_6.setObjectName("label_6")
        # self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        # self.progressBar.setGeometry(QtCore.QRect(190, 90, 111, 16))
        # self.progressBar.setProperty("value", 24)
        # self.progressBar.setObjectName("progressBar")
        # self.progressBar_2 = QtWidgets.QProgressBar(self.groupBox)
        # self.progressBar_2.setGeometry(QtCore.QRect(190, 120, 111, 16))
        # self.progressBar_2.setProperty("value", 24)
        # self.progressBar_2.setObjectName("progressBar_2")
        # self.label_7 = QtWidgets.QLabel(self.groupBox)
        # self.label_7.setGeometry(QtCore.QRect(320, 30, 171, 16))
        # self.label_7.setObjectName("label_7")
        # self.label_8 = QtWidgets.QLabel(self.groupBox)
        # self.label_8.setGeometry(QtCore.QRect(490, 30, 16, 16))
        # self.label_8.setObjectName("label_8")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(620, 30, 130, 25))
        self.pushButton_2.setObjectName("refresh")
        self.chooiseMatch = QtWidgets.QPushButton(self.groupBox)
        self.chooiseMatch.setGeometry(QtCore.QRect(620, 60, 130, 25))
        self.chooiseMatch.setObjectName("chooiseMatch")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslate_ui(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        self.centralwidget.setStyleSheet(
            "QToolTip { color: #ffffff; background-color: #000000; "
            "border: 0px; }")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow",
                                             "Football Analytics"))
        self.pushButton_2.setText(_translate("MainWindow", "Сменить тему"))
        self.chooiseMatch.setText(_translate("MainWindow", "Выбор матча"))

        columns_team = ("team", "games", "wins", "draws", "loses", "goals",
                        "missed", 'gd', "pts", "xg", "npxg", "xga",
                        "npxga", "npxgd", "ppda", "oppda", "dc", "odc", "xpts")
        for index, value in enumerate(columns_team):
            item = self.tableWidget_3.horizontalHeaderItem(index)
            item.setText(_translate("MainWindow", value))
        self.tabWidget.addTab(self.team_1, "Команда №1")

        columns_player = ("player", "position", "appearances", "minutes",
                          "goals", "npg", "a", "sh90", "kp90", "xg", "npxg",
                          "xa", "xgchain", "xgbuildup", "xg90", "npxg90",
                          "xa90", "xg90xa90", "npxg90xa90", "xgchain90",
                          "xgbuildup90", "yellow", "red")
        for index, value in enumerate(columns_player):
            item = self.tableWidget_1.horizontalHeaderItem(index)
            item.setText(_translate("MainWindow", value))
        self.tabWidget.addTab(self.team_1, "Команда №1")
        for index, value in enumerate(columns_player):
            item = self.tableWidget_2.horizontalHeaderItem(index)
            item.setText(_translate("MainWindow", value))
        self.tabWidget.addTab(self.team_2, "Команда №2")

        columns_gameIndicators = ("team", "period", "bp", "shots", "on_targ",
                                  "off_targ", "blocks", "corner", "offside",
                                  "foul", "yellow", "chance",
                                  "sh_miss", "hit_w", "sh_in", "sh_off",
                                  "saves", "pass",
                                  "apass", "long", "cross", "loss_bp",
                                  "duels", "air_w",
                                  "tack", "interc", "cl")
        for index, value in enumerate(columns_gameIndicators):
            item = self.tableWidget.horizontalHeaderItem(index)
            item.setText(_translate("MainWindow", value))
        self.tabWidget.addTab(self.tab_3, "Показатели матча")

        self.groupBox.setTitle(_translate("MainWindow", "Другие расчеты"))
        self.label.setText(_translate("MainWindow",
                                      "Прогнозируемый результат:"))
        self.label_2.setText(_translate("MainWindow",
                                        "Фактический результат:"))
        self.label_3.setText(_translate("MainWindow", "None"))
        self.label_4.setText(_translate("MainWindow", "None"))
        # self.label_5.setText(_translate("MainWindow",
        #                                 "Оценка рейтинга команды №2:"))
        # self.label_6.setText(_translate("MainWindow",
        #                                 "Оценка рейтинга команды №1:"))
        # self.label_7.setText(_translate("MainWindow",
        #                                 "Ожидаемый % владения мячом:"))
        # self.label_8.setText(_translate("MainWindow", "0"))
