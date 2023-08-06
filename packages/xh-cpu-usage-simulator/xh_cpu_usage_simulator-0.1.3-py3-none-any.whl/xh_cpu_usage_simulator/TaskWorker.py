import time

from xh_cpu_usage_simulator.MovingAvg import MovingAvg


def worker(index: int, d: dict, r: dict) -> [int, int]:
    bucket = MovingAvg(10)

    def do_something():
        bucket.insert(1)

    def get_time():
        t = time.time_ns()
        ms = t // 1_000_000
        s = ms // 1000
        return s, ms

    s, _ = get_time()

    task_to_run = int(d[f"{index}"])
    target = task_to_run
    mv = MovingAvg(10)
    while True:
        n_s, n_ms = get_time()
        if n_s != s:
            new_task_to_run = int(d[f"{index}"])
            # if task_to_run != new_task_to_run:
            #     print(f"[Worker {index}]Target to run updated from {task_to_run} -> {new_task_to_run}")
            # if target != 0:
            #     print(f"[Worker {index}] Completed {task_to_run - target}/{task_to_run} [{round(1- target/task_to_run, 2)} %]")

            completed = task_to_run - target
            mv.insert(completed)
            r.update({f"{index}-complete": round(mv.avg, 2)})

            task_to_run = new_task_to_run
            # print(f"[Worker {index}]Rest target")
            target = task_to_run
            s = n_s

        if target > 0:
            target -= 1
            do_something()  # payload
        elif target == 0:
            diff = (s + 1) * 1000 - n_ms
            # print(f"[Worker {index}]Taking {(n_ms - (s * 1000))} ms for {task_to_run} tasks [Sleep for {round(diff/1000, 4)} s]")
            if diff > 0:
                time.sleep(diff / 1000)
            else:
                continue
