# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import EmptyDatasetException
from os.path import join, exists, basename, splitext
from deepview.validator.datasets.core import Dataset
from deepview.validator.writers import Writer
from glob import glob
from PIL import Image
import numpy as np
import warnings


class DarkNetDataset(Dataset):
    """
    This class reads Darknet format datasets.
    Dataset format should be the same as coco128 at:
    https://www.kaggle.com/datasets/ultralytics/coco128

    Optionally, the images and the text annotations can be in the
    same directory.
    Unit-test for this class is defined under:
        file: test/deepview/validator/datasets/test_darknet.py

    Parameters
    ----------

        source: str
            The path to the source dataset.

        info_dataset: dict
            Contains information such as :

            .. code-block:: python

                {
                    "classes": [list of unique labels],
                    "validation":
                    {
                        "images: 'path to the images',
                        "annotations": 'path to the annotations'
                    }
                }

            *Note: the classes are optional and the path to the images
            and annotations can be the same.*

        gformat: str
            The annotation format that can be either 'yolo', 'pascalvoc',
            or 'coco'. By default darknet datasets have annotations in
            'yolo' format.

        absolute: bool
            Specify as True if the annotations are not normalized to the
            image dimensions. By default they are normalized.

        validate_type: str
            The type of validation to perform that can be 'detection' or
            'segmentation'.

        show_missing_annotations: bool
            If this is True, then print on the terminal all
            missing annotations. Else, it will only
            print the number of missing annotations.

    Raises
    ------
        InvalidDatasetSourceException
            This exception will be raised if the path
            to the images or annotations is None.

        DatasetNotFoundException
            This exception will be raised if the provided path
            to the images or annotations does not exist.

        ValueError
            This exception will be raised if the provided
            path to the images or annotations is not a string.

        EmptyDatasetException
            This exception will be raised if the provided
            path to the images or text files does not contain
            any image files or text files respectively.
    """

    def __init__(
        self,
        source,
        info_dataset=None,
        gformat='yolo',
        absolute=False,
        validate_type="detection",
        show_missing_annotations=False
    ):
        super(DarkNetDataset, self).__init__(
            source=source,
            gformat=gformat,
            absolute=absolute,
            validate_type=validate_type,
            show_missing_annotations=show_missing_annotations
        )

        if info_dataset is None:
            info_dataset = self.get_detection_dataset(source)

        self.validate_type = validate_type.lower()
        self.image_source = self.validate_input_source(
            info_dataset.get('validation').get('images'))
        self.annotation_source = self.validate_input_source(
            info_dataset.get('validation').get('annotations'))
        self.labels = info_dataset.get('classes', None)

        self.images = list()
        for extension in ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']:
            if len(self.images) == 0:
                self.images = glob(join(self.image_source, f'*.{extension}'))
            else:
                break

        if len(self.images) == 0:
            raise EmptyDatasetException(
                "images",
                self.image_source
            )

        for ext in ['*.txt', '*.json']:
            self.annotations = glob(join(self.annotation_source, ext))
            if len(self.annotations) == 0 or (
                len(self.annotations) == 1 and basename(
                    self.annotations[0]) == "labels.txt"):
                continue
            else:
                break
        
        if len(self.annotations) == 0:
            raise EmptyDatasetException(
                "annotations",
                self.annotation_source
            )

        self.annotation_extension = splitext(
            self.annotations[0]
        )[1]

    def build_dataset(self):
        """
        This method builds the instances to allow iteration
        in the dataset.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_darknet.py
            function: test_build_dataset

        Parameters
        ----------
            None

        Returns
        -------
            instances: list of tuple
                One instance contains the
                (path to the image, path to the annotation)

        Raises
        ------
            None
        """

        missing_annotations = 0
        instances = list()
        for image_path in self.images:
            annotation_path = join(
                self.annotation_source,
                splitext(
                    basename(image_path))[0] +
                self.annotation_extension)

            if exists(annotation_path):
                instances.append((image_path, annotation_path))
            else:
                instances.append((image_path, None))
                if self.show_missing_annotations:
                    Writer.logger(
                        "Could not find the annotation " +
                        "for this image: {}. ".format(
                            basename(image_path)) +
                        "Looking for {}".format(
                            splitext(
                                basename(image_path))[0] +
                            self.annotation_extension),
                        code="WARNING")
                    missing_annotations += 1
                else:
                    missing_annotations += 1

        if not self.show_missing_annotations and missing_annotations > 0:
            Writer.logger(
                "There were {} images without annotations. ".format(
                    missing_annotations) + "To see the names of the images, " +
                "enable --show_missing_annotations in the command line.",
                code="WARNING")

        return instances

    def read_sample(self, instance):
        """
        This method reads one sample from the dataset.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_darknet.py
            function: test_read_sample

        Parameters
        ----------

            instance: tuple
                This contains (image path, annotation path).

        Returns
        -------
            ground truth instance: dict
                This contains information such as:

                .. code-block:: python

                    {
                        'image': image numpy array,
                        'height': height,
                        'width': width,
                        'boxes': list bounding boxes,
                        'labels': list of labels,
                        'image_path': image_path
                    }

        Raises
        ------
            None
        """

        image_path, annotation_path = instance
        image = np.asarray(Image.open(image_path))

        try:
            height, width, _ = image.shape
        except ValueError:
            Writer.logger(
                "Encountered a Gray image, skipping..{}".format(
                    basename(image_path)), code="WARNING")
            return None

        if self.validate_type == 'detection':
            load = self.txt_load_boxes(annotation_path)
        else:
            load = self.json_load_polygon_instance(annotation_path)

        if load is not None:
            boxes = load.get('boxes')
            labels = load.get('labels')
        else:
            return {
                'image': image,
                'height': height,
                'width': width,
                'boxes': [],
                'labels': [],
                'image_path': image_path
            }

        return {
            'image': image,
            'height': height,
            'width': width,
            'boxes': boxes,
            'labels': labels,
            'image_path': image_path
        }

    def txt_load_boxes(self, annotation_path):
        """
        This method reads from the text file annotation.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_darknet.py
            function: test_txt_load_boxes

        Parameters
        ----------

            annotation_path: str
                This is the path to the text file annotation.

        Returns
        -------
            annotation info: dict
                This contains information such as:

                .. code-block:: python

                    {
                        'boxes': list of bounding boxes,
                        'labels': list of labels
                    }

                None if the file is empty.

        Raises
        ------
            None
        """

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                annotation = np.genfromtxt(annotation_path)
        except TypeError:
            return None

        if len(annotation):
            annotation = annotation.reshape(-1, 5)
            boxes = annotation[:, 1:5]
            boxes = self.normalizer(boxes) if self.normalizer else boxes
            boxes = self.transformer(boxes) if self.transformer else boxes
        else:
            return None

        labels = annotation[:, 0:1].flatten().astype(np.int32)
        if len(self.labels):
            labels = [self.labels[int(label)].lower() for label in labels]

        return {
            'boxes': boxes,
            'labels': labels
        }

    def json_load_boxes(self, annotation_path):
        """
        This method reads from the JSON annotation.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_darknet.py
            function: test_json_load_boxes

        Parameters
        ----------

            annotation_path: str
                This is the path to the JSON annotation

        Returns
        -------
            annotation info: dict
                This contains information such as:

                .. code-block:: python

                    {
                        'boxes': list of bounding boxes,
                        'labels': list of labels
                    }

                None if the file is empty.

        Raises
        ------
            None
        """

        import json

        try:
            with open(annotation_path) as file:
                data = json.load(file)
                try:
                    annotation = np.array(data["boxes"])
                    annotation = self.normalizer(
                        annotation) if self.normalizer else annotation
                    boxes = self.transformer(
                        annotation[:, 0:5]
                    ) if self.transformer else annotation[:, 0:5]
                except KeyError:
                    return None
                try:
                    if len(self.labels):
                        labels = [self.labels[int(label)].lower()
                                  for label in data["labels"]]
                    else:
                        labels = data["labels"]
                except KeyError:
                    return None
        except FileNotFoundError:
            return None

        return {
            'boxes': boxes,
            'labels': labels
        }
    # TODO: Make this method single with the method above.

    def json_load_polygon_instance(self, annotation_path):
        """
        This method loads a single instance from
        a JSON file in the image dataset to grab the segments.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_darknet.py
            function: test_json_load_boxes

        Parameters
        ----------

            annotation_path: str
                This is the path to the JSON annotation

        Returns
        -------
            annotation info: dict
                This contains information such as:

                .. code-block:: python

                    {
                        'boxes': list of polygon segments,
                        'labels': list of labels
                    }

                None if the file is empty.

        Raises
        ------
            None

        """

        import json

        try:
            with open(annotation_path) as file:
                data = json.load(file)
                height, width = self.shape
                try:
                    boxes = []
                    for polygon in data["segment"]:
                        # a list of vertices
                        x_y = []
                        for vertex in polygon:
                            vertex = self.denormalizer(
                                vertex, height, width) if \
                                self.denormalizer else vertex
                            x_y.append(float(vertex[0]))
                            x_y.append(float(vertex[1]))
                        boxes.append(x_y)
                except KeyError:
                    return None
                try:
                    labels = []
                    for label in data["labels"]:
                        labels.append(int(label) + 1)
                except KeyError:
                    return None
        except FileNotFoundError:
            return None

        return {
            'boxes': boxes,
            'labels': labels
        }
