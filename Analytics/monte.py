from montecarlo.montecarlo import montecarlo
from random import random


def final_points(g):
    """

    Args:
        score:
        g:

    Returns:

    """

    points = g['points']
    for n in range(0, g['games']):
        result = random()
        if result <= g['winpct']:
            points += 3
        elif result <= g['drawpct'] + g['winpct']:
            points += 1
    if points > 54:
        return True
    else:
        return False


def setup_team_one(team, pts, games, winpct, drawpct, score) -> dict:
    """

    Args:
        team: Название домашней команды
        pts: Количество набранных очков
        games: Количество оставшихся игр
        winpct: процент выигранных матчей за сезон (выигранные матчи / всего матчей)
        drawpct: процент матчей сыгранных вничью за сезон (количество ничьих / всего матчей)

    Returns: словарь с данными для расчета вероятности набрать Х очков за оставшиеся игры

    """
    return {'team': team, 'points': pts, 'games': games, 'winpct': winpct, 'drawpct': drawpct, 'score': score}


# def setup_team_two(team: str, pts: int, games: int, winpct: float, drawpct: float) -> dict:
#     """
#
#     Args:
#         team: Название гостевой команды
#         pts: Количество набранных очков
#         games: Количество оставшихся игр
#         winpct: процент выигранных матчей за сезон (выигранные матчи / всего матчей)
#         drawpct: процент матчей сыгранных вничью за сезон (количество ничьих / всего матчей)
#
#     Returns: словарь с данными для расчета вероятности набрать Х очков за оставшиеся игры
#
#     """
#     return {'team': team, 'points': pts, 'games': games, 'winpct': winpct, 'drawpct': drawpct}


mc = montecarlo(final_points, setup=setup_team_one(team='One', pts=43, games=4, winpct=0.54, drawpct=0.24, score=50))
mc.run(iterations=300000)
#
# mc = montecarlo(final_points, setup=setup_team_two)
# mc.run(iterations=300000)
