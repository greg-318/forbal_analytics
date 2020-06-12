import itertools
import numpy as np

__doc__ = "Теорема Бернулли. Работаем с функцией match_result_probabilities"

NUMBER_OF_GOALS = 6


class GoalsMatch:

    def number_of_goals_probabilities(self, p_shots: list) -> list:
        self.p_shots = p_shots
        self.p_shots = np.sort(np.asarray(self.p_shots, dtype=np.float64))
        p_compl = 1.0 - self.p_shots

        all_idx = set(range(len(self.p_shots)))

        p_goals = np.zeros(min(len(self.p_shots), NUMBER_OF_GOALS) + 1)

        for k in range(len(p_goals)):
            if k > 5:
                binom_nom = len(p_shots) - np.arange(k)
                binom_den = k - np.arange(k)
                max_proba = np.prod(binom_nom * self.p_shots[-k:] / binom_den) * np.prod(p_compl[:-k])
                max_proba_for_greater_k = max_proba * 3

                if max_proba_for_greater_k < 1e-3:
                    p_goals_int = [round((round(np.float(x), 2)) * 100) for x in p_goals]
                    p_goals_int += [0] * (6 - len(p_goals_int))
                    return p_goals_int

            for idx_scored in itertools.combinations(range(len(self.p_shots)), k):
                scored_proba = np.prod(self.p_shots[list(idx_scored)])
                idx_missed = list(all_idx - set(idx_scored))
                missed_proba = np.prod(p_compl[idx_missed])

                p_goals[k] += scored_proba * missed_proba

                p_goals_int = [round((round(np.float(x), 2)) * 100) for x in p_goals]
                p_goals_int += [0] * (6 - len(p_goals_int))

        return p_goals_int

    def match_result_probabilities(self, p_shots_home: list, p_shots_away: list) -> list:
        """
        :return: массив размера 3 с вероятностями (победа хозяев, ничья, победа гостей)
        """

        self.p_shots_home = p_shots_home
        self.p_shots_away = p_shots_away

        if len(self.p_shots_home) > 12:
            self.p_shots_home = self.p_shots_home[:12]
        if len(self.p_shots_away) > 12:
            self.p_shots_away = self.p_shots_away[:12]

        if len(self.p_shots_home) <= 1:
            if self.p_shots_home[0] < 0.11:
                self.p_shots_home[0] = 0.11

        if len(self.p_shots_away) <= 1:
            if self.p_shots_away[0] < 0.11:
                self.p_shots_away[0] = 0.11

        # Можно вызвать метод number_of_goals_probabilities создав экземпляр класса
        self.p_home = self.number_of_goals_probabilities(self.p_shots_home)
        self.p_away = self.number_of_goals_probabilities(self.p_shots_away)

        p_home_win = 0.
        p_draw = 0.
        p_away_win = 0.
        for goals_home in range(len(self.p_home)):
            for goals_away in range(len(self.p_away)):
                p = self.p_home[goals_home] * self.p_away[goals_away]
                if goals_home > goals_away:
                    p_home_win += p
                elif goals_home < goals_away:
                    p_away_win += p
                else:
                    p_draw += p

        p_home_win = int(p_home_win / 100 + 0.5)
        p_away_win = int(p_away_win / 100 + 0.5)
        p_draw = int(p_draw / 100 + 0.5)

        if sum([p_home_win, p_away_win, p_draw]) < 100:
            p_draw += sum([p_home_win, p_away_win, p_draw])

        if sum([p_home_win, p_away_win, p_draw]) > 100:
            p_draw -= (sum([p_home_win, p_away_win, p_draw]) - 100)

        return [p_home_win, p_draw, p_away_win]
