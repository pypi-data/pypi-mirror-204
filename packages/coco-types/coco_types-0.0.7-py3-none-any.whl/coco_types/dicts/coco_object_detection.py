from typing import Literal, TypeAlias, TypedDict


class Info(TypedDict):
    year: int
    version: str
    description: str
    contributor: str
    url: str
    date_created: str


class Licence(TypedDict):
    id: int
    name: str
    url: str


class Image(TypedDict):
    id: int
    width: int
    height: int
    file_name: str


TPolygonSegmentation: TypeAlias = list[list[float]]


class RLE(TypedDict):
    size: list[int]
    counts: list[int]


class COCO_RLE(TypedDict):
    size: list[int]
    counts: str | bytes


class Annotation(TypedDict):
    id: int
    image_id: int
    category_id: int
    # Segmentation can be a polygon, RLE or COCO RLE.
    # Exemple of polygon: "segmentation": [[510.66,423.01,511.72,420.03,...,510.45,423.01]]
    # Exemple of RLE: "segmentation": {"size": [40, 40], "counts": [245, 5, 35, 5, 35, 5, 35, 5, 35, 5, 1190]}
    # Exemple of COCO RLE: "segmentation": {"size": [480, 640], "counts": "aUh2b0X...BgRU4"}
    segmentation: TPolygonSegmentation | RLE | COCO_RLE
    # The COCO bounding box format is [top left x position, top left y position, width, height].
    # bbox exemple:  "bbox": [473.07,395.93,38.65,28.67]
    bbox: list[float]
    iscrowd: Literal[0] | Literal[1]


class Category(TypedDict):
    id: int
    name: str
    supercategory: str


class Dataset(TypedDict):
    info: Info
    licences: list[Licence]
    images: list[Image]
    annotations: list[Annotation]
    categories: list[Category]
