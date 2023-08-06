# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import UnsupportedAnnotationFormatException
from deepview.validator.exceptions import UnsupportedDatasetTypeException
from deepview.validator.exceptions import InvalidDatasetSourceException
from deepview.validator.exceptions import DatasetNotFoundException
from deepview.validator.exceptions import EmptyDatasetException
from glob import glob
from PIL import Image
import numpy as np
import os


class Dataset:
    """
    This class contains transformation methods for both images and annotations.
    Images can be resized and annotations can be normalized, denormalized or
    converted to specific formats (yolo, coco, pascalvoc). Validation will
    process boxes in pascalvoc format, so transformations exists from
    yolo to pascalvoc and coco to pascalvoc. More information can be found
    on the annotation formats by following this link:
    https://support.deepviewml.com/hc/en-us/articles/10869801702029-Darknet-Ground-Truth-Annotations-Schema
    Unit-test for this class is defined under:
        file: test/deepview/validator/datasets/test_core.py

    Parameters
    ----------

        gformat: str
            The annotation format (yolo, pascalvoc, coco).

        absolute: bool
            If true, then the annotations are not normalized.

        validate_type: str
            Can be either 'detection' or 'segmentation'

        show_missing_annotations: bool
            If this is True, then print on the terminal
            all missing annotations. Else, it will only
            print the number of missing annotations.

    Raises
    ------
        UnsupportedAnnotationFormatException
            This exception will be raised if the provided
            annotation format is not identified.

        UnsupportedDatasetTypeException
            This exception will be raised if the provided
            path does not reflect either Darknet or TFRecord
            format.

        InvalidDatasetSourceException
            This exception will be raised if the path
            to the dataset is None.

        DatasetNotFoundException
            This exception will be raised if the provided path
            to the dataset does not exist.

        EmptyDatasetException
            This exception will be raised if the provided path
            to a directory does not contain any images, text files,
            or tfrecord files.

        ValueError
            This exception will be raised if the provided
            path to the dataset is not a string. Other raises are
            caused if the provided parameters
            in certain methods does not conform to the specified data type
            or the parameters are invalid. i.e. The image dimensions
            provided less than or equal to 0.
    """

    def __init__(
        self,
        source=None,
        gformat='yolo',
        absolute=False,
        validate_type='detection',
        show_missing_annotations=False
    ):
        self.source = source
        self.shape = None  # (height, width)
        self.format = gformat.lower()
        self.show_missing_annotations = show_missing_annotations
        self.absolute = absolute
        self.validate_type = validate_type

        if self.format not in ['yolo', 'pascalvoc', 'coco']:
            raise UnsupportedAnnotationFormatException(self.format)

        self.images, self.annotations = list(), list()

        self.transformer = None
        if self.format == 'yolo':
            self.transformer = self.yolo2xyxy
        elif self.format == 'coco':
            self.transformer = self.xywh2xyxy
        else:
            self.transformer = None

        self.normalizer = None
        self.denormalizer = None
        if absolute:
            if validate_type.lower() == 'detection':
                self.normalizer = self.normalize
        else:
            if validate_type.lower() == 'segmentation':
                self.denormalizer = self.denormalize_polygon

    @staticmethod
    def validate_input_source(source):
        """
        This method validates the existance of the source path.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_validate_input_source

        Parameters
        ----------

            source: str
                The path to the dataset.

        Returns
        -------
            source: str
                The validated path to the dataset.

        Raises
        ------
            InvalidDatasetSourceException
                This exception will be raised if the source
                to the dataset is None.

            DatasetNotFoundException
                This exception will be raised if the provided source
                to the dataset does not exist.

            ValueError
                This exception will be raised if the provided
                source to the dataset is not a string.
        """

        if source is None:
            raise InvalidDatasetSourceException(source)
        else:
            if not (isinstance(source, str)):
                raise ValueError(
                    "The provided path to the dataset is not a string. " +
                    "Recieved type: {}".format(
                        type(source)))
            if not os.path.exists(source):
                raise DatasetNotFoundException(source)
            else:
                return source
    
    @staticmethod
    def read_yaml_file(file_path):
        """
        This function reads yaml files internal to AuZone for collecting
        dataset information.
        Unit-test for this function is defined under:
            file: test/test_datasets.py
            function: test_read_yaml_file

        Parameters
        ----------

            file_path: str
                The path to the yaml file.

        Returns
        -------
            info_dataset: dict
                This contains the yaml file contents.
                For AuZoneRecords, the structure is defined as:
                {
                    "classes": [contains unique string labels of the dataset],
                    "type": "darknet",
                    "validation": {
                        "path": the path to the *.tfrecord files
                        }
                }

                For AuZoneNet, the structure is defined as:
                {
                    "classes": [contains unique string labels of the dataset],
                    "validation": {
                        "images": the path to the images,
                        "annotations": the path to the label annotations
                    }
                }

        Raises
        ------
            FileNotFoundError
                    This method will raise an exception if the provided
                    path to the labels.txt does not exist.
        """

        try:
            import yaml
        except ImportError:
            pass

        with open(file_path) as file:
            return yaml.full_load(file)

    def get_detection_dataset(
        self,
        source, 
        labels_path=None
        ):
        """
        This method inspects the *.yaml file contents if it exists.
        Otherwise it will search for either images with text
        annotations (Darknet) or tfrecord files (TFRecord Dataset).
        Unit-test for this method is defined under:
            file: test/test_datasets.py
            function: test_get_detection_dataset

        Parameters
        ----------

            source: str
                The validated path to the dataset.
                This can point to a yaml file or a directory containing
                tfrecords or images and text annotations.

            labels_path: str
                The path to the labels.txt (if provided).

        Returns
        -------
            dataset object: DarknetDataset or TFRecordDataset
                Depending on the dataset passed, the appropriate
                object will be created.

        Raises
        ------
            UnsupportedDatasetTypeException
                This method will raise an exception if the yaml file
                specifies a dataset type that is not recognized.
                Can only recognize (darknet or tfrecord).

            FileNotFoundError
                This method will raise an exception if the provided
                path to the labels.txt does not exist.

            EmptyDatasetException
                This method will raise an exception if the path
                provided does not contain any tfrecords, images,
                or text annotations.
        """

        source = Dataset.validate_input_source(source)

        if os.path.isdir(source):
            # Handle AuZoneNet and AuZoneTFRecords format.
            filename = "dataset_info.yaml"
            labels_file = "labels.txt"
            for root, _, files in os.walk(source):
                if filename in files:
                    return self.read_yaml_file(os.path.join(root, filename))
            
            if labels_path is None:  
                for root, _, files in os.walk(source):
                    if labels_file in files:
                        labels_path = os.path.join(root, labels_file)

            if labels_path is not None:
                labels_path = Dataset.validate_input_source(labels_path)
                if os.path.exists(labels_path):
                    with open(labels_path) as file:
                        labels = [line.rstrip().lower()
                                  for line in file.readlines()]
                else:
                    raise FileNotFoundError(
                        f"Labels file does not exist at: {labels_path}")
            else:
                labels = list()

            # Handles standard TFRecord datasets.
            info_dataset = dict()
            tfrecord_files = glob(os.path.join(source, "*.tfrecord"))
            if len(tfrecord_files) != 0:
                info_dataset["classes"] = labels
                info_dataset["validation"] = { "path": source }
                return info_dataset

            # Handles standard Darknet datasets.
            image_files = list()
            info_dataset = dict()
            for extension in ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']:
                if len(image_files) == 0:
                    image_files = glob(
                        os.path.join(source, f"*.{extension}")
                    )
                    image_source = source
                    if len(image_files) == 0:
                        image_files = glob(os.path.join(
                            source, f"images/validate/*.{extension}"))
                        image_source = os.path.join(
                            source, "images/validate"
                        )
                else:
                    for ext in ['*.txt', '*.json']:
                        annotation_files = glob(os.path.join(source, ext))
                        annotation_source = source
                        if len(annotation_files) == 0 or (
                            len(annotation_files) == 1 and os.path.basename(
                                annotation_files[0]) == "labels.txt"):
                            annotation_files = glob(os.path.join(
                                source, 'labels/validate/'+ ext))
                            annotation_source = os.path.join(
                                source, "labels/validate")
                            if len(annotation_files) == 0:
                                continue
                            else:
                                break
                        else:
                            break
                    
                    if len(annotation_files) == 0:
                        raise EmptyDatasetException("annotations", source)

                    info_dataset["type"] = "darknet"
                    info_dataset["classes"] = labels
                    info_dataset["validation"] = {
                        "images": image_source,
                        "annotations": annotation_source
                    }
                    return info_dataset
                    
        elif os.path.isfile(source):
            if os.path.basename(source) == "dataset_info.yaml":
                return self.read_yaml_file(source)
            elif os.path.splitext(source)[1] == ".txt":
                raise NotImplementedError(
                    "Single text file is not currently supported.")
            elif os.path.splitext(source)[1] == ".deepview":
                raise NotImplementedError(
                    "Deepview files are not currently supported.")
            else:
                UnsupportedDatasetTypeException(source)
        
        else:
            UnsupportedDatasetTypeException(source)

    @staticmethod
    def validate_dimension(dimension):
        """
        This method validates the dimension
        either height or width to be of type
        integers and cannot be less than or equal to 0.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_validate_dimension

        Parameters
        ----------

            dimension: int
                The dimension to validate.

        Returns
        -------
            dimension: int
                The validated dimension that is an integer
                and is greater than 0.

        Raises
        ------
            ValueError
                This method will raise an exception if the dimension
                is not an integer or it is less than or equal to 0.
        """

        if not (isinstance(dimension, int)):
            raise ValueError("The provided dimension is not an integer. " +
                             "Recieved type: {}".format(type(dimension)))
        elif (dimension <= 0):
            raise ValueError("The provided dimension is invalid. " +
                             "Recieved dimension: {}".format(dimension))
        else:
            return dimension

    @staticmethod
    def resize(image, size=None):
        """
        This method resizes the images depending on the size.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_resize

        Parameters
        ----------

            image: (height, width, 3) np.ndarray
                The image represented as a numpy array.

            size: (height, width) tuple
                Specify the size to resize.

        Returns
        -------
            image: (height, width, 3)
                Resized image.

        Raises
        ------
            ValueError
                This method will raise an exception if the
                provided image is not a np.ndarray or the given
                string image path does not exist.
        """

        if size is None:
            return image
        else:
            # Resize method requires (width, height)
            size = (size[1], size[0])
            if isinstance(image, str):
                if os.path.exists(image):
                    image = Image.open(image)
                    image = image.resize(size)
                    return np.asarray(image)
                else:
                    raise ValueError(
                        "The given image path does not exist at {}".format(
                            image)
                    )
            elif isinstance(image, np.ndarray):
                image = Image.fromarray(np.uint8(image))
                image = image.resize(size)
                return np.asarray(image)
            else:
                raise ValueError("The image provided is neither a " +
                                 "numpy array or a pillow image object. " +
                                 "Recieved type: {}".format(type(image)))

    @staticmethod
    def bgr2rgb(image):
        """
        This method converts BGR image to RGB image.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_bgr2rgb

        Parameters
        ----------

            image: (height, width, 3) np.ndarray
                The image as a BGR numpy array.

        Returns
        -------
            image: (height, width, 3) np.ndarray
                RGB image.

        Raises
        ------
            NotImplementedError
                This method is currently not implemented.
        """

        raise NotImplementedError("This method is currently not implemented.")

    @staticmethod
    def rgb2bgr(image):
        """
        This method converts RGB image to BGR image.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_rgb2bgr

        Parameters
        ----------

            image: (height, width, 3) np.ndarray
                The image as a RGB numpy array.

        Returns
        -------
            image: (height, width, 3) np.ndarray
                BGR image.

        Raises
        ------
            NotImplementedError
                This method is currently not implemented.
        """

        raise NotImplementedError("This method is currently not implemented.")

    @staticmethod
    def normalize(boxes, height, width):
        """
        This method normalizes the boxes to the width
        and height of the image or model input resolution.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_normalize

        Parameters
        ----------

            boxes: np.ndarray
                List of lists of floats [[boxes1], [boxes2]].
                Contains boxes to normalize.

            height: int
                The dimension to normalize the y-coordinates.

            width: int
                The dimension to normalize the x-coordinates.

        Returns
        -------
            Normalized boxes: np.ndarray
                new x-coordinate = old x-coordinate/width
                new y-coordinate = old y-coordinate/height

        Raises
        ------
            ValueError
                This method will raise an exception if the provided boxes
                is not a numpy array or if the provided height and width
                are not integers or they have invalid dimensions
                which are less than or equal to 0.
        """

        if not (isinstance(boxes, np.ndarray)):
            raise ValueError("The provided boxes is not a numpy array. " +
                             "Recieved type: {}".format(boxes))
        else:
            if not (isinstance(height, int) or isinstance(width, int)):
                raise ValueError(
                    "The provided width or height is not an integer. " +
                    "Recieved width: {} and height: {}".format(
                        type(width),
                        type(height)))
            elif (height <= 0 or width <= 0):
                raise ValueError(
                    "The provided width and height has invalid dimensions. " +
                    "Recieved width: {} and height: {}".format(
                        width,
                        height))
            else:
                boxes[..., 0:1] /= width
                boxes[..., 1:2] /= height
                boxes[..., 2:3] /= width
                boxes[..., 3:4] /= height
                return boxes

    @staticmethod
    def denormalize(boxes, height, width):
        """
        This method denormalizes the boxes from the width
        and height of the image or model input resolution.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_denormalize

        Parameters
        ----------

            boxes: np.ndarray
                List of lists of floats [[boxes1], [boxes2]].
                Contains boxes to denormalize.

            height: int
                The dimension to denormalize the y-coordinates.

            width: int
                The dimension to denormalize the x-coordinates.

        Returns
        -------
            Denormalized boxes: np.ndarray
                new x-coordinate = old x-coordinate*width
                new y-coordinate = old y-coordinate*height

        Raises
        ------
            ValueError
                This method will raise an exception if the provided boxes
                is not a numpy array or if the provided height and width are
                not integers or they have invalid dimensions which are less
                than or equal to 0.
        """

        if not (isinstance(boxes, np.ndarray)):
            raise ValueError("The provided boxes is not a numpy array. " +
                             "Recieved type: {}".format(boxes))
        else:
            if not (isinstance(height, int) or isinstance(width, int)):
                raise ValueError(
                    "The provided width or height is not an integer. " +
                    "Recieved width: {} and height: {}".format(type(width),
                                                               type(height)))
            elif (height <= 0 or width <= 0):
                raise ValueError(
                    "The provided width and height has invalid dimensions. " +
                    "Recieved width: {} and height: {}".format(width, height))
            else:
                boxes[..., 0:1] *= width
                boxes[..., 1:2] *= height
                boxes[..., 2:3] *= width
                boxes[..., 3:4] *= height
                return boxes

    @staticmethod
    def normalize_polygon(vertex, height, width):
        """
        This method normalizes the vertex
        coordinate of a polygon.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_normalize_polygon

        Parameters
        ----------

            vertex: list
                This contains [x, y] coordinate.

            height: int
                The dimension to normalize the y-coordinates.

            width: int
                The dimension to normalize the x-coordinates.

        Returns
        -------
            normalized coordinates: list
                This contains [x, y]

        Raises
        ------
            ValueError
                This method will raise an exception if the provided
                height and width are not integers or they have
                invalid dimensions which are less than or
                equal to 0.
        """

        if not (isinstance(height, int) or isinstance(width, int)):
            raise ValueError(
                "The provided width or height is not an integer. " +
                "Recieved width: {} and height: {}".format(
                    type(width),
                    type(height)))
        elif (height <= 0 or width <= 0):
            raise ValueError(
                "The provided width and height has invalid dimensions. " +
                "Recieved width: {} and height: {}".format(
                    width,
                    height))
        else:
            return [float(vertex[0]) / width, float(vertex[1]) / height]

    @staticmethod
    def denormalize_polygon(vertex, height, width):
        """
        This method denormalizes the vertex
        coordinate of a polygon.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_denormalize_polygon

        Parameters
        ----------

            vertex: list
                This contains [x, y] coordinate.

            height: int
                The dimension to denormalize the y-coordinates.

            width: int
                The dimension to denormalize the x-coordinates.

        Returns
        -------
            Denormalized coordinates: list
                This contains [x, y]

        Raises
        ------
            ValueError
                This method will raise an exception if the provided
                height and width are not integers or they have
                invalid dimensions which are less than or
                equal to 0.
        """

        if not (isinstance(height, int) or isinstance(width, int)):
            raise ValueError(
                "The provided width or height is not an integer. " +
                "Recieved width: {} and height: {}".format(
                    type(width),
                    type(height)))
        elif (height <= 0 or width <= 0):
            raise ValueError(
                "The provided width and height has invalid dimensions. " +
                "Recieved width: {} and height: {}".format(
                    width,
                    height))
        else:
            return [float(vertex[0]) * width, float(vertex[1]) * height]

    @staticmethod
    def yolo2xyxy(boxes):
        """
        This method converts yolo format into pascalvoc format.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_yolo2xyxy

        Parameters
        ----------

            boxes: np.ndarray
                Contains lists for each boxes in
                yolo format [[boxes1], [boxes2]]

        Returns
        -------
            boxes: np.ndarray
                Contains list for each boxes in
                pascalvoc format

        Raises
        ------
            ValueError
                This method will raise an exception if the
                provided boxes parameter is not a numpy array.
        """

        if not (isinstance(boxes, np.ndarray)):
            raise ValueError(
                "The parameter for boxes has an incorrect type. " +
                "Requires numpy array but recieved {}".format(
                    type(boxes)))
        else:
            w_c = boxes[..., 2:3]
            h_c = boxes[..., 3:4]
            boxes[..., 0:1] = boxes[..., 0:1] - w_c / 2
            boxes[..., 1:2] = boxes[..., 1:2] - h_c / 2
            boxes[..., 2:3] = boxes[..., 0:1] + w_c
            boxes[..., 3:4] = boxes[..., 1:2] + h_c
            return boxes

    @staticmethod
    def xywh2xyxy(boxes):
        """
        This method converts coco format to pascalvoc format.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_xywh2xyxy

        Parameters
        ----------

            boxes: np.ndarray
                Contains lists for each boxes in
                coco format [[boxes1], [boxes2]]

        Returns
        -------
            boxes: np.ndarray
                Contains list for each boxes in
                pascalvoc format

        Raises
        ------
            ValueError
                This method will raise an exception if the
                provided boxes parameter is not a numpy array.
        """

        if not (isinstance(boxes, np.ndarray)):
            raise ValueError(
                "The parameter for boxes has an incorrect type. " +
                "Requires numpy array but recieved {}".format(
                    type(boxes)))
        else:
            boxes[..., 2:3] = boxes[..., 2:3] + boxes[..., 0:1]
            boxes[..., 3:4] = boxes[..., 3:4] + boxes[..., 1:2]
            return boxes

    def build_dataset(self):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method.")

    def read_sample(self, instance):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method.")

    def read_all_samples(self, info="Validation Progress"):
        """
        This method reads all the samples in either Darknet or
        TFRecord datasets.
        Unit-test for this method is defined under:
            file: test/deepview/validator/datasets/test_core.py
            function: test_read_all_samples

        Parameters
        ----------

            info: str
                The description of why image instances are being read.
                By default it is to run validation,
                hence "Validation Progress".

        Returns
        -------
            ground truth instance: dict
                This method yeilds one sample of the ground truth
                instance which contains information on the image
                as a numpy array, boxes, labels, and image path.

        Raises
        ------
            None
        """

        try:
            from tqdm import tqdm
        except ImportError:
            pass

        try:
            instances = tqdm(self.build_dataset(), colour="green")
            instances.set_description(info)
            for instance in instances:
                yield self.read_sample(instance)

        except NameError:
            instances = self.build_dataset()
            num_samples = len(instances)
            for index in range(num_samples):
                print(
                    "\t - [INFO]: Computing Metrics for instance: " +
                    "%i of %i [%2.f %s]" %
                    (index + 1,
                     num_samples,
                     100 * ((index + 1) / float(num_samples)),
                     '%'), end='\r')
                yield self.read_sample(instances[index])
