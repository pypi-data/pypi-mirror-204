import numpy.typing as npt
import numpy as np

from scale_sensor_fusion_io.models.sensors.camera.camera_intrinsics import (
    CameraIntrinsics,
)

from ..common import SensorID
from ...pose_path import PosePath
from .camera_distortion import DistortionModel, DistortionParams, BrownConradyParams
from dataclasses import dataclass
from typing import List, Union, Optional, Literal, Any


# Define CameraDistortion dataclass
@dataclass
class CameraDistortion:
    model: DistortionModel
    params: DistortionParams

    @staticmethod
    def from_values(model: str, values: List[float]) -> "CameraDistortion":
        if model == DistortionModel.BROWN_CONRADY:
            k1, k2, p1, p2, k3, k4, k5, k6 = values
            return CameraDistortion(
                model=DistortionModel.BROWN_CONRADY,
                params=BrownConradyParams(
                    k1=k1, k2=k2, p1=p1, p2=p2, k3=k3, k4=k4, k5=k5, k6=k6
                ),
            )


# Define CameraSensorContent dataclass
@dataclass
class CameraSensorVideo:
    timestamps: List[int]
    content: npt.NDArray[np.uint8]
    fps: float


# Define CameraSensorImages dataclass
@dataclass
class CameraSensorImage:
    timestamp: int
    content: npt.NDArray[np.uint8]


# Define CameraSensor dataclass
@dataclass
class CameraSensor:
    id: SensorID
    poses: PosePath
    intrinsics: CameraIntrinsics
    video: Optional[CameraSensorVideo] = None
    images: Optional[List[CameraSensorImage]] = None
    type: Literal["camera"] = "camera"
    parent_id: Optional[SensorID] = None
