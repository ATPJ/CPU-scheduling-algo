from enum import Enum


class Algo(str, Enum):
    fcfs = "FCFS"
    spn = "SPN"
    hrrn = "HRRN"
    rr = "RR"


class Process:
    def __init__(self, name: str, at: int, cbt: int) -> None:
        self.name = name
        self.at = at
        self.cbt = cbt
        self.visited = False
        self.start_time = None
        self.end_time = None
        self.waiting_time = None
        self.total_time = None

    def set_times(self, start_time, end_time, waiting_time, total_time):
        self.start_time = start_time
        self.end_time = end_time
        self.waiting_time = waiting_time
        self.total_time = total_time

    def set_rpr(self, rpr: float):
        self.rpr = rpr

    def make_rr_process(self):
        self.start_time = []
        self.end_time = []

    def __repr__(self) -> str:
        return f"<P: {self.name}, st: {self.start_time}, end: {self.end_time}>"
