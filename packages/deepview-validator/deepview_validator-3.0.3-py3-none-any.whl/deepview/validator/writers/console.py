# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.writers.core import Writer


class ConsoleWriter(Writer):
    """
    This class is used to print the metrics on the terminal.
    Unit-test for this class is defined under:
        file: test/test_console.py
    Parameters
    ----------
        None

    Raises
    ------
        None
    """

    def __init__(
        self
    ):
        super(ConsoleWriter, self).__init__()

    def __call__(self, message, parameters=None, validation_type='detection'):
        """
        When this is called, it prints the metrics on the console.
        Unit-test for this method is defined under:
            file: test/test_console.py
            function: test_print_metrics

        Parameters
        ----------

            message: dict.
                This message contains information regarding the
                metrics.

                * For detection:

                    .. code-block:: python

                        {
                            "model": Name of the model,
                            "engine": Engine used (npu, cpu, gpu),
                            "dataset": Name of the dataset,
                            "numgt": Number of ground truths in the dataset,
                            "Total TP": Total true positives,
                            "Total FN": Total false negatives,
                            "Total Class FP": Total classification false
                                              positives,
                            "Total Loc FP": Total localization false positives,
                            "OP": Overall precision,
                            "mAP": {'0.5': mAP at 0.5 IoU threshold,
                                    '0.75': mAP at 0.75 IoU threshold,
                                    '0.5:0.95': mAP across 0.5-0.95
                                                IoU thresholds
                                },
                            "OR": Overall recall,
                            "mAR": {'0.5': mAR at 0.5 IoU threshold,
                                    '0.75': mAR at 0.75 IoU threshold,
                                    '0.5:0.95': mAR across 0.5-0.95
                                                IoU thresholds
                                },
                            "OA": Overall Accuracy,
                            "mACC": {'0.5': mACC at 0.5 IoU threshold,
                                    '0.75': mACC at 0.75 IoU threshold,
                                    '0.5:0.95': mACC across 0.5-0.95
                                                IoU thresholds
                                    },
                            "LocFPErr": {'0.5': localization false positive
                                                ratio at 0.5 IoU threshold,
                                        '0.75': localization false positive
                                                ratio at 0.75 IoU threshold,
                                        '0.5:0.95': localization false positive
                                                    ratio across 0.5-0.95
                                                    IoU thresholds
                                        },
                            "ClassFPErr": { '0.5': classification false
                                                   positive ratio at 0.5
                                                   IoU threshold,
                                            '0.75': classification false
                                                    positive ratio at 0.75
                                                    IoU threshold,
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
                        "validation-threshold": Validation score
                                                threshold to filter
                                                predictions,
                        "detection-threshold": Detection score threshold
                                               for model NMS,
                        "nms": Type of NMS performed (standard, fast, matrix),
                        "normalization": Type of image normalization
                                       performed (raw, signed, unsigned, etc.),
                        "maximum_detections": Maximum detections set,
                        "warmup": Number of warmup iterations used,
                        "label offset": The label offset specified
                    }

            validation_type: str
                This is the type of validation performed.
                Either 'detection' or 'segmentation'.

        Returns
        -------

            header: str
                The validation header message.

            summary: str
                The formatted validation showing the metrics.

            timings: str
                The formatted timings of the model

        """

        if validation_type.lower() == 'detection':
            header, summary, timings = self.format_detection_summary(
                                            message, parameters
                                        )
        elif validation_type.lower() == 'segmentation':
            header, summary, timings = self.format_segmentation_summary(
                                            message
                                        )
        print(header)
        print(summary)
        if timings is not None:
            print(timings)

        return header, summary, timings
