from typing import TypedDict

from .coco_object_detection import Annotation, Category, Image, Info, Licence


class AnnotationKP(Annotation):
    keypoints: list[int]
    num_keypoints: int


class CategoryKP(Category):
    keypoints: list[str]
    skeleton: list[tuple[int, int]]


class DatasetKP(TypedDict):
    info: Info
    licences: list[Licence]
    images: list[Image]
    annotations: list[AnnotationKP]
    categories: list[CategoryKP]
