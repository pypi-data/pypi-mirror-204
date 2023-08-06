# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import UnsupportedNormalizationException
from deepview.validator.exceptions import UnsupportedEngineException
from deepview.validator.exceptions import NonMatchingIndexException
from deepview.validator.exceptions import UnsupportedNMSException
from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.writers.core import Writer
from deepview.validator.runners.core import Runner
from time import monotonic_ns as clock_now
from os.path import exists
from timeit import timeit
import numpy as np


class DeepViewRTRunner(Runner):
    """
    This class runs DeepViewRT models using the VAAL API.
    Unit-test for this class is defined under:
        file: test/deepview/validator/runners/test_deepviewrt.py

    Parameters
    ----------

        model_path: str
            The path to the model.

        labels: list
            Unique string labels.

        max_detections: int
            The maximum detections to output.

        warmup: int
            The number of warmup iterations to perform.

        engine: str
            The type of engine to run the model (cpu, npu, gpu).

        norm: str
            The type of image normalization to perform
            (raw, unsigned, signed, whitening, imagenet).

        nms_type: str
            The type of non max supression to perform (standard, fast, matrix).

        detection_score_threshold: float
            NMS score threshold from 0 to 1.

        detection_iou_threshold: float
            NMS iou threshold from 0 to 1.

        label_offset: int
            The index offset to match label index to the ground truth index.

        box_format: str
            The box format to output the model predictions.

    Raises
    ------
        UnsupportedNormalizationException
            This exception will be raised if the passed image normalization is
            not recognized.

        UnsupportedEngineException
            This exception will be raised if the passed engine is not
            recognized.

        NonMatchingIndexException
            This exception will be raised if the model outputs an index
            that is out of bounds to the labels list passed
            or the labels contained within the model itself.

        UnsupportedNMSException
            This exception will be raised if the NMS provided is not
            recognized.

        MissingLibraryException
            This exception will be raised if the deepview.vaal library
            is not found.

        NotImplementedError
            Some methods have not been implemented yet.

        ValueError
            This method will raise an exception if the provided image_path
            does not exist and the provided image is not a numpy.ndarray.
    """

    def __init__(
        self,
        model_path,
        labels,
        max_detections=100,
        warmup=0,
        engine='npu',
        norm='raw',
        nms_type=None,
        detection_score_threshold=0.5,
        detection_iou_threshold=0.5,
        label_offset=0,
        box_format='xyxy'
    ):
        super(DeepViewRTRunner, self).__init__(model_path)

        self.labels = labels
        self.label_offset = label_offset

        try:
            import deepview.vaal as vaal
        except ImportError:
            raise MissingLibraryException(
                "vaal library is needed to run DeepViewRT models.")

        if engine.lower() not in ['npu', 'cpu', 'gpu']:
            raise UnsupportedEngineException(engine)

        try:
            self.ctx = vaal.Context(engine)
        except AttributeError:
            raise EnvironmentError(
                'Did not find Vaal Context. Try setting the environment \
                    variable VAAL_LIBRARY to the VAAL library.')
        self.device = self.ctx.device

        if nms_type is not None:
            if nms_type.lower() not in ['standard', 'fast', 'matrix']:
                raise UnsupportedNMSException(nms_type)
            self.ctx['nms_type'] = nms_type

        if norm.lower() not in [
            'raw',
            'signed',
            'unsigned',
            'whitening',
                'imagenet']:
            raise UnsupportedNormalizationException(self.norm)

        if max_detections is not None:
            self.ctx['max_detection'] = max_detections

        self.ctx['box_format'] = box_format
        self.ctx['score_threshold'] = detection_score_threshold
        self.ctx['iou_threshold'] = detection_iou_threshold

        if norm is not None:
            if norm == 'raw':
                self.ctx['normalization'] = vaal.ImageProc.RAW.value
            elif norm == 'signed':
                self.ctx['proc'] = vaal.ImageProc.SIGNED_NORM.value
            elif norm == 'unsigned':
                self.ctx['proc'] = vaal.ImageProc.UNSIGNED_NORM.value
            elif norm == 'whitening':
                self.ctx['proc'] = vaal.ImageProc.WHITENING.value
            elif norm == 'imagenet':
                self.ctx['proc'] = vaal.ImageProc.IMAGENET.value
            else:
                Writer.logger(
                    f"Unsupported normalization method: {norm}", code="ERROR")

        self.ctx.load_model(model_path)
        if int(warmup) > 0:
            Writer.logger("Loading model and warmup...", code="INFO")
            t = timeit(self.ctx.run_model, number=self.warmup)
            Writer.logger("model warmup took %f seconds (%f ms avg)\n" %
                          (t, t * 1000 / self.warmup), code="INFO")

    def run_single_instance(self, image):
        """
        This method runs deepviewrt models and parses the prediction
        bounding boxes, scores, and labels and records timings
        (load, inference, box).
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_deepviewrt.py
            function: test_run_single_instance

        Parameters
        ----------

            image: str or np.ndarray
                If the dataset is Darknet, then the image path is used which
                is a string.
                If the dataset is TFRecords, then the image is a
                np.ndarray.

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
            ValueError
                This method will raise an exception if the provided image_path
                does not exist and the provided image is not a numpy.ndarray.
        """

        if isinstance(image, str):
            start = clock_now()
            if exists(image):
                self.ctx.load_image(image)
            else:
                raise ValueError(
                    "The provided image path does not exist at: {}".format(
                        image))
            load_ns = clock_now() - start
        elif isinstance(image, np.ndarray):
            start = clock_now()
            rgba_image = np.concatenate(
                (image, np.zeros((image.shape[0], image.shape[1], 1))), axis=2)
            self.ctx.load_image(rgba_image.astype(np.uint8))
            load_ns = clock_now() - start
        else:
            raise ValueError(
                "The provided image is neither a path nor a np.ndarray. " +
                "Provided with type: {}".format(type(image)))

        self.loading_input_timings.append(load_ns * 1e-6)

        start = clock_now()
        self.ctx.run_model()
        infer_ns = clock_now() - start
        self.inference_timings.append(infer_ns * 1e-6)

        start = clock_now()
        bxs = self.ctx.boxes()
        boxes, classes, scores = self.postprocessing(bxs)
        boxes_ns = clock_now() - start
        self.box_timings.append(boxes_ns * 1e-6)

        return boxes, classes, scores

    def postprocessing(self, outputs):
        """
        This method collects the bounding boxes, scores and
        labels for the image.
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_deepviewrt.py
            function: test_postprocessing

        Parameters
        ----------

            outputs:
                This contains bounding boxes, scores, labels.

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
                This method will raise an exception if the model label
                index is out of bounds to the input labels list
                or the unique labels contained within the model.
        """

        boxes, classes, scores = list(), list(), list()

        for box in outputs:
            boxes.append([box.xmin, box.ymin, box.xmax, box.ymax])
            scores.append(box.score)

            label = box.label + self.label_offset

            if len(self.labels):
                if len(self.ctx.labels):
                    try:
                        dt_class = self.ctx.labels[label].lower().rstrip(
                            '\"').lstrip('\"')
                    except IndexError:
                        raise NonMatchingIndexException(label)
                    classes.append(dt_class)
                else:
                    # raise ModelUnknownLabelsException(model=self.source)
                    try:
                        dt_class = self.labels[label].lower().rstrip(
                            '\"').lstrip('\"')
                    except IndexError:
                        raise NonMatchingIndexException(label)
                    classes.append(dt_class)
            else:
                classes.append(label)

        boxes = np.array(boxes)
        classes = np.array(classes)
        scores = np.array(scores)

        return boxes, classes, scores

    def clamp(self, value, min=0, max=1):
        """
        This method clamps a given value between 0 and 1 by default. If
        the value is in between the set min and max, then it is returned.
        Otherwise it returns either min or max depending on
        which is the closest.
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_deepviewrt.py
            function: test_clamp

        Parameters
        ----------

            value: float or int
                Value to clamp between 0 and 1 (defaults).

            min: int or float
                Minimum acceptable value.

            max: int or float
                Maximum acceptable value.

        Returns
        -------
            value: int or float
                This is the clamped value.
        """

        return min if value < min else max if value > max else value

    def get_input_type(self):
        """
        This method returns the model input type.
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_deepviewrt.py
            function: test_get_input_type

        Parameters
        ----------
            None

        Returns
        -------
            type: str
                The model input type

        Raises
        ------
            NotImplementedError
                This method will raise an exception because it has not
                been implemented yet.
        """

        raise NotImplementedError("This method has not been implemented.")

    def get_output_type(self):
        """
        This method returns the model output type.
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_deepviewrt.py
            function: test_get_output_type

        Parameters
        ----------
            None

        Returns
        -------
            type: str
                The model output type

        Raises
        ------
            NotImplementedError
                This method will raise an exception because it has not
                been implemented yet.
        """

        raise NotImplementedError("This method has not been implemented.")

    def get_input_shape(self):
        """
        This method gets the model input shape.
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_deepviewrt.py
            function: test_get_input_shape

        Parameters
        ----------
            None

        Returns
        -------
            type: tuple or list
                The model input shape.

        Raises
        ------
            NotImplementedError
                This method will raise an exception because it has not
                been implemented yet.
        """

        raise NotImplementedError("This method has not been implemented.")
