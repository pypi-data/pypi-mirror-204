from typing import Final, Type
from typing_extensions import Self

import sys
import logging
import multiprocessing

from ..coretex import Experiment
from ..folder_management import FolderManager
from ..logging import LogHandler

from .calculate_metrics import uploadMetricsWorker


class ProjectCallback:

    def __init__(self, experiment: Experiment, refreshToken: str) -> None:
        self._experiment: Final = experiment

        self.process = multiprocessing.Process(
            target = uploadMetricsWorker,
            args = (refreshToken, self._experiment.id)
        )

    @classmethod
    def create(cls, experimentId: int, refreshToken: str) -> Self:
        experiment = Experiment.fetchById(experimentId)
        if experiment is None:
            raise ValueError

        return cls(experiment, refreshToken)

    def onStart(self) -> None:
        self.process.start()

    def onSuccess(self) -> None:
        pass

    def onException(self, exception: BaseException) -> None:
        pass

    def onNetworkConnectionLost(self) -> None:
        FolderManager.instance().clearTempFiles()

        sys.exit()

    def onCleanUp(self) -> None:
        logging.getLogger("coretexpylib").info("Experiment execution finished")
        self.process.kill()

        try:
            from py3nvml import py3nvml
            py3nvml.nvmlShutdown()
        except:
            pass

        LogHandler.instance().flushLogs()
        LogHandler.instance().reset()

        FolderManager.instance().clearTempFiles()
