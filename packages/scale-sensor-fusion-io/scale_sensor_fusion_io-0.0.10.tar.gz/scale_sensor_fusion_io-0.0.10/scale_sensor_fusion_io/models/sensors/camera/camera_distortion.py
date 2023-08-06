from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Any, ClassVar, Dict, Literal, Mapping, Protocol, Type, Union

from typing_extensions import TypeAlias


class DistortionModel(str, Enum):
    FISHEYE = "fisheye"
    MOD_KANNALA = "mod_kannala"
    CYLINDRICAL = "cylindrical"
    OMNIDIRECTIONAL = "omnidirectional"
    BROWN_CONRADY = "brown_conrady"
    MOD_EQUI_FISH = "mod_equi_fish"
    FISHEYE_RAD_TAN_THIN_PRISM = "fisheye_rad_tan_prism"


@dataclass
class DistortionParamsBase:
    model: DistortionModel


@dataclass
class BrownConradyParams(DistortionParamsBase):
    model: Literal[DistortionModel.BROWN_CONRADY] = DistortionModel.BROWN_CONRADY
    k1: float = 0
    k2: float = 0
    k3: float = 0
    k4: float = 0
    k5: float = 0
    k6: float = 0
    p1: float = 0
    p2: float = 0
    lx: float = 0
    ly: float = 0


@dataclass
class FisheyeParams(DistortionParamsBase):
    model: Literal[DistortionModel.FISHEYE] = DistortionModel.FISHEYE
    k1: float = 0
    k2: float = 0
    k3: float = 0
    k4: float = 0


@dataclass
class AppleFisheyeParams(DistortionParamsBase):
    model: Literal[DistortionModel.MOD_EQUI_FISH] = DistortionModel.MOD_EQUI_FISH
    k2: float = 0
    k3: float = 0
    k4: float = 0


@dataclass
class AppleKannalaParams(DistortionParamsBase):
    model: Literal[DistortionModel.MOD_KANNALA] = DistortionModel.MOD_KANNALA
    k1: float = 0
    k2: float = 0
    k3: float = 0
    k4: float = 0


@dataclass
class CylindricalParams(DistortionParamsBase):
    model: Literal[DistortionModel.CYLINDRICAL] = DistortionModel.CYLINDRICAL


@dataclass
class OmnidirectionalParams(DistortionParamsBase):
    model: Literal[DistortionModel.OMNIDIRECTIONAL] = DistortionModel.OMNIDIRECTIONAL
    k1: float = 0
    k2: float = 0
    k3: float = 0
    p1: float = 0
    p2: float = 0
    lx: float = 0
    ly: float = 0
    xi: float = 0


@dataclass
class FisheyeRadTanThinPrismParams(DistortionParamsBase):
    model: Literal[
        DistortionModel.FISHEYE_RAD_TAN_THIN_PRISM
    ] = DistortionModel.FISHEYE_RAD_TAN_THIN_PRISM
    k1: float = 0
    k2: float = 0
    k3: float = 0
    k4: float = 0
    k5: float = 0
    k6: float = 0
    p1: float = 0
    p2: float = 0
    s1: float = 0
    s2: float = 0
    s3: float = 0
    s4: float = 0


DistortionParams: TypeAlias = Union[
    BrownConradyParams,
    FisheyeParams,
    AppleFisheyeParams,
    AppleKannalaParams,
    CylindricalParams,
    OmnidirectionalParams,
    FisheyeRadTanThinPrismParams,
]

DISTORTION_PARAMETERS = {
    params
    for dist_models in DistortionParams.__args__  # type: ignore
    for params in dist_models.__dataclass_fields__.keys()
}


class DataClassProtocol(Protocol):
    __dataclass_fields__: ClassVar[dict]


def extract_distortion_params(
    distortion: Union[DataClassProtocol, Mapping, dict]
) -> DistortionParams:
    """
    Generic helper to extract distortion params from untyped input
    """
    distortion_fields: Dict[str, Any] = {}
    if isinstance(distortion, dict):
        distortion_fields = distortion
    elif isinstance(distortion, Mapping):
        distortion_fields = {k: v for k, v in distortion.items()}
    elif is_dataclass(distortion):
        distortion_fields = asdict(distortion)
    else:
        distortion_fields = distortion.__dict__

    model: DistortionModel = distortion_fields.get("model", distortion_fields.get("camera_model", DistortionModel.BROWN_CONRADY))

    dataclass: Type[DistortionParams] = next(
        i
        for i in [
            FisheyeParams,
            AppleFisheyeParams,
            AppleKannalaParams,
            CylindricalParams,
            OmnidirectionalParams,
            BrownConradyParams,
            FisheyeRadTanThinPrismParams,
        ]
        if i.model == model  # type: ignore
    )
    # construct param dict for dataclass
    d = {}
    for key in dataclass.__dataclass_fields__:
        if (
            key in distortion_fields
            and key != "model"
            and distortion_fields[key] is not None
        ):
            d[key] = distortion_fields[key]
    return dataclass(**d)
