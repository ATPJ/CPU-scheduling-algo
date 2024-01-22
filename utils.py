from models import Process, Algo


def get_and_make_process(number: int) -> list[Process]:
    processes = []
    print("Give the processes information with this format: AT CBT\nex: 0 5")
    for i in range(1, number+1):
        at_i, cbt_i = map(int, input(f"Process {i} info: ").split())
        p = Process(i, at_i, cbt_i)
        processes.append(p)

    return processes


def make_process_list_with_same_info(processes_info: list[tuple]) -> list[Process]:
    processes = []
    for idx, p in enumerate(processes_info):
        processes.append(Process(idx+1, p[0], p[1]))

    return processes


def making_compare_table(data: dict):
    print("    Algo Name    |    Average Waiting Time    |    Average Total Time    ")
    print("-------------------------------------------------------------------------")
    for algo in (Algo.fcfs, Algo.spn, Algo.hrrn, Algo.rr, Algo.srtf):
        formated_name = str(algo.value.zfill(4)).replace("0", " ") + (" "*5)
        formated_avg_wt = str(data[algo]['avg_wt']).zfill(10).replace("0", " ") + (" "*10)
        formated_avg_tt = str(data[algo]['avg_tt']).zfill(9).replace("0", " ") + (" "*9)
        print("                 |                            |                          ")
        print(f"    {formated_name}    |    {formated_avg_wt}    |    {formated_avg_tt}    ")
        print("                 |                            |                          ")
