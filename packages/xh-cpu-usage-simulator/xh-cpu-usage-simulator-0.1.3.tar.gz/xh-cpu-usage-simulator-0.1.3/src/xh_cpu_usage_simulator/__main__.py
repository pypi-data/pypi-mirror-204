# This is a sample Python script.
import argparse
import sys
from multiprocessing import Process, Manager, Array

import psutil

from xh_cpu_usage_simulator import TaskWorker
from xh_cpu_usage_simulator.MovingAvg import MovingAvg
from xh_cpu_usage_simulator.PsMonitor import PsMonitor
from xh_cpu_usage_simulator.LinearRegressionPrediction import LinearRegressionPredication


def validation(min_usage: float, max_usage: float):
    if not 0 < min_usage < 100:
        raise Exception(f"minimum usage[{min_usage}] is out of range")
    if not 0 < max_usage < 100:
        raise Exception(f"maximum usage[{max_usage}] is out of range")

    if max_usage < min_usage:
        raise Exception(f"Usage bound [{min_usage} - {max_usage}] is not valid")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="xh-cpu-usage-simulator",
        usage="A simple tool to simulate system loading of cpu"
    )

    parser.add_argument("--min", help="minimum percentage cpu usage", type=float)
    parser.add_argument("--max", help="maximum percentage cpu usage", type=float)
    parser.add_argument("--iv", help="initial value", type=float, default=1000)

    parsed_args = parser.parse_args(sys.argv[1:])

    lower_bound = parsed_args.min
    upper_bound = parsed_args.max
    iv = parsed_args.iv

    validation(lower_bound, upper_bound)

    d = Manager().dict()
    r = Manager().dict()
    cpu_count = psutil.cpu_count(logical=False)

    ps = []
    for i in range(cpu_count):
        d.update({f"{i}": iv / cpu_count})
        r.update({f"{i}-complete": 0})
        # bucket = MovingAvg(10)
        p = Process(target=TaskWorker.worker, args=(i, d, r))
        p.start()
        ps.append(p)

    total_operation = sum([d[i] for i in d])

    m_avg = MovingAvg(10)

    # target = 70
    rounds = 0
    prediction = LinearRegressionPredication(10)
    for m in PsMonitor().monitor():
        if m_avg.cur_index == 0:
            if rounds == 0:
                rounds += 1
            else:
                rounds += 1
                cur_total_operation = round(sum([d[i] for i in d]), 2)
                cur_total_mv = round(sum([r[i] for i in r], 2))
                prediction.insert(m_avg.avg, cur_total_mv)

                target = round(lower_bound + abs(lower_bound - upper_bound) / 2, 2)


                def next_operation():
                    if prediction.is_ready():
                        return prediction.predict(target)
                    else:
                        return None


                if lower_bound > m_avg.avg:
                    for i in d:
                        n_op = next_operation()
                        d[i] = n_op / len(d) if n_op is not None and n_op > 0 else d[i] * 2
                    new_total_operation = round(sum([d[i] for i in d]), 2)
                    print(
                        f"{rounds:05d}::Targeting[{lower_bound} < {target} < {upper_bound}], now[{m_avg.avg}], increase operation with loading[{cur_total_mv}] from {cur_total_operation} to {new_total_operation}")
                elif upper_bound < m_avg.avg:
                    for i in d:
                        n_op = next_operation()
                        d[i] = n_op / len(d) if n_op is not None else d[i] * 0.85
                    new_total_operation = round(sum([d[i] for i in d]), 2)
                    print(
                        f"{rounds:05d}::Targeting[{lower_bound} < {target} < {upper_bound}], now[{m_avg.avg}], decrease operation with loading[{cur_total_mv}] from {cur_total_operation} to {new_total_operation}")
                else:
                    for i in d:
                        n_op = next_operation()
                        d[i] = n_op / len(d) if n_op is not None else d[i] * 0.85
                    new_total_operation = round(sum([d[i] for i in d]), 2)
                    print(
                        f"{rounds:05d}::Targeting[{lower_bound} < {target} < {upper_bound}], now[{m_avg.avg}], adjustment with loading[{cur_total_mv}] from {cur_total_operation} to {new_total_operation}")
        m_avg.insert(m.avg)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
