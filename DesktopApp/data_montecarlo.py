class Games:

    def __init__(self, count, games_num=0):
        self.count = count
        self.games_num = games_num

    @property
    def games_num(self):
        return self._games_num

    @games_num.setter
    def games_num(self, num):
        if not isinstance(num, int) or num > self.count:
            raise ValueError("Неверное значение")
        self._games_num = num
        self.list_games = tuple(range(self.count-self._games_num+1))
        self.max_points = tuple(range(max(self.list_games) * 3+1))
