from typing import Optional

import psutil

from ..metric import Metric


class MetricDiskRead(Metric):

    def extract(self) -> Optional[float]:
        diskIoCounters = psutil.disk_io_counters()
        if diskIoCounters is None:
            return None
        return float(diskIoCounters.read_bytes)
