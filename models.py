from enum import Enum


class Algo(str, Enum):
    fcfs = "FCFS"
    spn = "SPN"
    hrrn = "HRRN"
