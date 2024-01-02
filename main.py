from typer import Typer
from enum import Enum

from models import Algo, Process

from ScheduleAlgo.Scheduler import Scheduler

app = Typer()


@app.command()
def main(number: int, algo: Algo):
    # print(f'Number: {number}, algo: {algo.value}')
    processes = []
    print("Give the processes information with this format: AT CBT\nex: 0 5")
    for i in range(1, number+1):
        at_i, cbt_i = map(int, input(f"Process {i} info: ").split())
        p = Process(i, at_i, cbt_i)
        processes.append(p)

    sch = Scheduler(algo, processes)
    sch.calculate()


if __name__ == "__main__":
    app()
