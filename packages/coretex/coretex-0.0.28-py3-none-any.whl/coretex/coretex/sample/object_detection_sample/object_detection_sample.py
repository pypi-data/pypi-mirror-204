from typing import Optional, Union
from typing_extensions import Self
from pathlib import Path

from ..image_sample import ImageSample


class ObjectDetectionSample(ImageSample):
    """
        Represents the Object detection sample object from Coretex.ai
    """

    @classmethod
    def createObjectDetectionSample(cls, datasetId: int, imagePath: Union[Path, str]) -> Optional[Self]:
        """
            Creates a new sample with the provided name and path

            Parameters:
            datasetId: int -> id of dataset to which sample will be added
            imagePath: Union[Path, str] -> path to the image file

            Returns:
            The created sample object or None if creation failed
        """

        return cls.createImageSample(datasetId, imagePath)
