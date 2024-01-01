from typer import Typer
from enum import Enum

from models import Algo

from ScheduleAlgo.Scheduler import Scheduler

app = Typer()


@app.command()
def main(number: int, algo: Algo):
    # print(f'Number: {number}, algo: {algo.value}')
    at = []
    cbt = []
    print("Give the processes information with this format:\n AT CBT\nex:\n 0 5")
    for i in range(1, number+1):
        at_i, cbt_i = map(int, input(f"Process {i} info: ").split())
        at.append(at_i)
        cbt.append(cbt_i)

    sch = Scheduler(algo, at, cbt)
    sch.calculate()


if __name__ == "__main__":
    app()
