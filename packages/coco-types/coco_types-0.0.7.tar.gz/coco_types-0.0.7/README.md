# COCO Types

Note: This package loads the data as is and does not create dictionaries mapping ids to lists of images/annotations/categories.

## Installation

The package is available on pypi [here](https://pypi.org/project/coco-types/), you can install it with:
```
pip install coco-types
```

## Loading COCO data

You can load COCO dataset labels into Pydantic objects by using the `Dataset` and `DatasetKP` classes.

For an object detection dataset:
```python
import coco_types

with open("path/to/json", encoding="utf-8") as data_file:
    dataset = coco_types.Dataset.parse_raw(data_file.read())
```

For a keypoint detection dataset:
```python
import coco_types

with open("path/to/json", encoding="utf-8") as data_file:
    dataset = coco_types.DatasetKP.parse_raw(data_file.read())
```


## Usage example:
```python
import coco_types

with open("path/to/json", encoding="utf-8") as data_file:
    dataset = coco_types.Dataset.parse_raw(data_file.read())

img = dataset.images[0]
print(f"Image's filename {img.file_name}")
print(f"Image's id {img.id}")
print(f"Image's height {img.height}")
print(f"Image's width {img.width}")

img_annotations = [annotation for annotation in dataset.annotations
                   if annotation.image_id == img.id]
ann = img_annotations[0]
print(f"Annotation's id: {ann.id}")
print(f"Annotation's image id: {ann.image_id}")
print(f"Annotation's category id: {ann.category_id}")
print(f"Annotation's iscrowd: {ann.iscrowd}")
print(f"Annotation's bbox: {ann.bbox}")
print(f"Annotation's area {ann.area}")

for cat in dataset.categories:
    if cat.id == ann.category_id:
        break

print(f"Category's name {cat.name}")
print(f"Category's supercategory {cat.supercategory}")
```

### Keypoints
If using a dataset with keypoints (`coco_types.DatasetKP`), then annotations will have two additional attributes: `keypoints` and `num_keypoints`.\
In the same way, categories will have  two additional attributes: `keypoints` and `skeleton`.


## TypedDict versions
A `TypedDict` version of the pydantic models can be accessed using `coco_types.dicts.*` (for example `coco_types.dicts.Dataset`). This can be useful if you have data that is slightly malformed / follows a slightly different format but is still usable.
