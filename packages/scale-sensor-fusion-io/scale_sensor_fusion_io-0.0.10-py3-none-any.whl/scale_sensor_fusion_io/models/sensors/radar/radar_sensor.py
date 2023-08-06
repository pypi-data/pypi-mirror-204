from ..common import SensorID
from ...pose_path import PosePath
from dataclasses import dataclass
from typing import List, Union, Optional, Literal, Any

import numpy.typing as npt
import numpy as np


@dataclass
class RadarSensorPoints:
    positions: npt.NDArray[np.float32]
    directions: Optional[npt.NDArray[np.float32]] = None
    lengths: Optional[npt.NDArray[np.float32]] = None
    timestamps: Optional[Union[npt.NDArray[np.int32], npt.NDArray[np.int64]]] = None


@dataclass
class RadarSensorFrame:
    timestamp: int
    points: RadarSensorPoints


@dataclass
class RadarSensor:
    id: SensorID
    poses: PosePath
    frames: List[RadarSensorFrame]
    type: Literal["radar"] = "radar"
    coordinates: Literal["ego", "world"] = "world"
    parent_id: Optional[SensorID] = None
