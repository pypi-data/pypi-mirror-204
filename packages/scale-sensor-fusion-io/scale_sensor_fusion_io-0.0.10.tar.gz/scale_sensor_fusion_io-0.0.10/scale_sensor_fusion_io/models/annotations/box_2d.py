

@dataclass
class Box2DPath:
    timestamps: List[int]
    values: List[List[float]]  # left, top, width, height


@dataclass
class Box2DAnnotation:
    id: AnnotationID
    sensor_id: SensorID
    path: Box2DPath
    type: Literal["box"] = "box"
    parent_id: Optional[AnnotationID] = None
    stationary: Optional[bool] = False
    label: Optional[str] = None
    attributes: Optional[List[AttributePath]] = None

