# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.writers.core import Writer
import numpy as np
from os import path

try:
    import tensorflow as tf
except ImportError:
    pass


class TensorBoardWriter(Writer):
    """
    This class is used to publish the images and the metrics onto TensorBoard.
    Unit-test for this class is defined under:
        file: test/test_tensorboard.py

    Parameters
    ----------

        logdir: str
            This is the path to the tfevents file.

    Raises
    ------
        None
    """

    def __init__(
        self,
        logdir=None
    ):
        super(TensorBoardWriter, self).__init__()

        self.logdir = logdir
        self.writer = None
        if logdir:
            self.writer = tf.summary.create_file_writer(self.logdir)

    def __call__(self, image, image_path, step=0):
        """
        When it is called, it publishes the images onto tensorboard.
        Unit-test for this method is defined under:
            file: test/test_tensorboard.py
            function: test_tensorboard_image_display

        Parameters
        ----------

            image: (height, width, 3) np.ndarray
                The image array to display to tensorboard

            image_path: str
                The path to the image.

            step: int
                This represents the number of the current epoch when training
                a model.

        Returns
        -------
            None

        Raises
        ------
            None
        """

        with self.writer.as_default():
            nimage = np.expand_dims(image, 0)
            tf.summary.image(
                path.basename(image_path),
                nimage,
                step=step
            )
            self.writer.flush()

    def publish_metrics(
            self,
            message,
            parameters=None,
            step=0,
            validation_type='detection'):
        """
        This method publishes the metric summary onto tensorboard.
        Unit-test for this method is defined under:
            file: test/test_tensorboard.py
            function: test_publish_metrics

        Parameters
        ----------

            message: dict
                This contains the validation metrics.

                * For detection:

                .. code-block:: python

                    {
                        "model": Name of the model,
                        "engine": Engine used (npu, cpu, gpu),
                        "dataset": Name of the dataset,
                        "numgt": Number of ground truths in the dataset,
                        "Total TP": Total true positives,
                        "Total FN": Total false negatives,
                        "Total Class FP": Total classification false positives,
                        "Total Loc FP": Total localization false positives,
                        "OP": Overall precision,
                        "mAP": {'0.5': mAP at 0.5 IoU threshold,
                                '0.75': mAP at 0.75 IoU threshold,
                                '0.5:0.95': mAP across 0.5-0.95 IoU thresholds
                            },
                        "OR": Overall recall,
                        "mAR": {'0.5': mAR at 0.5 IoU threshold,
                                '0.75': mAR at 0.75 IoU threshold,
                                '0.5:0.95': mAR across 0.5-0.95 IoU thresholds
                            },
                        "OA": Overall Accuracy,
                        "mACC": {'0.5': mACC at 0.5 IoU threshold,
                                '0.75': mACC at 0.75 IoU threshold,
                                '0.5:0.95': mACC across 0.5-0.95 IoU thresholds
                                },
                        "LocFPErr": {'0.5': localization false positive ratio
                                            at 0.5 IoU threshold,
                                    '0.75': localization false positive ratio
                                            at 0.75 IoU threshold,
                                    '0.5:0.95': localization false positive
                                                ratio across 0.5-0.95
                                                IoU thresholds
                                    },
                        "ClassFPErr": { '0.5': classification false positive
                                               ratio at 0.5 IoU threshold,
                                        '0.75': classification false positive
                                                ratio at 0.75 IoU threshold,
                                        '0.5:0.95': classification false
                                                    positive ratio across
                                                    0.5-0.95 IoU thresholds
                                    },
                        "timings": timings
                                (input, inference, decode at min/max/avg)
                    }

                * For segmentation:

                .. code-block:: python

                    {
                        "model": Name of the model,
                        "engine": Engine used (npu, cpu, gpu),
                        "dataset": Name of the dataset,
                        "numgt": Number of ground truths in the dataset,
                        "Total TP": Total true positives,
                        "Total FN": Total false negatives,
                        "Total FP": Total false positives,
                        "OP": Overall precision,
                        "OR": Overall recall,
                        "OA": Overall Accuracy,
                        "mAP": Mean average precision,
                        "mAR": Mean average recall,
                        "mACC": Mean average accuracy,
                        "timings": timings
                            (input, inference, decode at min/max/avg)
                    }

            parameters: dict
                This contains information regarding the model and
                validation parameters.

                .. code-block:: python

                    {
                        "validation-iou": Validation IoU used to
                                          consider true positives,
                        "detection-iou": Detection IoU for model NMS,
                        "validation-threshold": Validation score threshold
                                                to filter predictions,
                        "detection-threshold": Detection score threshold
                                               for model NMS,
                        "nms": Type of NMS performed (standard, fast, matrix),
                        "normalization": Type of image normalization
                                      performed (raw, signed, unsigned, etc.),
                        "maximum_detections": Maximum detections set,
                        "warmup": Number of warmup iterations used,
                        "label offset": The label offset specified
                    }

            step: int
                This is the iteration number which represents the
                epoch number when training a model.

            validation_type: str
                This is the type of validation performed
                (detection or segmentation).

        Returns
        -------
            None

        Raises
        ------
            None
        """

        with self.writer.as_default():

            if validation_type.lower() == 'detection':
                header, summary, timings = self.format_detection_summary(
                    message, parameters
                )
            elif validation_type.lower() == 'segmentation':
                header, summary, timings = self.format_segmentation_summary(
                    message
                )

            if timings is None:
                timings = "None"
            tf.summary.text(
                header,
                summary,
                step=step
            )
            tf.summary.text(
                "Timing Results",
                timings,
                step=step
            )
            self.writer.flush()


class TrainingTensorBoardWriter(TensorBoardWriter):
    """
    This class is used to publish metrics on training a model.
    Unit-test for this class is defined under:
        file: test/test_tensorboard.py

    Parameters
    ----------

        writer: TF.summary file writer object
            This is the writer object defined in trainer.

    Raises
    ------
        None
    """

    def __init__(
        self,
        writer
    ):
        super(TrainingTensorBoardWriter, self).__init__()
        self.writer = writer
