from typing import Tuple, Dict

import time

from ..networking import NetworkManager
from ..coretex.experiment.experiment import Experiment


METRICS = [
    ("cpu_usage", "time (s)", "usage (%)"),
    ("ram_usage", "time (s)", "usage (%)"),
    ("download_speed", "time (s)", "bytes"),
    ("upload_speed", "time (s)", "bytes"),
    ("disk_read", "time (s)", "bytes"), 
    ("disk_write", "time (s)", "bytes")
]


def setupGPUMetrics() -> None:
    # Making sure that if GPU exists, GPU related metrics are added to METRICS list
    # py3nvml.nvmlShutdown() is never called because process for uploading metrics
    # will kill itself after experiment and in that moment py3nvml cleanup will
    # automatically be performed

    try:
        from py3nvml import py3nvml
        py3nvml.nvmlInit()

        METRICS.extend([
            ("gpu_usage", "time (s)", "usage (%)"),
            ("gpu_temperature", "time (s)", "usage (%)")
        ])
    except:
        pass


def uploadMetricsWorker(refreshToken: str, experimentId: int) -> None:
    setupGPUMetrics()
    NetworkManager.instance().authenticateWithRefreshToken(refreshToken)

    experiment = Experiment.fetchById(experimentId)
    if experiment is None:
        raise ValueError

    createdMetrics = experiment.createMetrics(METRICS)

    if len(createdMetrics) == 0:
        raise RuntimeError(">> [Coretex] Failed to create Metrics list!")

    while True:
        startTime = time.time()
        metricValues: Dict[str, Tuple[float, float]] = {}

        for metric in experiment.metrics:
            metricValue = metric.extract()

            if metricValue is not None:
                metricValues[metric.name] = startTime, metricValue

        experiment.submitMetrics(metricValues)
        time.sleep(5)  # delay between sending generic metrics
