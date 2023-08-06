
# Define LabeledPointsAnnotationLabeledPoint dataclass
@dataclass
class LabeledPoint:
    sensor_id: SensorID
    point_ids: npt.NDArray[np.uint32]
    sensor_frame: Optional[int] = None


# Define LabeledPointsAnnotation dataclass
@dataclass
class LabeledPointsAnnotation:
    id: AnnotationID
    label: str
    labeled_points: List[LabeledPoint]
    is_instance: bool = False
    type: Literal["labeled_points"] = "labeled_points"
    parent_id: Optional[AnnotationID] = None


