

played = [27,89,54,78,9,1,6,3,9,10,1,2,13,4,15,1,18,19,20]
nou_played = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20]

games = 10


def play(value_games, value_played, value_nouplayed):
    list_play = []

    for i in range(value_games):
        list_play.append(value_played[i])

    if len(list_play) != value_played:
        for f in value_nouplayed[value_games:]:
            list_play.append(f)
    print(list_play)


play(games, played, nou_played)