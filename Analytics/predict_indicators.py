import itertools
import numpy as np

__doc__ = "Теорема Бернулли. Работаем с функцией match_result_probabilities "

NUMBER_OF_GOALS = 10


def number_of_goals_probabilities(p_shots: list) -> list:
    """
    :param p_shots: array or list: вероятность для каждого удара, что он станет голом
    :return: массив вероятностей забить ровно k голов
    >>> number_of_goals_probabilities([0.1, 0.1])
    array([0.81 0.18 0.01])
    >>> number_of_goals_probabilities([0.8, 0.2, 0.2])
    array([0.128 0.576 0.264 0.032])
    """
    p_shots = np.sort(np.asarray(p_shots, dtype=np.float64))
    p_compl = 1.0 - p_shots

    all_idx = set(range(len(p_shots)))

    p_goals = np.zeros(min(len(p_shots), NUMBER_OF_GOALS) + 1)

    for k in range(len(p_goals)):
        if k > 5:
            binom_nom = len(p_shots) - np.arange(k)
            binom_den = k - np.arange(k)
            max_proba = np.prod(binom_nom * p_shots[-k:] / binom_den) * np.prod(p_compl[:-k])
            max_proba_for_greater_k = max_proba * 3

            if max_proba_for_greater_k < 1e-3:
                p_goals_int = [int(str(round(i, 2)).split('.')[1]) for i in p_goals]
                return p_goals_int

        for idx_scored in itertools.combinations(range(len(p_shots)), k):
            scored_proba = np.prod(p_shots[list(idx_scored)])
            idx_missed = list(all_idx - set(idx_scored))
            missed_proba = np.prod(p_compl[idx_missed])

            p_goals[k] += scored_proba * missed_proba

            p_goals_int = [int(str(round(i, 2)).split('.')[1]) for i in p_goals]
    return p_goals_int


def match_result_probabilities(p_shots_home: list, p_shots_away: list) -> list:
    """
    :param p_shots_home: array or list: вероятность, что каждый удар хозяев будет забит (xG home)
    :param p_shots_away: array or list: вероятность, что каждый удар гостей будет забит (xG away)
    :return: массив размера 3 с вероятностями (победа хозяев, ничья, победа гостей)
    >>> match_result_probabilities([0.4], [0.3])
    array([ 0.28,  0.54,  0.18])
    >>> match_result_probabilities([0.1, 0.1, 0.1], [0.2, 0.1])
    array([ 0.2024,  0.5886,  0.209 ])
    """
    p_home_float = number_of_goals_probabilities(p_shots_home)
    p_home = [round(i, 2) for i in p_home_float]
    p_away_float = number_of_goals_probabilities(p_shots_away)
    p_away = [round(i, 2) for i in p_away_float]

    p_home_win = 0.
    p_draw = 0.
    p_away_win = 0.
    for goals_home in range(len(p_home)):
        for goals_away in range(len(p_away)):
            p = p_home[goals_home] * p_away[goals_away]
            if goals_home > goals_away:
                p_home_win += p
            elif goals_home < goals_away:
                p_away_win += p
            else:
                p_draw += p

    p_home_win = int(p_home_win / 100 + .5)
    p_away_win = int(p_away_win / 100 + .5)
    p_draw = int(p_draw / 100 + .5)

    if sum([p_home_win, p_away_win, p_draw]) != 100:
        p_draw += 1




    return np.round([p_home_win, p_draw, p_away_win], 4).tolist()
