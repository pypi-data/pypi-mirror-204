from dataclasses import dataclass

AnnotationId: TypeAlias = Union[str, int]

"""
The LocalizationAdjustmentAnnotation represents a PosePath applied a scene to fix localization issues or convert from ego to world coordinates.
"""

@dataclass
class LocalizationAdjustmentAnnotation:
   id: AnnotationId
   poses: PosePath
   type: Literal['localization_adjustment'] = 'localization_adjustment'
   parent_id: Optional[AnnotationId] = None
