import sys
sys.path.append("D:\Мои документы\Desktop\R&D\Analytics")
from models import player, team, game_indicators
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox

data = {
    "Atletico_Madrid_1-0_Getafe": {
        "Atletico_Madrid": {
            "player_list": [
                "Jan Oblak",
                "Kieran Trippier",
                "Stefan Savic",
                "Giménez",
                "Renan Lodi",
                "Thomas Partey",
                "Koke",
                "Saúl Ñíguez",
                "Thomas Lemar",
                "João Félix",
                "Álvaro Morata",
                "Vitolo",
                "Marcos Llorente",
                "Mario Hermoso",
            ]
        },
        "Getafe": {
            "player_list": [
                "David Soria",
                "Nyom",
                "Bruno",
                "Djené Dakonam",
                "Leandro Cabrera",
                "Damián Suárez",
                "Faycal Fajr",
                "Mauro Arambarri",
                "Marc Cucurella",
                "Jorge Molina",
                "Jaime Mata",
                "Ángel",
                "Raúl García",
                "Enric Gallego",
            ]
        }
    },
    "Leganes_0-1_Atletico_Madrid": {
        "Leganes": {
            "player_list": [
                "Juan Soriano",
                "Roberto Rosales",
                "Dimitrios Siovas",
                "Kenneth Omeruo",
                "Rodrigo Tarín",
                "Jonathan Silva",
                "Roque Mesa",
                "Rubén Pérez",
                "Eraso",
                "Martin Braithwaite",
                "Youssef En - Nesyri",
                "Unai Bustinza",
                "José Arnáiz",
                "Javier Avilés",
            ]
        },
        "Atletico_Madrid": {
            "player_list": [
                "Jan Oblak",
                "Stefan Savic",
                "Mario Hermoso",
                "Giménez",
                "Thomas Partey",
                "Kieran Trippier",
                "Thomas Lemar",
                "Koke",
                "Saúl Ñíguez",
                "João Félix",
                "Álvaro Morata",
                "Felipe",
                "Marcos Llorente",
                "Vitolo",
            ]
        }
    },
    "Arsenal_2-1_Burnley": {
        "Arsenal": {
            "player_list": [
                "Bernd Leno",
                "Ainsley Maitland - Niles",
                "David Luiz",
                "Sokratis",
                "Nacho Monreal",
                "Matteo Guendouzi",
                "Joe Willock",
                "Pierre - Emerick Aubameyang",
                "Dani Ceballos",
                "Reiss Nelson",
                "Alexandre Lacazette",
                "Sead Kolasinac",
                "Lucas Torreira",
                "Nicolas Pepe",
            ]
        },
        "Burnley": {
            "player_list": [
                "Nick Pope",
                "Matthew Lowton",
                "Ben Mee",
                "James Tarkowski",
                "Erik Pieters",
                "Johann Berg Gudmundsson",
                "Ashley Westwood",
                "Jack Cork",
                "Dwight McNeil",
                "Chris Wood",
                "Ashley Barnes",
                "Aaron Lennon",
                "Jay Rodriguez",
            ]
        }
    },
    "Burnley_3-0_Southampton": {
        "Burnley": {
            "player_list": [
                "Nick Pope",
                "Matthew Lowton",
                "Ben Mee",
                "James Tarkowski",
                "Erik Pieters",
                "Johann Berg Gudmundsson",
                "Jack Cork",
                "Ashley Westwood",
                "Dwight McNeil",
                "Chris Wood",
                "Ashley Barnes",
                "Jay Rodriguez",
                "Aaron Lennon",
            ]
        },
        "Southampton": {
            "player_list": [
                "Angus Gunn",
                "Jannik Vestergaard",
                "Jan Bednarek",
                "Jack Stephens",
                "Yan Valery",
                "Ryan Bertrand",
                "Oriol Romeu",
                "James Ward - Prowse",
                "Danny Ings",
                "Nathan Redmond",
                "Che Adams",
                "Pierre - Emile Højbjerg",
                "Michael Obafemi",
                "Sofiane Boufal",
            ]
        }
    },
    "RasenBallsport_Leipzig_2-1_Eintracht_Frankfurt": {
        "RasenBallsport_Leipzig": {
            "player_list": [
                "Péter Gulácsi",
                "Nordi Mukiele",
                "Ibrahima Konaté",
                "Willi Orban",
                "Lukas Klostermann",
                "Marcel Halstenberg",
                "Christopher Nkunku",
                "Diego Demme",
                "Marcel Sabitzer",
                "Yussuf Poulsen",
                "Timo Werner",
                "Konrad Laimer",
                "Emil Forsberg",
                "Ademola Lookman",
            ]
        },
        "Eintracht_Frankfurt": {
            "player_list": [
                "Kevin Trapp",
                "David Abraham",
                "Evan Ndicka",
                "Makoto Hasebe",
                "Erik Durm",
                "Dominik Kohr",
                "Sebastian Rode",
                "Filip Kostic",
                "Daichi Kamada",
                "Gonçalo Paciência",
                "Dejan Joveljic",
                "Almamy Touré",
                "Jonathan de Guzmán",
                "Timothy Chandler",
            ]
        }
    },
    "Union_Berlin_0-4_RasenBallsport_Leipzig": {
        "Union_Berlin": {
            "player_list": [
                "Rafal Gikiewicz",
                "Christopher Trimmel",
                "Keven Schlotterbeck",
                "Marvin Friedrich",
                "Christopher Lenz",
                "Robert Andrich",
                "Grischa Prömel",
                "Suleiman Abdullahi",
                "Christian Gentner",
                "Marius Bülter",
                "Sebastian Andersson",
                "Sebastian Polter",
                "Sheraldo Becker",
                "Anthony Ujah",
            ]
        },
        "RasenBallsport_Leipzig": {
            "player_list": [
                "Péter Gulácsi",
                "Ibrahima Konaté",
                "Nordi Mukiele",
                "Willi Orban",
                "Lukas Klostermann",
                "Marcel Halstenberg",
                "Diego Demme",
                "Kevin Kampl",
                "Marcel Sabitzer",
                "Yussuf Poulsen",
                "Timo Werner",
                "Konrad Laimer",
                "Christopher Nkunku",
                "Emil Forsberg",
            ]
        }
    },
    "Cagliari_1-2_Inter": {
        "Cagliari": {
            "player_list": [
                "Robin Olsen",
                "Ragnar Klavan",
                "Luca Ceppitelli",
                "Fabio Pisacane",
                "Nahitan Nández",
                "Luca Pellegrini",
                "Radja Nainggolan",
                "Marko Rog",
                "Artur Ionita",
                "João Pedro",
                "Alberto Cerri",
                "Lucas Castro",
                "Giovanni Simeone",
                "Luca Cigarini",
            ]
        },
        "Inter": {
            "player_list": [
                "Samir Handanovic",
                "Danilo D'Ambrosio",
                "Andrea Ranocchia",
                "Milan Skriniar",
                "Antonio Candreva",
                "Kwadwo Asamoah",
                "Marcelo Brozovic",
                "Stefano Sensi",
                "Matías Vecino",
                "Lautaro Martínez",
                "Romelu Lukaku",
                "Matteo Politano",
                "Nicolò Barella",
                "Diego Godín",
            ]
        }
    },
    "Inter_4-0_Lecce": {
        "Inter": {
            "player_list": [
                "Samir Handanovic",
                "Danilo D'Ambrosio",
                "Andrea Ranocchia",
                "Milan Skriniar",
                "Antonio Candreva",
                "Kwadwo Asamoah",
                "Marcelo Brozovic",
                "Stefano Sensi",
                "Matías Vecino",
                "Lautaro Martínez",
                "Romelu Lukaku",
                "Matteo Politano",
                "Roberto Gagliardini",
                "Nicolò Barella",
            ]
        },
        "Lecce": {
            "player_list": [
                "Gabriel",
                "Andrea Rispoli",
                "Luca Rossettini",
                "Fabio Lucioni",
                "Marco Calderoni",
                "Panagiotis Tachtsidis",
                "Jacopo Petriccione",
                "Filippo Falco",
                "Zan Majer",
                "Andrea La Mantia",
                "Gianluca Lapadula",
                "Diego Farias",
                "Marco Mancosu",
                "Romario Benzar",
            ]
        }
    },
    "Toulouse_1-0_Dijon": {
        "Toulouse": {
            "player_list": [
                "Baptiste Reynet",
                "Steven Moreira",
                "Kelvin Adou",
                "Bafode Diakite",
                "Issiaga Sylla",
                "William Vainqueur",
                "Ibrahim Sangare",
                "Mathieu Dossevi",
                "Jean - Victor Makengo",
                "Max Gradel",
                "Efthymios Koulouris",
                "Quentin Boisgard",
                "Kalidou Sidibe",
                "Wesley Said",
            ]
        },
        "Dijon": {
            "player_list": [
                "Rúnar Alex Rúnarsson",
                "Mickaël Alphonse",
                "Senou Coulibaly",
                "Bruno Ecuele Manga",
                "Fouad Chafik",
                "Wesley Lautoa",
                "Mama Baldé",
                "Romain Amalfitano",
                "Didier Ndong",
                "Benjamin Jeannot",
                "Júlio Tavares",
                "Frederic Sammaritano",
                "Jules Keita",
                "Bryan Soumaré",
            ]
        }
    },
    "Dijon_1-2_Saint-Etienne": {
        "Dijon": {
            "player_list": [
                "Rúnar Alex Rúnarsson",
                "Mickaël Alphonse",
                "Senou Coulibaly",
                "Bruno Ecuele Manga",
                "Fouad Chafik",
                "Romain Amalfitano",
                "Didier Ndong",
                "Mama Baldé",
                "Benjamin Jeannot",
                "Frederic Sammaritano",
                "Júlio Tavares",
                "Enzo Loiodice",
                "Jules Keita",
                "Bryan Soumaré",
            ]
        },
        "Saint-Etienne": {
            "player_list": [
                "Stéphane Ruffier",
                "Mathieu Debuchy",
                "Loic Perrin",
                "Harold Moukoudi",
                "Miguel Trauco",
                "Yann M'Vila",
                "Jean Eudes Aholou",
                "Romain Hamouma",
                "Ryad Boudebouz",
                "Denis Bouanga",
                "Wahbi Khazri",
                "Arnaud Nordin",
                "Zaydou Youssef",
                "Robert Beric",
            ]
        }
    },
    "FC_Ufa_2-3 FC_Krasnodar": {
        "FC_Ufa": {
            "player_list": [
                "Aleksey Chernov",
                "Jimmy Tabidze",
                "Aleksandr Putsko",
                "Bojan Jokic",
                "Aleksandr Sukhov",
                "Azer Aliev",
                "Catalin Carp",
                "Daniil Fomin",
                "Olivier Thill",
                "Sly",
                "Andrei Kozlov",
                "Vyacheslav Krotov",
                "Dmitri Sysuev",
                "Azamat Zaseev",
            ]
        },
        "FC_Krasnodar": {
            "player_list": [
                "Matvey Safonov",
                "Sergei Petrov",
                "Aleksandr Martynovich",
                "Uros Spajic",
                "Cristian Ramírez",
                "Tonny Vilhena",
                "Ruslan Kambolov",
                "Kristoffer Olsson",
                "Younes Namli",
                "Ari",
                "Wanderson",
                "Jón Gudni Fjóluson",
                "Magomed - Shapi Suleymanov",
                "Ivan Ignatyev",
            ]
        }
    },
    "FK_Akhmat_1-0_FC_Krasnodar": {
        "FK_Akhmat": {
            "player_list": [
                "Evgeni Gorodov",
                "Rizvan Utsiev",
                "Zoran Nizic",
                "Andrey Semenov",
                "Wilker Ángel",
                "Evgeny Kharin",
                "Ismael",
                "Anton Shvets",
                "Bernard Berisha",
                "Oleg Ivanov",
                "Ablae Mbengue",
                "Odise Roshi",
                "Damian Szymanski",
                "Andrés Ponce",
            ]
        },
        "FC_Krasnodar": {
            "player_list": [
                "Matvey Safonov",
                "Sergei Petrov",
                "Aleksandr Martynovich",
                "Uros Spajic",
                "Dmitriy Stotskiy",
                "Tonny Vilhena",
                "Ruslan Kambolov",
                "Kristoffer Olsson",
                "Wanderson",
                "Ari",
                "Younes Namli",
                "Cristian Ramírez",
                "Magomed - Shapi Suleymanov",
                "Ivan Ignatyev",
            ]
        }
    },
}


