import typer

from typing_extensions import Annotated
from typing import Optional

from models import Algo
from ScheduleAlgo.Scheduler import Scheduler
from utils import (get_and_make_process,
                   make_process_list_with_same_info,
                   making_compare_table)

app = typer.Typer()


@app.command(name='plot')
def main(number: int, algo: Algo, time_slice: Annotated[Optional[int], typer.Argument()] = 10):
    processes = get_and_make_process(number)
    sch = Scheduler(algo, processes, qunt=time_slice)
    sch.calculate()


@app.command(name='compare')
def compare(number: int, time_slice: Annotated[Optional[int], typer.Argument()] = 10,
            show_plot: bool = False):
    processes_info = []
    print("Give the processes information with this format: AT CBT\nex: 0 5")
    for i in range(1, number+1):
        at_i, cbt_i = map(int, input(f"Process {i} info: ").split())
        processes_info.append((at_i, cbt_i))

    data = {}
    for algo in (Algo.fcfs, Algo.spn, Algo.hrrn, Algo.rr, Algo.srtf):
        processes = make_process_list_with_same_info(processes_info)
        sch = Scheduler(algo, processes, qunt=time_slice)
        sch.calculate(show_plot)
        data[algo] = {'avg_wt': sch.avg_waiting_time, 'avg_tt': sch.avg_total_time}

    making_compare_table(data)


if __name__ == "__main__":
    app()
