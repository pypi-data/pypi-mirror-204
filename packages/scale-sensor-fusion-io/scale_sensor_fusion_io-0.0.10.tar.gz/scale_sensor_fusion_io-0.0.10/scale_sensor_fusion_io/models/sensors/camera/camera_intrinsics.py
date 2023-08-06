from dataclasses import dataclass
from .camera_distortion import DistortionParams

@dataclass
class CameraIntrinsics:
    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int

    distortion: DistortionParams
    skew: float = 0
    scale_factor: float = 0
