# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import UnsupportedAnnotationFormatException
from deepview.validator.exceptions import NonMatchingIndexException
from os.path import basename, splitext, join, exists
from deepview.validator.datasets.core import Dataset
from deepview.validator.runners.core import Runner
import numpy as np
import warnings


class OfflineRunner(Runner):
    """
    This class reads model prediction annotations stored in text files
    that are in YOLO format. For more information on the Yolo format visit:
    https://support.deepviewml.com/hc/en-us/articles/10869801702029

    *Note: These text files should also include the model prediction scores
    which adds to the Yolo format: [cls score xc yc width height]*

    Use Case: PT models are ran using https://github.com/ultralytics/yolov5
    repository. These model predictions will be stored in TXT files that
    are in Yolo format. This class will read the text files to be validated.

    Unit-test for this class is defined under:
        file: test/deepview/validator/runners/test_offline.py

    Parameters
    ----------

        annotation_source: str
            This is the path to the model prediction annotations
            stored in text files with yolo format annotations.
            [cls score xc yc width height].

        labels: list
            This contains the unique string labels in the dataset.

        annotation_extension: str
            This represents the extension of the files that store
            the prediction annotations. Only text files is supported
            at the moment.

        format: str
            Specify the format of the annotations (yolo, coco, pascalvoc).

        label_offset: int
            The index offset to match label index to the ground truth index.

    Raises
    ------
        UnsupportedAnnotationFormatException
            This exception will be raised if the annotation format passed
            is not recognized.

        NonMatchingIndexException
                This exception will be raised if the model outputs an index
                that is out of bounds to the labels list passed.
    """

    def __init__(
        self,
        annotation_source,
        labels,
        annotation_extension='txt',
        format='yolo',
        label_offset=0
    ):

        super(OfflineRunner, self).__init__(annotation_source)

        self.labels = labels
        self.annotation_extension = annotation_extension
        self.format = format
        self.label_offset = label_offset
        self.device = "cpu"

        if self.format not in ['yolo', 'pascalvoc', 'coco']:
            raise UnsupportedAnnotationFormatException(self.format)

        self.transformer = None
        if self.format == 'yolo':
            self.transformer = Dataset.yolo2xyxy
        elif self.format == 'coco':
            self.transformer = Dataset.xywh2xyxy
        else:
            self.transformer = None

    def run_single_instance(self, image):
        """
        This method reads one prediction annotation file based on the
        image name and returns the bounding boxes and labels.
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_offline.py
            function: test_run_single_instance

        Parameters
        ----------

            image: str
                The path to the image. This is used to match the
                annotation to be read.

        Returns
        -------

            boxes: np.ndarray
                The prediction bounding boxes.. [[box1], [box2], ...]

            classes: np.ndarray
                The prediction labels.. [cl1, cl2, ...]

            scores: np.ndarray
                The prediction confidence scores.. [score, score, ...]
                normalized between 0 and 1.

        Raises
        ------
            NonMatchingIndexException
                This exception will be raised if the model outputs an index
                that is out of bounds to the labels list passed.

            ValueError
                This exception will be raised if the provided image is not a
                string path pointing to the image or if the provided path does
                not exist.
        """

        if isinstance(image, str):
            if exists(image):
                annotation_path = join(self.source, "{}.{}".format(
                    splitext(basename(image))[0], self.annotation_extension
                ))
            else:
                raise ValueError(
                    "The provided image path does not exist at: {}".format(
                        image))
        else:
            raise ValueError(
                "The provided image needs to be a string path pointing " +
                "to the image. Provided with type: {}".format(type(image)))

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                annotation = np.genfromtxt(annotation_path)
        except FileNotFoundError:
            return [], [], []

        if len(annotation):
            annotation = annotation.reshape(-1, 6)
            boxes = annotation[:, 2:6]
            boxes = self.transformer(boxes) if self.transformer else boxes
        else:
            return [], [], []

        scores = annotation[:, 1:2].flatten().astype(np.float32)
        labels = annotation[:, 0:1].flatten().astype(
            np.int32) + self.label_offset

        if len(self.labels):
            string_labels = list()
            for label in labels:
                try:
                    string_labels.append(self.labels[int(label)])
                except IndexError:
                    raise NonMatchingIndexException(label)
            labels = string_labels

        return boxes, labels, scores
