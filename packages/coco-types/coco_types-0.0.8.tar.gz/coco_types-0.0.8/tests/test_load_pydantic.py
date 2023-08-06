from pathlib import Path

import coco_types


def test_can_parse_sample_file() -> None:
    with Path("data_samples/coco_25k/annotations.json").open(encoding="utf-8") as data_file:
        dataset = coco_types.Dataset.parse_raw(data_file.read())

    assert dataset.images[0].file_name == "000000174482.jpg"
    assert dataset.annotations[0].bbox == [187.74, 5.84, 310.4, 380.49]
    assert dataset.categories[0].name == "person"
