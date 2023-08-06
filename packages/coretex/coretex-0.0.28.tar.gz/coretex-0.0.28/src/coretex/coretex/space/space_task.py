from enum import IntEnum


class SpaceTask(IntEnum):

    objectDetection       = 1
    imageSegmentation     = 2
    tabularDataProcessing = 3
    superResolution       = 4
    videoAnalytics        = 5
    audioAnalytics        = 6
    bodyTracking          = 7
    other                 = 8
    imuEventDetection     = 9
    nlp                   = 10  # Natural Language Processing
    bioInformatics        = 11
