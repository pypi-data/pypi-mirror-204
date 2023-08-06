from typing import Generic, Literal, TypeAlias, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class Info(BaseModel):
    year: int
    version: str
    description: str
    contributor: str
    url: str
    date_created: str


class Licence(BaseModel):
    id: int
    name: str
    url: str


class Image(BaseModel):
    id: int
    width: int
    height: int
    file_name: str


TPolygonSegmentation = list[list[float]]


class RLE(BaseModel):
    size: list[int]
    counts: list[int]


class COCO_RLE(BaseModel):
    size: list[int]
    counts: str | bytes


_TSegmentation = TypeVar("_TSegmentation", TPolygonSegmentation, RLE, COCO_RLE)


class Annotation(GenericModel, Generic[_TSegmentation]):
    id: int
    image_id: int
    category_id: int
    # Segmentation can be a polygon, RLE or COCO RLE.
    # Exemple of polygon: "segmentation": [[510.66,423.01,511.72,420.03,...,510.45,423.01]]
    # Exemple of RLE: "segmentation": {"size": [40, 40], "counts": [245, 5, 35, 5, 35, 5, 35, 5, 35, 5, 1190]}
    # Exemple of COCO RLE: "segmentation": {"size": [480, 640], "counts": "aUh2b0X...BgRU4"}
    segmentation: _TSegmentation
    area: float
    # The COCO bounding box format is [top left x position, top left y position, width, height].
    # bbox exemple:  "bbox": [473.07,395.93,38.65,28.67]
    bbox: list[float]
    iscrowd: Literal[0] | Literal[1]

AnnotationAny: TypeAlias = Annotation[TPolygonSegmentation] | Annotation[RLE] | Annotation[COCO_RLE]

class Category(BaseModel):
    id: int
    name: str
    supercategory: str


class Dataset(BaseModel):
    info: Info | None = None
    licences: list[Licence] | None = None
    images: list[Image]
    annotations: list[AnnotationAny]
    categories: list[Category]
