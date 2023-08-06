# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import DivisionByZeroException
import numpy as np


class Metrics:
    """
    This class is an abstract class that provides a template for the
    metric computations.
    Unit-test for this class is defined under:
        file: test/test_metrics.py

    Parameters
    ----------
    None

    Raises
    ------
        DivisionByZeroException
            This will raise the exception if a ZeroDivisionError is caught.

        ValueError
            This will raise the exception if the provided parameters
            in certain methods does not conform to the specified data type
            or the parameters are out of bounds. i.e. The thresholds provided
            are greater than 1 or less than 0.
    """

    def __init__(
        self
    ):
        pass

    @staticmethod
    def validate_threshold(threshold, eps=1e-10):
        """
        The method validates the threshold to be a floating type
        and does not exceed defined bounds (0...1).
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_validate_threshold

        Parameters
        ----------

            threshold: float
                The threshold to validate.

        Returns
        -------
            threshold: float
                The validated threshold.

        Raises
        ------
            ValueError
                This method will raise the exception if the provided threshold
                is not floating point type or it is out bounds
                (less than 0 or greater than 1).
        """

        if not (isinstance(threshold, (float, np.float32))):
            raise ValueError(
                "The provided threshold is not of numeric type: float. " +
                "Provided with: {}".format(
                    type(threshold)))
        if (threshold <= 0 or threshold >= 1. + eps):
            raise ValueError(
                "The provided threshold is out of bounds: {}. ".format(
                    threshold) + "This value can only be between 0 and 1")
        else:
            return threshold

    @staticmethod
    def divisor(num, denom, info='Basic Division'):
        """
        This method performs basic division operations for ratio metrics.
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_divisor

        Parameters
        ----------

        num: int, float, complex
            This is the numerator in the division.

        denom: int, float, complex
            This is the denominator in the division.

        info: str
            This is the description of the operation.
            i.e what is being calculated?

        Returns
        -------
            The division result: int, float, complex
                Resulting value is the result when num/denom is performed.

        Raises
        ------
            DivisionByZeroException
                This method will raise the exception
                if the denominator provided is 0.

            ValueError
                This method will raise the exception
                if the provided parameters for num and denom
                are not numeric types (int, float, complex).
        """

        if not (isinstance(info, str)):
            raise ValueError(
                "Unexpected input type of info is provided. " +
                "The parameter for info should be of type string. " +
                "Provided with info: {}".format(
                    type(info)))
        
        if not (isinstance(num, (int, float, complex)) or 
                isinstance(num, (np.int32, np.float32, np.complex128))):
            raise ValueError(
                "Unexpected input type of num is provided. " +
                "It should be a numeric datatype of type int, float,  " +
                "or complex. Provided with num: {} ".format(
                    type(num))
                )
        elif not (isinstance(denom, (int, float, complex)) or 
                  isinstance(denom, (np.int32, np.float32, np.complex128))):
            raise ValueError(
                "Unexpected input type of denom is provided. " +
                "It should be a numeric datatype of type int, float,  " +
                "or complex. Provided with denom: {} ".format(
                    type(denom))
                )
        else:
            try:
                return num / denom
            except ZeroDivisionError:
                raise DivisionByZeroException(
                    info,
                    num,
                    denom
                )

    @staticmethod
    def compute_precision(tp, fp):
        """
        This method calculates the precision = tp/(tp+fp).
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_compute_precision

        Parameters
        ----------

        tp: int
            The number of true positives.

        fp: int
            The number of false positives.

        Returns
        -------
            Precision score: float
                Resulting value is the result of tp/(tp+fp).

        Raises
        ------
            DivisionByZeroException
                This method will raise the exception if tp + fp = 0.

            ValueError
                This method will raise the exception if the
                provided parameters for tp and fp
                are not integers or the values for tp and fp
                are negative integers.
        """

        if not isinstance(tp, (int, np.int32)):
            raise ValueError(
                "Unexpected input type of tp is provided. " +
                "It should be type int. " +
                "Provided with tp: {} ".format(type(tp))
            )
        elif not isinstance(fp, (int, np.int32)):
            raise ValueError(
                "Unexpected input type of fp is provided. " +
                "It should be type int. " +
                "Provided with fp: {} ".format(type(fp))
            )
        else:
            if (tp < 0 or fp < 0):
                raise ValueError(
                    "tp or fp cannot be less than 0. " +
                    "Provided with tp: {} and fp: {}".format(tp,fp)
                )
            else:
                try:
                    return tp / (tp + fp)
                except ZeroDivisionError:
                    raise DivisionByZeroException(
                        "precision",
                        tp,
                        (tp + fp)
                    )

    @staticmethod
    def compute_recall(tp, fn):
        """
        This method calculates the recall = tp/(tp+fn).
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_compute_recall

        Parameters
        ----------

        tp: int
            The number of true positives.

        fn: int
            The number of false negatives.

        Returns
        -------
            Recall score: float
                Resulting value is the result of tp/(tp+fn).

        Raises
        ------
            DivisionByZeroException
                This method will raise the exception if tp + fn = 0.

            ValueError
                This method will raise the exception
                if the provided parameters for tp and fn
                are not integers or the values for tp
                and fn are negative integers.
        """

        if not isinstance(tp, (int, np.int32)):
            raise ValueError(
                "Unexpected input type of tp is provided. " +
                "It should be type int. " +
                "Provided with tp: {} ".format(type(tp))
            )
        elif not isinstance(fn, (int, np.int32)):
            raise ValueError(
                "Unexpected input type of fn is provided. " +
                "It should be type int. " +
                "Provided with fn: {} ".format(type(fn))
            )
        else:
            if (tp < 0 or fn < 0):
                raise ValueError(
                    "tp or fn cannot be less than 0. " +
                    "Provided with tp: {} and fn: {}".format(tp,fn)
                )
            else:
                try:
                    return tp / (tp + fn)
                except ZeroDivisionError:
                    raise DivisionByZeroException(
                        "recall",
                        tp,
                        (tp + fn)
                    )

    @staticmethod
    def compute_accuracy(tp, fp, fn):
        """
        This method calculates the accuracy = tp/(tp+fp+fn).
        Unit-test for this method is defined under:
            file: test/test_metrics.py
            function: test_compute_accuracy

        Parameters
        ----------

        tp: int
            The number of true positives.

        fp: int
            The number of false positives.

        fn: int
            The number of false negatives.

        Returns
        -------
            Accuracy score: float
                Resulting value is the result of tp/(tp+fp+fn).

        Raises
        ------
            DivisionByZeroException
                This method will raise the exception if tp + fp + fn = 0.

            ValueError
                This method will raise the exception
                if the provided parameters for tp, fp, and fn
                are not integers or the values for tp, fp,
                or fn are negative integers.
        """

        if not isinstance(tp, (int, np.int32)):
            raise ValueError(
                "Unexpected input type of tp is provided. " +
                "It should be type int. " +
                "Provided with tp: {}".format(type(tp))
            )
        elif not isinstance(fp, (int, np.int32)):
            raise ValueError(
                "Unexpected input type of fp is provided. " +
                "It should be type int. " +
                "Provided with fp: {}".format(type(fp))
            )
        elif not isinstance(fn, (int, np.int32)):
            raise ValueError(
                "Unexpected input type of fn is provided. " +
                "It should be type int. " +
                "Provided with fn: {}".format(type(fn))
            )
        else:
            if (tp < 0 or fp < 0 or fn < 0):
                raise ValueError(
                    "tp, fn, or fp cannot be less than 0. " +
                    "Provided with tp: {}, fp: {}, fn: {}.".format(
                        tp,
                        fp,
                        fn)
                )
            else:
                try:
                    return tp / (tp + fp + fn)
                except ZeroDivisionError:
                    raise DivisionByZeroException(
                        "accuracy",
                        tp,
                        (tp + fp + fn)
                    )