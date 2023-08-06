# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

import numpy as np


class DetectionDataCollection:
    """
    This class acts as a container for DetectionLabelData objects
    for each label and provides methods to capture the
    total number of true positives, false positives, and
    false negatives in the dataset.
    Unit-test for this class is defined under:
        test/test_metrics.py

    Parameters
    ----------
        None

    Raises
    ------
        ValueError
            This will raise the exception if the provided parameters
            in certain methods does not conform to the specified data type
            or the parameters are out of bounds. i.e. The thresholds provided
            are greater than 1 or less than 0.
    """

    def __init__(self):

        # A list containing the DetectionLabelData objects for each label.
        self.label_data_list = list()
        # Total number of ground truths in the dataset.
        self.total_gt = 0
        # A list containing the strings of unique labels.
        self.labels = list()

    @staticmethod
    def validate_score(score, eps=1e-10):
        """
        The method validates the confidence score or the
        score threshold to be a floating type and does not
        exceed defined bounds (0...1).
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_validate_score_iou

        Parameters
        ----------

            score: float
                The score to validate.

        Returns
        -------
            score: float
                The validated score.

            eps: float
                Invalid score leniency.

        Raises
        ------
            ValueError
                This method will raise the exception if the provided score
                is not floating point type or it is out bounds
                (less than 0 or greater than 1).
        """

        if not isinstance(score, (float, np.float32)):
            raise ValueError(
                "The provided score is not of numeric type: float. " +
                "Provided with type: {}".format(
                    type(score)))
        if (score < 0 or score > 1. + eps):
            raise ValueError(
                "The provided score is out of bounds: {}. ".format(score) +
                "This value can only be between 0 and 1")
        else:
            return score

    @staticmethod
    def validate_iou(iou, eps=1e-10):
        """
        The method validates the IoU score or the
        IoU threshold to be a floating type and does not
        exceed defined bounds (0...1).
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_validate_score_iou

        Parameters
        ----------

            iou: float
                The iou to validate.

        Returns
        -------
            iou: float
                The validated IoU.

            eps: float
                Invalid IoU leniency.

        Raises
        ------
            ValueError
                This method will raise the exception if the provided IoU
                is not floating point type or it is out bounds
                (less than 0 or greater than 1).
        """

        if not isinstance(iou, (float, np.float32)):
            raise ValueError(
                "The provided iou is not of numeric type: float. " +
                "Provided with iou: {}".format(
                    type(iou)))
        if (iou < 0 or iou > 1. + eps):
            raise ValueError(
                "The provided iou is out of bounds: {}. ".format(iou) +
                "This value can only be between 0 and 1")
        else:
            return iou

    def add_gt(self, num=1):
        """
        This method adds the number of recorded ground truths
        of the dataset.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_add_get_gt

        Parameters
        ----------

        num: int
            The number of ground truths to add.

        Returns
        -------
            None

        Raises
        ------
            ValueError
                This method will raise the exception if the provided num
                are not integers or the value for num is a negative integer.
        """

        if not isinstance(num, (int, np.int32)):
            raise ValueError(
                "Unexpected input type is provided for num {}. ".format(
                    type(num)) + "It can only be of type integer."
            )
        else:
            if num < 0:
                raise ValueError(
                    "num cannot be a negative integer, {}".format(num)
                )
            else:
                self.total_gt += num

    def get_gt(self):
        """
        This method gets the number of recorded ground truths.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_add_get_gt

        Parameters
        ----------
            None

        Returns
        -------
            total ground truths: int
                The number of ground truths.

        Raises
        ------
            None
        """

        return self.total_gt

    def add_label_data(self, label):
        """
        This method adds DetectionLabelData object per label.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_add_get_label_data

        Parameters
        ----------

        label: str or int
            The string label or the integer index
            to place as a data container.

        Returns
        -------
            None

        Raises
        ------
            None
        """

        if not (isinstance(label, (str, int, np.int32, np.int64))):
            raise ValueError(
                "Unexpected input type is provided for label {}. ".format(
                    type(label)) + "It can only be of type integer or string.")
        else:
            self.label_data_list.append(DetectionLabelData(label))

    def get_label_data(self, label):
        """
        This method grabs the DetectionLabelData object by label.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_add_get_label_data

        Parameters
        ----------

        label: str or int
            A unique string label or integer index from the dataset.

        Returns
        -------
            None if the object does not exist.

            label_data: DetectionLabelData
                The data container of the label specified.

        Raises
        ------
            None
        """

        for label_data in self.label_data_list:
            if label_data.get_label() == label:
                return label_data
        return None

    def get_label_data_list(self):
        """
        This method gets the list containing the DetectionLabelData objects.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_add_get_label_data

        Parameters
        ----------
            None

        Returns
        -------
            label_data_list: list or np.ndarray
                The list containing the DetectionLabelData objects.

        Raises
        ------
            None
        """

        return self.label_data_list

    def get_labels(self):
        """
        This method gets the list containing the recorded
        unique string or integer index labels.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_capture_class

        Parameters
        ----------
            None

        Returns
        -------
            labels: list or np.ndarray
                The list containing the unique string or integer
                index labels.

        Raises
        ------
            None
        """

        return self.labels
    
    def reset_containers(self):
        """
        This method resets the label_data_list container to an empty list
        and resets the labels captured to an empty list.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_capture_class

        Parameters
        ----------
            None

        Returns
        -------
            None

        Raises
        ------
            None
        """

        self.label_data_list = []
        self.labels = []

    def capture_class(self, labels):
        """
        This method records the unique labels encountered
        in the prediction and ground truth and creates a
        container (DetectionLabelData) for each unique label found.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_capture_class

        Parameters
        ----------

            labels: list() or np.ndarray
                This list contains labels for one image.

        Returns
        -------
            None

        Raises
        ------
            None
        """

        for label in labels:
            if isinstance(label, str):
                if label.lower() in ["background", " ", ""]:
                    continue
            if label not in self.labels:
                self.add_label_data(label)
                self.labels.append(label)

    def categorize(
            self,
            index_matches,
            index_extra_dt,
            index_missed_gt,
            iou_list,
            gt_labels,
            dt_labels,
            scores
        ):
        """
        This method defines the predictions as either true positives,
        false positives, or false negatives.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function test_categorize_sum_outcomes

        Parameters
        ----------

            index_matches: list or np.ndarray
                This contains the indices of each match
                [[index_dt, index_gt]...].

            index_extra_dt: list or np.ndarray
                This contains indices of model
                predictions captured as local fp.

            index_missed_gt: list or np.ndarray
                This contains indices of ground truth that were not matched.

            iou_list: list or np.ndarray
                This contains the IoU values of all
                matches in respective order.

            gt_labels: list or np.ndarray
                This contains the ground truth string or integer index labels.

            dt_labels: list or np.ndarray
                This contains the model prediction string
                or integer index labels.

            scores: list or np.ndarray
                This contains the score values for each model prediction.

        Returns
        -------
            None

        Raises
        ------
            ValueError
                This method will raise the exception if the provided iou
                or score does not conform to the specified data type
                or the parameters are out of bounds. i.e. The provided iou
                or score is greater than 1 or less than 0.
        """

        self.add_gt(len(gt_labels))

        # Matched Predictions
        for match in index_matches:

            dt_label, gt_label = dt_labels[match[0]], gt_labels[match[1]]
            iou = iou_list[match[0]]
            score = scores[match[0]]

            if dt_label != gt_label:
                label_data = self.get_label_data(dt_label)
                if label_data is not None:
                    label_data.add_class_fp(iou, score)

            label_data = self.get_label_data(gt_label)
            if label_data is not None:
                label_data.add_gt()
                if dt_label == gt_label:
                    label_data.add_tp(iou, score)

        # Extra Predictions.
        for extra in index_extra_dt:
            dt_label = dt_labels[extra]
            score = scores[extra]

            label_data = self.get_label_data(dt_label)
            if label_data is not None:
                label_data.add_local_fp(score)

        # Missed Predictions.
        for missed in index_missed_gt:
            gt_label = gt_labels[missed]

            label_data = self.get_label_data(gt_label)
            if label_data is not None:
                label_data.add_gt()

    def sum_outcomes(self, iou_threshold, score_threshold):
        """
        This method adds the total number of
        true positives, false positives (localization and classification)
        and false negatives in the dataset at the specified validation
        IoU and score thresholds.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_categorize_sum_outcomes

        Parameters
        ----------

            iou_threshold: float
                Validation IoU threshold to consider true positives.

            score_threshold: float
                Validation score threshold to filter predictions.

        Returns
        -------
            outcomes: int
                The total number of true positives,
                false positives (local and class), and false negatives.

        Raises
        ------
            ValueError
                This method will raise the exception if the provided thresholds
                are not floating types or they are out bounds
                (less than 0 or greater than 1).
        """

        score_threshold = self.validate_score(score_threshold)
        iou_threshold = self.validate_iou(iou_threshold)
        total_tp, total_class_fp, total_local_fp = 0, 0, 0
        for label_data in self.label_data_list:

            total_tp += label_data.get_tp_count(iou_threshold, score_threshold)
            total_class_fp += label_data.get_class_fp_count(
                iou_threshold, score_threshold)
            total_local_fp += label_data.get_local_fp_count(
                iou_threshold, score_threshold)

        total_fn = self.total_gt - (total_tp + total_class_fp)
        return total_tp, total_fn, total_class_fp, total_local_fp


