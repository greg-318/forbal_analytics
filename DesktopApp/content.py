import sys
import re
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore
from pymongo import MongoClient
import pathlib

path = '\\'.join(str(pathlib.Path().absolute()).split(r'\\')[:-1])
sys.path.append(path)

from Analytics.predict_indicators import number_of_goals_probabilities, \
    match_result_probabilities
from Analytics.models.team import Team, Player
from Analytics.models.game_indicators import GameIndicators, TeamIndicators


class SetContent:
    def __init__(self, match_info, ui):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db_conn = self.client["football"]
        self.match = match_info
        self.ui = ui

        self.col_conn = self.db_conn["teams"]
        self.teams = [next(self.col_conn.find({"name": x}, {"_id": 0,
                                                            "datetime": 0}))
                      for x in [self.match["team1"]["name"],
                                self.match["team2"]["name"]]]

        self.teams[0]["name"] = self.teams[0]["name"].replace("_", " ")
        self.teams[1]["name"] = self.teams[1]["name"].replace("_", " ")
        self.match["team1"]["name"] = self.match["team1"]["name"].replace("_",
                                                                          " ")
        self.match["team2"]["name"] = self.match["team2"]["name"].replace("_",
                                                                          " ")

        self.home = [self.match["team1"]["xg"] / self.match["team1"]["sh"]
                     for _ in range(self.match["team1"]["sh"])]
        self.away = [self.match["team2"]["xg"] / self.match["team2"]["sh"]
                     for _ in range(self.match["team2"]["sh"])]
        self.setTeam(self.teams[0]["players"], self.ui.tableWidget_1)
        self.setTeam(self.teams[1]["players"], self.ui.tableWidget_2)
        self.setMatch([self.match["team1"], self.match["team2"]],
                      TeamIndicators, self.ui.tableWidget)
        self.setMatch(self.teams, Team, self.ui.tableWidget_3)
        self.setTabs()
        self.setLabels()
        self.setGraphics()

    def setTeam(self, players_list, table):
        for p in players_list[:11]:
            player_dict = Player(**p).dict()
            for second_index, val in enumerate(player_dict.values()):
                if second_index == 0:
                    table.cellWidget(players_list.index(p),
                                     second_index).setItemText(0, str(val))
                else:
                    if val in ("", {}, []):
                        val = "None"
                    item = QTableWidgetItem()
                    item.setData(QtCore.Qt.DisplayRole, val)
                    table.setItem(players_list.index(p), second_index, item)

    def setMatch(self, teams_data, model, table):
        for index, t in enumerate(teams_data):
            team_dict = model(**t).dict()
            for second_index, val in enumerate(team_dict.values()):
                if val in ("", {}, []):
                    val = "None"
                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, val)
                table.setItem(index, second_index, item)

    def setTabs(self):
        match_list_value = re.findall('\w+', self.match["match"])
        self.ui.tabWidget.setTabText(0, match_list_value[0][:-1].replace("_",
                                                                         " "))
        self.ui.tabWidget.setTabText(1, match_list_value[1][1:].replace("_",
                                                                        " "))

    def setLabels(self):
        match_list_value = re.findall('\w+', self.match["match"])
        self.ui.label_4.setText(match_list_value[0][-1]+"-"+
                                match_list_value[1][0])
        expected_result = match_result_probabilities(self.home, self.away)
        self.ui.label_3.setText(f"{expected_result[0]}-{expected_result[2]}")

    def setGraphics(self):
        flag = number_of_goals_probabilities(self.home)
        if len(flag) < 10:
            while len(flag) < 11:
                flag.append(flag[0])
        flag = flag[:10]
        g = self.ui.graphWidget
        g.clear()
        self.ui.graphWidget.setTitle(self.match['team1']['name'])
        g.plot(self.ui.probabilities, flag, pen=self.ui.red, symbol="o",
               symbolSize=6, symbolBrush="w")

        flag2 = number_of_goals_probabilities(self.away)
        if len(flag2) < 10:
            while len(flag2) < 11:
                flag2.append(flag2[0])
        flag2 = flag2[:10]
        g2 = self.ui.graphWidget2
        g2.clear()
        self.ui.graphWidget2.setTitle(self.match['team2']['name'])
        g2.plot(self.ui.probabilities, flag2, pen=self.ui.blue, symbol="o",
                symbolSize=6, symbolBrush="w")
