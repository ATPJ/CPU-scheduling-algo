import matplotlib.pyplot as plt

from collections import deque

from models import Algo, Process


class Scheduler:

    def __init__(self, algo: Algo, processes: list[Process], qunt: int = 10) -> None:
        self.algo = algo
        self.processes = processes
        self.N = len(processes)
        self.avg_waiting_time = 0
        self.avg_total_time = 0
        self.qunt = qunt

    def calculate(self):
        match self.algo:
            case Algo.fcfs:
                self.__fcfs()
            case Algo.spn:
                self.__spn()
            case Algo.hrrn:
                self.__hrrn()
            case Algo.rr:
                self.__rr()
            case Algo.srtf:
                self.__srtf()

        self.__caluclate_avg()
        if self.algo == Algo.rr or self.algo == Algo.srtf: self.__make_pr_plot()
        else: self.__make_plot()

    def __fcfs(self):
        last_p: Process = None
        for _ in range(self.N):
            p = self.__get_min_at_process()
            if last_p is None: start = p.at
            else: start = last_p.end_time
            end = start + p.cbt
            wait_t = start - p.at
            total_t = end - p.at

            p.set_times(start, end, wait_t, total_t)
            last_p = p

    def __spn(self):
        last_p: Process = None
        t = 0
        while self.__check_if_any_remain():
            ps = self.__find_all_process_with_atleaset_t_at(t)
            print(t, " and ", ps)
            # ps = sorted(ps, key=lambda k: (k.cbt, k.at))
            if len(ps) == 0:
                t += 1
                continue

            # for _ in range(len(ps)):
            p = self.__get_min_cbt_process(ps)
            if last_p is None: start = p.at
            else: start = last_p.end_time
            end = start + p.cbt
            wait_t = start - p.at
            total_t = end - p.at

            p.set_times(start, end, wait_t, total_t)
            last_p = p
            t = p.end_time

    def __hrrn(self):
        last_p: Process = None
        t = 0
        while self.__check_if_any_remain():
            ps = self.__find_all_process_with_atleaset_t_at(t)
            if len(ps) == 0:
                t += 1
                continue

            self.__calculate_rpr(ps, t)
            ps = sorted(ps, key=lambda k: (k.rpr, k.cbt), reverse=True)
            if len(ps) >= 2 and ps[0].rpr == ps[1].rpr:
                ps = list(reversed(ps))
            p = ps[0]
            if last_p is None: start = p.at
            else: start = last_p.end_time
            end = start + p.cbt
            wait_t = start - p.at
            total_t = end - p.at

            p.set_times(start, end, wait_t, total_t)
            p.visited = True
            last_p = p
            t = p.end_time

    def __rr(self):
        for p in self.processes:
            p.make_rr_process()

        t = 0
        ps: deque = deque(self.__find_all_process_with_atleaset_t_at(t))
        ps = deque(sorted(ps, key=lambda k: k.at, reverse=True))
        while self.__check_if_any_remain():
            ps = self.__update_if_any_new(ps, t)
            if len(ps) == 0:
                t += 1
                continue

            p: Process = ps.pop()

            if p.cbt <= self.qunt:
                p.start_time.append(t)
                p.end_time.append(t + p.cbt)
                wait_t = p.start_time[0] - p.at
                total_t = p.end_time[-1] - p.at
                p.waiting_time = wait_t
                p.total_time = total_t
                p.visited = True
                t += p.cbt
            else:
                p.start_time.append(t)
                p.end_time.append(t + self.qunt)
                p.cbt = p.cbt - self.qunt
                ps.appendleft(p)
                if p.cbt == 0:
                    p.waiting_time = p.start_time[0] - p.at
                    p.total_time = p.end_time[-1] - p.at
                    p.visited = True
                t += self.qunt

    def __srtf(self):
        for p in self.processes:
            p.make_rr_process()

        t = 0
        ps: deque = deque(self.__find_all_process_with_atleaset_t_at(t))
        ps = deque(sorted(ps, key=lambda k: k.at, reverse=True))
        while self.__check_if_any_remain():
            ps = self.__update_if_any_new(ps, t)
            if len(ps) == 0:
                t += 1
                continue

            ps = deque(sorted(ps, key=lambda k: k.cbt, reverse=True))
            p: Process = ps.pop()

            p.start_time.append(t)
            p.end_time.append(t + 1)
            p.cbt -= 1
            if p.cbt == 0:
                for i in range(len(p.start_time) - 1):
                    if i == 0:
                        p.waiting_time += (p.start_time[i] - p.at)
                    else:
                        p.waiting_time += (p.start_time[i+1] - p.end_time[i])
                p.total_time = p.end_time[-1] - p.at
                p.visited = True

            t += 1

    def __get_min_at_process(self) -> Process:
        value = 1000000000000000
        proc = None
        for p in self.processes:
            if p.at < value and p.visited == False:
                value = p.at
                proc = p

        proc.visited = True
        return proc

    def __get_min_cbt_process(self, processes: list[Process]) -> Process:
        value = 1000000000000000
        proc = None
        for p in processes:
            if p.cbt < value and p.visited == False:
                value = p.cbt
                proc = p

        proc.visited = True
        return proc

    def __find_all_process_with_atleaset_t_at(self, t: int) -> list[Process]:
        return [p for p in self.processes if p.at <= t and not p.visited]

    def __caluclate_avg(self):
        for p in self.processes:
            self.avg_waiting_time += p.waiting_time
            self.avg_total_time += p.total_time

        self.avg_waiting_time = self.avg_waiting_time / len(self.processes)
        self.avg_total_time = self.avg_total_time / len(self.processes)

    def __check_if_any_remain(self) -> bool:
        for p in self.processes:
            if not p.visited:
                return True

        return False

    def __calculate_rpr(self, ps: list[Process], t: int):
        for p in ps:
            wt = t - p.at
            current_rpr = float(wt) / float(p.cbt)
            p.set_rpr(current_rpr)

    def __update_if_any_new(self, ps: deque[Process], t: int) -> deque[Process]:
        ps = ps
        ps_tmp = self.__find_all_process_with_atleaset_t_at(t)
        ps_tmp = sorted(ps_tmp, key=lambda k: k.at, reverse=True)
        for p in ps_tmp:
            if p not in ps:
                ps.append(p)

        return ps

    def __debug(self):
        for p in self.processes:
            print(p)

    def __make_plot(self):
        # self.__debug()
        plt.figure(figsize=(12, 8))
        plt.yticks(range(len(self.processes) + 1))
        plt.xticks(range(200))
        plt.xlabel("Time")
        plt.ylabel("Process")

        for p in self.processes:
            plt.scatter(p.at, p.name, color='red', marker='x')
            plt.plot([p.start_time, p.end_time], [p.name, p.name])

        msg = f"Average Waiting Time: '{self.avg_waiting_time}' and  Average Total Time: '{self.avg_total_time}'"
        plt.figtext(0.5, 0.01, msg, wrap=True, horizontalalignment='center', fontsize=12)
        plt.show()

    def __make_pr_plot(self):
        plt.figure(figsize=(16, 8))
        plt.yticks(range(len(self.processes) + 1))
        plt.xticks(range(200))
        plt.xlabel("Time")
        plt.ylabel("Process")

        for p in self.processes:
            plt.scatter(p.at, p.name, color='red', marker='x')
            for i in range(len(p.start_time)):
                plt.plot([p.start_time[i], p.end_time[i]], [p.name, p.name], color=f"C{p.name}")

        msg = f"Average Waiting Time: '{self.avg_waiting_time}' and  Average Total Time: '{self.avg_total_time}'"
        plt.figtext(0.5, 0.01, msg, wrap=True, horizontalalignment='center', fontsize=12)
        plt.show()
