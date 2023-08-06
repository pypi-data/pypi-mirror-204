# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import InvalidModelSourceException
from os.path import exists
import numpy as np


class Runner:
    """
    This class is an Abstract Class that provides a template
    for the other runner classes.
    Unit-test for this class is defined under:
        file: test/deepview/validator/runners/test_core.py

    Parameters
    ----------

        source: str
            This is the path to the model, TRT engine,
            or a directory of text files.

    Raises
    ------
        InvalidModelSourceException
            This exception will be raised if source is None.

        FileNotFoundError
            This exception will be raised if the path to the
            model does not exist.
    """

    def __init__(
        self,
        source=None,

    ):

        if source is None:
            raise InvalidModelSourceException(source)

        if isinstance(source, str):
            self.source = self.validate_model_path(source)
        else:
            self.model = source

        self.model = None
        self.input_shape = None
        self.device = None

        self.box_timings = list()
        self.inference_timings = list()
        self.loading_input_timings = list()

        self.sync_dict = {
            "motorbike": "motorcycle",
            "aeroplane": "airplane",
            "sofa": "couch",
            "pottedplant": "potted plant",
            "diningtable": "dining table",
            "tvmonitor": "tv"
        }

        self.load_model()

    @staticmethod
    def validate_model_path(source):
        """
        This method validates the existance of the model path.
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_core.py
            function: test_validate_model_path

        Parameters
        ----------

            source: str
                This is the path to the model.

        Returns
        -------
            source: str
                The validated path to the model.

        Raises
        ------

            FileNotFoundError
                This exception will be raised if the path to the
                model does not exist.
        """

        if not exists(source):
            raise FileNotFoundError(
                "Model file is expected to be at: {}".format(source))

        return source

    def load_model(self):
        """Abstract Method"""
        pass

    def run_single_instance(self, image, image_path):
        """Abstract Method"""
        pass

    def postprocessing(self, outputs):
        """Abstract Method"""
        pass

    def get_input_type(self):
        """Abstract Method"""
        pass

    def get_output_type(self):
        """Abstract Method"""
        pass

    def get_input_shape(self):
        """Abstract Method"""
        pass

    def summarize(self):
        """
        This method returns a summary of all the timings.
        (mean, avg, max) of (load, inference, box).
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/test_core.py
            function: test_summarize

        Parameters
        ----------
            None

        Returns
        -------
            timings in ms: dict

            .. code-block:: python

                {
                 'min_inference_time': minimum time to produce bounding boxes,
                 'max_inference_time': maximum time to produce bounding boxes,
                 'min_input_time': minimum time to load an image,
                 'max_input_time': maximum time to load an image,
                 'min_decoding_time': minimum time to process model
                                    predictions,
                 'max_decoding_time': maximum time to process model
                                    predictions,
                 'avg_decoding': average time to process model predictions,
                 'avg_input': average time to load an image,
                 'avg_inference': average time to produce bounding boxes,
                }

        Raises
        ------
            None
        """

        try:
            return {
                'min_inference_time': np.min(self.inference_timings),
                'max_inference_time': np.max(self.inference_timings),
                'min_input_time': np.min(self.loading_input_timings),
                'max_input_time': np.max(self.loading_input_timings),
                'min_decoding_time': np.min(self.box_timings),
                'max_decoding_time': np.max(self.box_timings),
                'avg_decoding': np.mean(self.box_timings),
                'avg_input': np.mean(self.loading_input_timings),
                'avg_inference': np.mean(self.inference_timings),
            }

        except ValueError:
            return None
