# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import ZeroUniqueLabelsException
from deepview.validator.metrics.core import Metrics


class SegmentationMetrics(Metrics):
    """
    This class provides methods to calculate:

        - precision.
                -> overall precision.

                -> mAP.
        - recall.
                -> overall recall.

                -> mAR.
        - accuracy.
                -> overall accuracy.

                -> mACC.

    Unit-test for this class is defined under:
        test/deepview/validator/metrics/test_segmentationmetrics.py

    Parameters
    ----------

        segmentationdatacollection: SegmentationDataCollection
            This contains the number of ground truths in the dataset
            and tp, fp, and fn per class.

    Raises
    ------
        DivisionByZeroException
                This will raise an exception if a division of zero
                is encountered when calculating precision, recall, or accuracy.

        ZeroUniqueLabelsException
                This method will raise an exception if the number of unique
                labels captured is zero.

        ValueError
            This will raise the exception if the provided parameters
            in certain methods does not conform to the specified data type.
    """

    def __init__(
        self,
        segmentationdatacollection=None
    ):
        super(SegmentationMetrics, self).__init__()
        self.segmentationdatacollection = segmentationdatacollection

    def compute_overall_metrics(self, total_tp, total_fn, total_fp):
        """
        This method computes the overall precision, recall, and accuracy.

            - overall precision = sum tp/(sum tp + sum fp).
            - overall recall = sum tp/(sum tp + sum fn).
            - overall accuracy  = sum tp/(sum tp + sum fn + sum fp).

        Unit-test for this method is defined under:
            file: test/deepview/validator/metrics/test_segmentationmetrics.py
            function: test_compute_overall_metrics

        Parameters
        ----------

            total_tp: int
                Total number of true positives in the dataset.

            total_fn: int
                Total number of false negatives in the dataset.

            total_fp: int
                Total number of false positives in the dataset.

        Returns
        -------
            overall metrics: list
                This contains overall precision, overall recall,
                and overall accuracy.

        Raises
        ------
            DivisionByZeroException
                This method will raise an exception if a division of zero
                is encountered when calculating precision, recall, or accuracy.
        """

        if total_tp == 0:
            return [0., 0., 0.]
        else:
            overall_precision = self.compute_precision(total_tp, total_fp)
            overall_recall = self.compute_recall(total_tp, total_fn)
            overall_accuracy = self.compute_accuracy(
                total_tp, total_fp, total_fn)
            return [overall_precision, overall_recall, overall_accuracy]

    def compute_segmentation_metrics(self):
        """
        This method computes mAP, mAR, maAccuracy for segmentation.

        - mean average precision = (sum of precision for every class) /
                                            (total number of unique classes).
        - mean average recall = (sum of recall for every class) /
                                            (total number of unique classes).
        - mean average accuracy = (sum of accuracy for every class) /
                                            (total number of unique classes).

        Unit-test for this method is defined under:
            file: test/deepview/validator/metrics/test_segmentationmetrics.py
            function: test_get_segmentation_metrics

        Parameters
        ----------
            None

        Returns
        -------
            class metrics: list
                This contains mean average precision, recall, and accuracy.

            class histogram data: dict
                This contains the number of true positives, false positives,
                and false negatives and aswell as precision, recall,
                and accuracy to plot as a histogram.

        Raises
        ------
            ZeroUniqueLabelsException
                This method will raise an exception if the number of unique
                labels captured is zero.

            DivisionByZeroException
                This method will raise an exception if a division of zero
                is encountered when calculating precision, recall, or accuracy.
        """

        mmap, mar, macc = 0, 0, 0
        num_class = len(self.segmentationdatacollection.label_data_list)
        if num_class == 0:
            raise ZeroUniqueLabelsException()
        else:
            class_histogram_data = dict()

        for label_data in self.segmentationdatacollection.label_data_list:

            precision = self.compute_precision(
                label_data.tps,
                label_data.fps
            )
            recall = self.compute_recall(
                label_data.tps,
                label_data.fns
            )
            accuracy = self.compute_accuracy(
                label_data.tps,
                label_data.fps,
                label_data.fns
            )

            mmap += precision
            mar += recall
            macc += accuracy

            class_histogram_data[label_data.get_label()] = {
                'precision': precision,
                'recall': recall,
                'accuracy': accuracy,
                'tp': int(label_data.tps),
                'fp': int(label_data.fps),
                'fn': int(label_data.fns),
                'gt': int(label_data.gt)
            }

        mmap /= num_class
        mar /= num_class
        macc /= num_class
        return [mmap, mar, macc], class_histogram_data
