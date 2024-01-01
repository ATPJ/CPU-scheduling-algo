import matplotlib.pyplot as plt

from models import Algo


class Scheduler:
    def __init__(self, algo: Algo, at: list[int], cbt: list[int]) -> None:
        self.algo = algo
        self.at = at
        self.cbt = cbt
        self.start_time = []
        self.end_time = []
        self.waiting_time = []
        self.total_time = []
        self.avg_waiting_time = None
        self.avg_total_time = None

    def calculate(self):
        match self.algo:
            case Algo.fcfs:
                self.__fcfs()
            case Algo.spn:
                self.__spn()
            case Algo.hrrn:
                self.__hrrn()
        self.make_plot()

    def __fcfs(self):
        pass

    def __spn(self):
        pass

    def __hrrn(self):
        pass

    def __get_min_index_and_value(self, *args) -> tuple(int, int):
        value = 1000000000000000
        index = -1
        for idx, v in enumerate(args):
            if v < value:
                value = v
                index = idx
        return (index, value)

    def make_plot(self):
        plt.yticks(range(len(self.start_time) + 1))
        plt.xticks(range(20))
        for i in range(len(self.start_time)):
            plt.scatter(self.at[i], i+1, color='red', marker='x')
            plt.plot([self.start_time[i], self.end_time[i]], [i+1, i+1])
        plt.show()
