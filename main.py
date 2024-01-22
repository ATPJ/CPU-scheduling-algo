import typer

from typing_extensions import Annotated
from typing import Optional

from models import Algo, Process
from ScheduleAlgo.Scheduler import Scheduler

app = typer.Typer()


@app.command()
def main(number: int, algo: Algo, time_slice: Annotated[Optional[int], typer.Argument()] = 10):
    # print(f'Number: {number}, algo: {algo.value}')
    processes = []
    print("Give the processes information with this format: AT CBT\nex: 0 5")
    for i in range(1, number+1):
        at_i, cbt_i = map(int, input(f"Process {i} info: ").split())
        p = Process(i, at_i, cbt_i)
        processes.append(p)

    sch = Scheduler(algo, processes, qunt=time_slice)
    sch.calculate()


if __name__ == "__main__":
    app()
