
@dataclass
class PolygonPath:
    timestamps: List[int]
    values: List[List[float]]  # x_0, y_0, x_1, y_1, ..., x_n, y_n


@dataclass
class PolygonAnnotation:
    id: AnnotationID
    sensor_id: SensorID
    path: PolygonPath
    type: Literal["polygon"] = "polygon"
    parent_id: Optional[AnnotationID] = None
    stationary: Optional[bool] = False
    label: Optional[str] = None
    attributes: Optional[List[AttributePath]] = None
