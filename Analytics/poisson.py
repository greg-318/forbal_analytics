import scipy.stats.distributions
import numpy as np

__doc__ = "Распределение Пуассона. Расчет по прошлому сезону"


def calculate_attack_defender(total_home_goals: int, total_away_goals: int, total_number_HG: int, total_number_AG: int,
                              total_goals_home_HT: int, number_home_games_HT: int,
                              miss_goals_away_AT: int, number_away_games_AT: int,
                              total_goals_away_AT: int, miss_goals_home_HT: int) -> list:
    """
    :param total_home_goals: количество забитых мячей всеми командами дома
    :param total_away_goals: количество забитых мячей всеми командами на выезде
    :param total_number_HG: количество домашних игр
    :param total_number_AG: количество гостевых игр
    :param total_goals_home_HT: всего забито домашней командой дома за прошлый сезон
    :param number_home_games_HT: всего сыграно игр домашней командой дома за прошлый сезон
    :param miss_goals_home_HT: всего пропущено домашней командой дома за прошлый сезон
    :param total_goals_away_AT: всего забито гостевой командой в гостях за прошлый сезон
    :param number_away_games_AT: всего сыграно игр гостевой командой в гостях за прошлый сезон
    :param miss_goals_away_AT: всего пропущено гостевой командой в гостях за прошлый сезон

    :return: массив вероятностей забить ровно k голов для домашней и гостевой команд
    """

    # Расчет для всех команд лиги
    av_goals_home = total_home_goals / total_number_HG  # сколько забили в среднем дома команды
    av_goals_away = total_away_goals / total_number_AG  # сколько забили в среднем в гостях команды

    av_conceded_home = total_away_goals / total_number_HG  # сколько пропустили в среднем дома команды
    av_conceded_away = total_home_goals / total_number_AG  # сколько пропустили в среднем в гостях команды

    # Расчет силы атаки домашней команды
    HT_attack = (total_goals_home_HT / number_home_games_HT) / av_goals_home

    # Расчет силы защиты гостей
    AT_defence = (miss_goals_away_AT / number_away_games_AT) / av_conceded_away

    # Расчет ожидаемого количества забитых голов домашней командой
    HT_attack_strength = HT_attack * AT_defence * av_goals_home

    # Расчет силы атаки гостей
    AT_attack = (total_goals_away_AT / number_away_games_AT) / av_goals_away

    # Расчет силы защиты домашней команды
    HT_defence = (miss_goals_home_HT / number_home_games_HT) / av_conceded_home

    # Расчет ожидаемого количества забитых голов гостей
    AT_attack_strength = AT_attack * HT_defence * av_goals_away

    # Распределение вероятности забить Х голов для домашней команды
    command_A = ((scipy.stats.distributions.poisson.pmf([0, 1, 2, 3, 4, 5, 6], HT_attack_strength)) * 100)
    p_goals_A = [round(np.float(x), 1) for x in command_A]

    # Распределение вероятности забить Х голов для гостевой команды
    command_B = ((scipy.stats.distributions.poisson.pmf([0, 1, 2, 3, 4, 5, 6], AT_attack_strength)) * 100)
    p_goals_B = [round(np.float(x), 1) for x in command_B]

    return [p_goals_A, p_goals_B]


def probability_score(prob: list) -> dict:
    """Расчитываем матрицу всех возможных результатов между двумя командами в пределах 5 мячей
        :param prob: список вероятностей для двух команд
        :return: словарь с процентами по каждому возможному результату матча
    """

    # Все вероятности победы П1 всухую: 1-0, 2-0, 3-0, 4-0, 5-0
    home_win_10 = tuple(round((prob[0][x] * prob[1][0]) / 100, 1) for x in range(1, 6))

    # Все вероятности победы П1 и пропущенном 1 мяче: 2-1, 3-1, 4-1, 5-1
    home_win_21 = tuple(round((prob[0][x] * prob[1][1]) / 100, 1) for x in range(2, 6))

    # Все вероятности победы П1 и пропущенных 2 мячах: 3-2, 4-2, 5-2
    home_win_32 = tuple(round((prob[0][x] * prob[1][2]) / 100, 1) for x in range(3, 6))

    # Все вероятности победы П1 и пропущенных 3 мячах: 4-3, 5-3
    home_win_43 = tuple(round((prob[0][x] * prob[1][3]) / 100, 1) for x in range(4, 6))

    # Все вероятности победы П1 и пропущенных 4 мячах: 5-4
    home_win_54 = tuple(round((prob[0][x] * prob[1][4]) / 100, 1) for x in range(5, 6))

    # Все вероятности ничьи: 0-0, 1-1, 2-2, 3-3, 4-4, 5-5
    draw = tuple(round((prob[0][x] * prob[1][x]) / 100, 1) for x in range(0, 6))

    # Все вероятности победы П2 всухую: 0-1, 0-2, 0-3, 0-4, 0-5
    away_win_01 = tuple(round((prob[0][0] * prob[1][x]) / 100, 1) for x in range(1, 6))

    # Все вероятности победы П2 и пропущенном 1 мяче: 1-2, 1-3, 1-4, 1-5
    away_win_12 = tuple(round((prob[0][1] * prob[1][x]) / 100, 1) for x in range(2, 6))

    # Все вероятности победы П2 и пропущенных 2 мячах: 2-3, 2-4, 2-5
    away_win_23 = tuple(round((prob[0][2] * prob[1][x]) / 100, 1) for x in range(3, 6))

    # Все вероятности победы П2 и пропущенных 3 мячах: 3-4, 3-5
    away_win_34 = tuple(round((prob[0][3] * prob[1][x]) / 100, 1) for x in range(4, 6))

    # Все вероятности победы П2 и пропущенных 4 мячах: 4-5
    away_win_45 = tuple(round((prob[0][4] * prob[1][x]) / 100, 1) for x in range(5, 6))

    return {'home_win_10': home_win_10, 'home_win_21': home_win_21, 'home_win_32': home_win_32,
            'home_win_43': home_win_43,
            'home_win_54': home_win_54,
            'draw': draw,
            'away_win_01': away_win_01, 'away_win_12': away_win_12, 'away_win_23': away_win_23,
            'away_win_34': away_win_34,
            'away_win_45': away_win_45,
            }
