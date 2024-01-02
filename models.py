from enum import Enum


class Algo(str, Enum):
    fcfs = "FCFS"
    spn = "SPN"
    hrrn = "HRRN"


class Process:
    def __init__(self, name: str, at: int, cbt: int) -> None:
        self.name = name
        self.at = at
        self.cbt = cbt
        self.visited = False

    def set_times(self, start_time, end_time, waiting_time, total_time):
        self.start_time = start_time
        self.end_time = end_time
        self.waiting_time = waiting_time
        self.total_time = total_time
