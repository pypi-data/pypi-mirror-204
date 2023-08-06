from typing import Union
from .common import *

from .attributes import *
# from .box_2d import *
from .cuboid import *
# from .event import *
# from .labeled_points import *
# from .localization_adjustment import *
# from .object import *
# from .polygon import *

Annotation = Union[
    AttributesAnnotation,
    # Box2DAnnotation,
    CuboidAnnotation,
    # LabeledPointsAnnotation,
    # LocalizationAdjustmentAnnotation,
    # ObjectAnnotation,
]