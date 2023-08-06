
@dataclass
class ObjectAnnotation:
    id: AnnotationID
    type: Literal["object"] = "object"
    parent_id: Optional[AnnotationID] = None
    label: Optional[str] = None
    attributes: Optional[List[AttributePath]] = None