class setContent:
    def __init__(self, match, ui):
        self.match = match.replace(" ", "_")
        self.ui = ui
        self.teamValue1, self.teamValue2 = [data[self.match][team] for team in data[self.match]]
        self.setTeamOne()
        self.setTeamTwo()
        self.setIndicatorsMatch()
        self.setResultMatch()

    def setTeamOne(self):
        for index, p in enumerate(self.teamValue1["player_list"]):
            if index >= 11:
                break
            player_dict = player.Player(player=p)
            indicators_player = player_dict.dict()
            for second_index, (_, val) in enumerate(indicators_player.items()):
                if second_index == 0:
                    self.ui.tableWidget_1.cellWidget(index, second_index).setItemText(0, str(val))
                    continue
                if second_index != 23:
                    if val in ("", {}, []):
                        val = "None"
                    self.ui.tableWidget_1.setItem(index, second_index, QTableWidgetItem(str(val)))

    def setTeamTwo(self):
        for index, p in enumerate(self.teamValue2["player_list"]):
            if index >= 11:
                break
            player_dict = player.Player(player=p)
            indicators_player = player_dict.dict()
            for second_index, (_, val) in enumerate(indicators_player.items()):
                if second_index == 0:
                    self.ui.tableWidget_2.cellWidget(index, second_index).setItemText(0, str(val))
                    continue
                if second_index != 23:
                    if val in ("", {}, []):
                        val = "None"
                    self.ui.tableWidget_2.setItem(index, second_index, QTableWidgetItem(str(val)))

    def setIndicatorsMatch(self):
        for index, t in enumerate(data[self.match]):
            team_dict = game_indicators.GameIndicators("", {}, {})
            team_dict.team1["name"] = t.replace("_", " ")
            indicators_team = team_dict.team1
            for second_index, (_, val) in enumerate(indicators_team.items()):
                if second_index != 10:
                    if val in ("", {}, []):
                        val = "None"
                    self.ui.tableWidget.setItem(index, second_index, QTableWidgetItem(str(val)))

    def setResultMatch(self):
        for index, t in enumerate(data[self.match]):
            team_dict = team.Team(name=t.replace("_", " "))
            indicators_team = team_dict.dict()
            for second_index, (_, val) in enumerate(indicators_team.items()):
                if second_index != 24:
                    if val in ("", {}, []):
                        val = "None"
                    self.ui.tableWidget_3.setItem(index, second_index, QTableWidgetItem(str(val)))


# print(data["Inter_4-0_Lecce"][0])
