# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.writers import ConsoleWriter, TensorBoardWriter
from datetime import datetime
from os import path, makedirs


class Evaluator:
    """
    This class is an abstract class that provides a template for the
    validation evaluations (detection or segmentation).
    Unit-test for this class is defined under:
        file: test/deepview/validator/evaluators/test_core.py

    Parameters
    ----------

        runner: Runner object depending on the model.
            This object provides methods to run the detection model.

        dataset: Dataset object depending on the dataset.
            This object provides methods to read and parse the dataset.

        datacollection: DataCollection object depending on detection
        or segmentation. This object stores the number of true positives,
        false positives, and false negatives per label
        that allows the computation of metrics.

        visualize: str
            This is the path to store the images with visualizations. Can
            optionally be None to exclude.

        tensorboard: str
            This is the path to store the tensorboard tfevents file. Can
            optionally be None to exclude.

        json_out: str
            This is the path to the store the JSON file validation
            summary.

        display: int
            This is the number of images to save. By default it is -1
            specifying all the images.

        parameters: dict
            The model parameters:

            .. code-block:: python

                {
                    "validation-iou": args.validation_iou,
                    "detection-iou": args.detection_iou,
                    "validation-threshold": args.validation_threshold,
                    "detection-threshold": args.detection_threshold,
                    "nms": args.nms_type,
                    "normalization": args.norm,
                    "maximum_detections": args.max_detection,
                    "warmup": args.warmup
                }

    Raises
    ------
        None

    """

    def __init__(
        self,
        runner,
        datacollection,
        dataset=None,
        visualize=None,
        tensorboard=None,
        json_out=None,
        display=-1,
        parameters=None
    ):

        self.runner = runner
        self.datacollection = datacollection
        self.dataset = dataset
        self.visualize = visualize
        self.tensorboard = tensorboard
        self.display = display
        self.parameters = parameters
        self.counter = 0

        # Time of test => Used to name the test results folder.
        today = datetime.now().strftime('%Y-%m-%d--%H:%M:%S').replace(":", "_")
        self.json_out = json_out
        if json_out:
            if path.splitext(json_out)[1].lower() == ".json":
                if not path.exists(path.dirname(json_out)):
                    makedirs(path.dirname(json_out))
                self.json_out = json_out
            elif path.splitext(json_out)[1].lower() == "":
                if not path.exists(path.normpath(json_out)):
                    makedirs(path.normpath(json_out))
                self.json_out = path.join(json_out, "results.json")
            else:
                raise ValueError("--json_out parameter can only accept " + 
                                 "json files, but received {}".format(json_out)
                                )

        if visualize:
            self.save_path = path.join(
                visualize, f"{path.basename(path.normpath(self.runner.source))}_{today}"
            )
            if not path.exists(self.save_path):
                makedirs(self.save_path)
            self.consolewriter = ConsoleWriter()
            self.tensorboardwriter = None

        elif tensorboard:
            self.save_path = path.join(
                tensorboard, f"{path.basename(path.normpath(self.runner.source))}_{today}"
            )
            if not path.exists(self.save_path):
                makedirs(self.save_path)
            self.tensorboardwriter = TensorBoardWriter(self.save_path)

        else:
            self.consolewriter = ConsoleWriter()
            self.tensorboardwriter = None

    def instance_collector(self):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method")

    def single_evaluation(self, instance, epoch, add_image):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method")

    def group_evaluation(self):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method")

    def conclude(self):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method")
