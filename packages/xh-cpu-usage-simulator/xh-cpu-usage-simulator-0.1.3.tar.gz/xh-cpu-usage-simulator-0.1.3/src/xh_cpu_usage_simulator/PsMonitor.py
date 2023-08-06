from dataclasses import dataclass
from typing import Generator

import psutil


@dataclass
class Metrics:
    avg: float


class PsMonitor:

    def monitor(self) -> Generator[Metrics, None, None]:
        # cpu_count = psutil.cpu_count()
        while True:
            result = psutil.cpu_percent(interval=1)
            yield Metrics(result)
