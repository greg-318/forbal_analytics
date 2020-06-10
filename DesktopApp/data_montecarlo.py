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
        self.list_games = self.count-self._games_num
        self.max_points = self.list_games * 3
