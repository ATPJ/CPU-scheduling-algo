import matplotlib.pyplot as plt

from models import Algo, Process


class Scheduler:
    def __init__(self, algo: Algo, processes: list[Process]) -> None:
        self.algo = algo
        self.processes = processes
        self.N = len(processes)
        self.avg_waiting_time = 0
        self.avg_total_time = 0

    def calculate(self):
        match self.algo:
            case Algo.fcfs:
                self.__fcfs()
            case Algo.spn:
                self.__spn()
            case Algo.hrrn:
                self.__hrrn()

        self.__caluclate_avg()
        self.__make_plot()

    def __fcfs(self):
        last_p: Process = None
        for _ in range(self.N):
            p = self.__get_min_process()
            if last_p is None: start = p.at
            else: start = last_p.end_time
            end = start + p.cbt
            wait_t = start - p.at
            total_t = end - p.at

            p.set_times(start, end, wait_t, total_t)
            last_p = p

    def __spn(self):
        pass

    def __hrrn(self):
        pass

    def __get_min_process(self) -> Process:
        value = 1000000000000000
        proc = None
        for p in self.processes:
            if p.at < value and p.visited == False:
                value = p.at
                proc = p

        proc.visited = True
        return proc

    def __caluclate_avg(self):
        for p in self.processes:
            self.avg_waiting_time += p.waiting_time
            self.avg_total_time += p.total_time

        self.avg_waiting_time = self.avg_waiting_time / len(self.processes)
        self.avg_total_time = self.avg_total_time / len(self.processes)

    def __make_plot(self):
        plt.figure(figsize=(12, 8))
        plt.yticks(range(len(self.processes) + 1))
        plt.xticks(range(200))
        plt.xlabel("Time")
        plt.ylabel("Process")

        for p in self.processes:
            plt.scatter(p.at, p.name, color='red', marker='x')
            plt.plot([p.start_time, p.end_time], [p.name, p.name])

        plt.show()