class DetectionLabelData:
    """
    This class acts a container that stores the total number
    of true positives,  false positives, false negatives per label
    and provides methods to calculate the mean average metrics.
    Unit-test for this class is defined under:
        file: test/test_metrics.py

    Parameters
    ----------

        label: str or int
            The unique string or integer index label to base the container.

    Raises
    ------
        ValueError
            The methods will raise an exception if the provided parameters
            do not conform to the specified data type in the method
            or the parameters are out of bounds such as the IoU
            and score threshold being greater than 1 or less than 0.
    """

    def __init__(
        self,
        label
    ):
        if not isinstance(label, (str, int, np.int32, np.int64)):
            raise ValueError("The provided label is neither string nor int. " +
                             "Recieved type: {}".format(type(label)))
        
        self.label = label
        # Total number of ground truths of the label
        self.gt = 0
        # Contains (IoU, score) values for predictions marked as true positives
        self.tps = list()
        # Contains (IoU, score) values for predictions marked as classification
        # false positives
        self.class_fps = list()
        # Contains score values for predictions captured as localization false
        # positives
        self.local_fps = list()

    def get_label(self):
        """
        This method grabs the class label being evaluated.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_set_label

        Parameters
        ----------
            None

        Returns
        -------
            label: str or int
                The string or integer index label.

        Raises
        ------
            None
        """

        return self.label

    def set_label(self, new_label):
        """
        This method sets the label to a different label.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_set_label

        Parameters
        ----------

            new_label: str or int
                The label to change.

        Returns
        -------
            None

        Raises
        ------
            ValueError
                This method will raise the exception if the provided label is
                neither string nor integer.
        """

        if not (isinstance(new_label, (str, int, np.int32, np.int64))):
            raise ValueError(
                "The provided label has an incorrect type: {}. ".format(
                    type(new_label)) + "Can only accept string or integer type.")
        else:
            self.label = new_label

    def add_gt(self, num=1):
        """
        This method adds the number of ground truth for the
        class label from the entire dataset.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_add_gt

        Parameters
        ----------

            num: int
                The number of ground truths to add.

        Returns
        -------
            None

        Raises
        ------
            ValueError
                This method will raise the exception if the provided
                num is not of type int or num is a negative integer.
        """

        if not (isinstance(num, (int, np.int32, np.int64))):
            raise ValueError(
                "The provided num has an incorrect type: {}. ".format(
                    type(num)) + "Can only accept integer type.")
        else:
            if num < 0:
                raise ValueError("The number of ground truths to add can " + 
                                 "can only be positive integers. " +
                                 "Recieved: {}".format(num))
            self.gt += num

    def get_gt(self):
        """
        This method gets the number of ground truths that is currently
        recorded.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_add_gt

        Parameters
        ----------
            None

        Returns
        -------
            self.gt: int
                The number of ground truths

        Raises
        ------
            None
        """

        return self.gt

    def get_tp_scores(self):
        """
        This method gets the prediction scores marked as true positives.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------
            None

        Returns
        -------
            scores: np.ndarray
                The true positive scores.

        Raises
        ------
            None
        """

        if len(self.tps):
            return np.array(self.tps)[:, 1]
        else:
            return np.array([])

    def get_tp_iou(self):
        """
        This method gets the prediction IoUs marked as true positives.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------
            None

        Returns
        -------
            IoUs: np.ndarray
                The true positive IoU values.

        Raises
        ------
            None
        """

        if len(self.tps):
            return np.array(self.tps)[:, 0]
        else:
            return np.array([])

    def get_class_fp_scores(self):
        """
        This method gets the prediction scores marked as
        classification false positives.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------
            None

        Returns
        -------
            scores: np.ndarray
                The classification false positive scores.

        Raises
        ------
            None
        """

        if len(self.class_fps):
            return np.array(self.class_fps)[:, 1]
        else:
            return np.array([])

    def get_class_fp_iou(self):
        """
        This method gets the prediction IoUs marked as
        classification false positives.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------
            None

        Returns
        -------
            IoUs: np.ndarray
                The classification false positive IoUs.

        Raises
        ------
            None
        """

        if len(self.class_fps):
            return np.array(self.class_fps)[:, 0]
        else:
            return np.array([])

    def get_local_fp_scores(self):
        """
        This method gets the prediction scores marked as
        localization false positives.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------
            None

        Returns
        -------
            scores: np.ndarray
                The localization false positive scores.

        Raises
        ------
            None
        """

        if len(self.local_fps):
            return np.array(self.local_fps)
        else:
            return np.array([])

    def add_tp(self, iou, score):
        """
        This method adds the true positive prediction IoU and
        confidence score. A true positive is when the prediction
        and the ground truth label matches and the IoU is
        greater than the set IoU threshold.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_add_truth_values

        Parameters
        ----------

            iou: float
                The IoU of the true positive prediction.

            score: float
                The confidence score of the true positive prediction.

        Returns
        -------
            None

        Raises
        ------
            ValueError
                This method will raise the exception if the provided
                iou and score are not floating types or they are out of bounds
                such as greater than 1 and less than 0.
        """

        score = DetectionDataCollection.validate_score(score)
        iou = DetectionDataCollection.validate_iou(iou)
        self.tps.append((iou, score))

    def add_class_fp(self, iou, score):
        """
        This method adds the false positive (classification) prediction
        IoU and confidence score. A false positive (classification)
        is when the prediction and the ground truth labels don't match
        and the IoU is greater than the set IoU threshold.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_add_truth_values

        Parameters
        ----------

            iou: float
                The IoU of the classification false positive prediction.

            score: float
                The confidence score of the classification false
                positive prediction.

        Returns
        -------
            None

        Raises
        ------
            ValueError
                This method will raise the exception if the provided
                iou and score are not floating types or they are out of bounds
                such as greater than 1 and less than 0.
        """

        score = DetectionDataCollection.validate_score(score)
        iou = DetectionDataCollection.validate_iou(iou)
        self.class_fps.append((iou, score))

    def add_local_fp(self, score):
        """
        This method adds the number of false positive (localization) captured.
        A false positive (localization) is when there is a
        prediction but no ground truth.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_add_truth_values

        Parameters
        ----------

            score: float
                The confidence score of the localization
                false positive prediction.

        Returns
        -------
            None

        Raises
        ------
            ValueError
                This method will raise an exception if the provided score
                is not a floating point type and is out bounds meaning it is
                greater than 1 or less than 0.
        """

        score = DetectionDataCollection.validate_score(score)
        self.local_fps.append(score)

    def get_tp_count(self, iou_threshold, score_threshold):
        """
        This method gets the number of true positives at the
        specified IoU threshold and score threshold.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------

            iou_threshold: float
                The IoU threshold to consider the true positives.

            score_threshold: float
                The score threshold to consider the predictions.

        Returns
        -------
            count: int
                The number of true positives at the specified
                IoU and score threshold.

        Raises
        ------
            ValueError
                This method will raise the exception if the provided
                iou_threshold and score_threshold are not floating
                types or they are out of bounds
                such as greater than 1 and less than 0.
        """

        score_threshold = DetectionDataCollection.validate_score(score_threshold)
        iou_threshold = DetectionDataCollection.validate_iou(iou_threshold)
        if len(self.tps):
            tp_iou = np.array(self.tps)[:, 0] >= iou_threshold
            tp_score = np.array(self.tps)[:, 1] >= score_threshold
            return np.count_nonzero(tp_iou * tp_score)
        else:
            return 0

    def get_class_fp_count(self, iou_threshold, score_threshold):
        """
        This method gets the number of classification false positives at
        the specified IoU and score threshold.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------

            iou_threshold: float
                The IoU threshold to consider classification false positives.

            score_threshold: float
                The score threshold to consider predictions.

        Returns
        -------
            count: int
                The number of classification false positives at the
                specified IoU and score threshold.

        Raises
        ------
            ValueError
                This method will raise the exception if the provided
                iou_threshold and score_threshold are not floating
                types or they are out of bounds
                such as greater than 1 and less than 0.
        """

        score_threshold = DetectionDataCollection.validate_score(score_threshold)
        iou_threshold = DetectionDataCollection.validate_iou(iou_threshold)
        if len(self.class_fps):
            fp_iou = np.array(self.class_fps)[:, 0] >= iou_threshold
            fp_score = np.array(self.class_fps)[:, 1] >= score_threshold
            return np.count_nonzero(fp_iou * fp_score)
        else:
            return 0

    def get_local_fp_count(self, iou_threshold, score_threshold):
        """
        This method gets the number of localization false positives
        at the specified IoU and score threshold.
        The IoU threshold is needed because true positives that have
        an IoU less than the set IoU threshold will be considered as
        localization false positives.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------

            iou_threshold: float
                The IoU threshold to consider true positives as local
                false positives.

            score_threshold: float
                The score threshold to consider predictions.

        Returns
        -------
            count: int
                The number of localization false positives at the
                specified IoU and score threshold.

        Raises
        ------
            ValueError
                This method will raise the exception if the provided
                iou_threshold and score_threshold are not floating
                types or they are out of bounds
                such as greater than 1 and less than 0.
        """

        score_threshold = DetectionDataCollection.validate_score(score_threshold)
        iou_threshold = DetectionDataCollection.validate_iou(iou_threshold)
        if len(self.tps):
            # Any predictions that are below the IoU thresholds are
            # localization false positives.
            fp_iou = np.array(self.tps)[:, 0] < iou_threshold
            tp_score = np.array(self.tps)[:, 1] >= score_threshold
            return np.count_nonzero(
                fp_iou * tp_score) + np.count_nonzero(
                np.array(self.local_fps) >= score_threshold)
        else:
            return np.count_nonzero(
                np.array(self.local_fps) >= score_threshold)

    def get_fn_count(self, iou_threshold, score_threshold):
        """
        This method gets the number of false negatives
        at the specified IoU threshold and score threshold.
        Score threshold is needed because by principle fp = gt - tp,
        and score and IoU threshold is required to find the
        number of true positives.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_get_truth_values

        Parameters
        ----------

            iou_threshold: float
                The IoU threshold to consider true positives.

            score_threshold: float
                The score threshold to consider predictions.

        Returns
        -------
            count: int
                The number of false negatives at the specified
                IoU and score threshold.

        Raises
        ------
            ValueError
                This method will raise the exception if the provided
                iou_threshold and score_threshold are not
                floating types or they are out of bounds
                such as greater than 1 and less than 0.

        """

        return self.gt - self.get_tp_count(iou_threshold, score_threshold)
