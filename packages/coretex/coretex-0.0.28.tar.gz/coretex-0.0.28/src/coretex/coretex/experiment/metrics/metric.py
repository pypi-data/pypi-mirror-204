from abc import abstractmethod
from typing import Dict, Any, List, Tuple, Optional
from typing_extensions import Self

from ....codable import Codable, KeyDescriptor
from ....networking import NetworkManager, RequestType


class Metric(Codable):

    name: str
    xLabel: str
    yLabel: str

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()
        descriptors["name"] = KeyDescriptor("metric")

        return descriptors 

    @classmethod
    def create(cls, name: str, xLabel: str, yLabel: str) -> Self:
        obj = cls()

        obj.name = name
        obj.xLabel = xLabel
        obj.yLabel = yLabel

        return obj

    @classmethod
    def createMetrics(cls, experimentId: int, values: List[Tuple[str, str, str]]) -> bool:
        metrics: List[Metric] = []

        for value in values:
            metrics.append(cls.create(*value))

        parameters: Dict[str, Any] = {
            "experiment_id": experimentId,
            "metrics": [metric.encode() for metric in metrics]
        }

        endpoint = "model-queue/metrics-meta"
        response = NetworkManager.instance().genericJSONRequest(
            endpoint = endpoint,
            requestType = RequestType.post,
            parameters = parameters
        )

        return not response.hasFailed()

    def extract(self) -> Optional[float]:
        return None
