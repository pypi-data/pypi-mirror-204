from ..common import SensorID
from ...pose_path import PosePath
from dataclasses import dataclass
from typing import List, Union, Optional, Literal, Any

import numpy.typing as npt
import numpy as np


# Define LidarSensorPoints dataclass
@dataclass
class LidarSensorPoints:
    positions: npt.NDArray[np.float32]
    colors: Optional[npt.NDArray[np.uint8]] = None
    intensities: Optional[npt.NDArray[np.uint8]] = None
    timestamps: Optional[Union[npt.NDArray[np.int32], npt.NDArray[np.int64]]] = None


# Define LidarSensorFrame dataclass
@dataclass
class LidarSensorFrame:
    timestamp: int
    points: LidarSensorPoints


# Define LidarSensor dataclass
@dataclass
class LidarSensor:
    id: SensorID
    poses: PosePath
    frames: List[LidarSensorFrame]
    parent_id: Optional[SensorID] = None
    coordinates: Literal["ego", "world"] = "world"
    type: Literal["lidar"] = "lidar"
