from typing import Callable, Optional, Type, TypeVar, Tuple, List
from enum import IntEnum

import logging

from .remote import processRemote
from .local import processLocal
from ..coretex import ExperimentStatus, NetworkDataset, ExecutingExperiment
from ..logging import LogHandler, initializeLogger, LogSeverity
from ..networking import RequestFailedError
from ..folder_management import FolderManager


DatasetType = TypeVar("DatasetType", bound = "NetworkDataset")


class ExecutionType(IntEnum):
     # TODO: NYI on backend

     local = 1
     remote = 2


def _prepareForExecution(
     experimentId: int,
     datasetType: Optional[Type[DatasetType]] = None,
     metrics: Optional[List[Tuple[str, str ,str]]] = None
) -> None:
     experiment = ExecutingExperiment.startExecuting(experimentId, datasetType)

     logPath = FolderManager.instance().logs / f"{experimentId}.log"
     customLogHandler = LogHandler.instance()
     customLogHandler.currentExperimentId = experimentId

     # if logLevel exists apply it, otherwise default to info
     if not "logLevel" in experiment.parameters:
          initializeLogger(LogSeverity.info, logPath)
     else:
          initializeLogger(experiment.parameters["logLevel"], logPath)

     experiment.updateStatus(
          status = ExperimentStatus.inProgress,
          message = "Executing project."
     )

     if metrics is not None:
          experiment.createMetrics(metrics)

          if len(ExecutingExperiment.current().metrics) > 0:
               logging.getLogger("coretexpylib").info(">> [Coretex] Metrics successfully created.")


def initializeProject(
     mainFunction: Callable[[ExecutingExperiment], None],
     datasetType: Optional[Type[DatasetType]] = None,
     metrics: Optional[List[Tuple[str, str ,str]]] = None
) -> None:

     try:
          experimentId, callback = processRemote()
     except:
          experimentId, callback = processLocal()

     try:
          _prepareForExecution(experimentId, datasetType, metrics)

          callback.onStart()

          logging.getLogger("coretexpylib").info("Experiment execution started")
          mainFunction(ExecutingExperiment.current())

          callback.onSuccess()
     except RequestFailedError:
          callback.onNetworkConnectionLost()
     except BaseException as ex:
          callback.onException(ex)

          raise
     finally:
          callback.onCleanUp()
