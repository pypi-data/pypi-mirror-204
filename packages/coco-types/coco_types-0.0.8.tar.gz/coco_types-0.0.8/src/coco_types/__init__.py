__version__ = "0.0.8"

from . import dicts  # pyright: ignore[reportUnusedImport]
from .coco_keypoints import AnnotationKP, AnnotationKPAny, CategoryKP, DatasetKP
from .coco_object_detection import (
    Annotation,
    AnnotationAny,
    Category,
    COCO_RLE,
    Dataset,
    Image,
    Info,
    Licence,
    RLE,
    TPolygonSegmentation,
)

__all__ = [
    "Annotation", "AnnotationAny", "Category", "COCO_RLE", "Dataset", "Image", "Info", "RLE", "Licence",
    "TPolygonSegmentation",
    "AnnotationKPAny", "AnnotationKP", "CategoryKP", "DatasetKP",
]
