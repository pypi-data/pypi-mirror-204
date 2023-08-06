# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.metrics.segmentationutils import create_mask_image, \
    create_mask_class, create_mask_background, \
    classify_mask, create_mask_classes
from deepview.validator.visualize import Drawer, SegmentationDrawer
from deepview.validator.metrics import SegmentationDataCollection, \
    SegmentationMetrics
from deepview.validator.evaluators.core import Evaluator
from copy import deepcopy
from os import path
import numpy as np


class SegmentationEval(Evaluator):
    """
    This class provides methods to perform segmentation validation.
    The common process of running validation:

        1) Grab the ground truth and the model prediction instances per image.
        2) Create masks for both ground truth and model prediction.
        3) Classify the mask pixels as either true positives,
           or false positives/negatives.
        4) Overlay the ground truth and predictions masks on the image.
        5) Calculate the metrics.

    Unit-test for this class is defined under:
        file: test/deepview/validator/evaluators/test_segmentationevaluator.py

    Parameters
    ----------

        runner: Runner object depending on the model.
            This object provides methods to run the detection model.

        dataset: Dataset object depending on the dataset.
            This object provides methods to read and parse the dataset.

        datacollection: DetectionDataCollection
            This object stores the number of true positives, false positives,
            and false negatives per label that
            allows the computation of metrics.

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

            This does not apply to segmentation, therefore it is set as None.

    Raises
    -------
        ValueError
            This will raise the exception if the provided parameters
            in certain methods does not conform to the specified data type
            or the parameters are out of bounds. i.e. The thresholds provided
            are greater than 1 or less than 0.
    """

    def __init__(
        self,
        runner,
        dataset=None,
        visualize=None,
        tensorboard=None,
        json_out=None,
        display=-1,
        parameters=None
    ):
        super(SegmentationEval, self).__init__(
            runner=runner,
            dataset=dataset,
            datacollection=SegmentationDataCollection(),
            visualize=visualize,
            tensorboard=tensorboard,
            json_out=json_out,
            display=display,
            parameters=parameters
        )

    def __call__(self, val_messenger):
        """
        This method allows tensorboardformatter object in trainer
        to operate here and resets the metrics after each epoch.
        Default validation has no use of this method.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_segmentationevaluator.py
            function: test__call__.py

        Parameters
        ----------

            val_messenger: TrainingTensorBoardWriter
                This object is internal for modelpack that was instantiated
                specifically for training a model.

        Returns
        -------
            None

        Raises
        ------
            None
        """

        self.tensorboardwriter = val_messenger
        self.datacollection = SegmentationDataCollection()

    def instance_collector(self):
        """Collects instances from the ground truth
        and predictions of segmentation models.

        Instances are data containers that show information regarding the
        ground truth (image, height, width, boxes, labels, image path, gt_mask)
        model predictions (dt_mask, dt_labels)
        for each image.


        This method collects the instances from the ground truth
        and the model segmentations.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_segmentationevaluator.py
            function: test_instance_collector

        Parameters
        ----------
            None

        Returns
        -------

            instances: dict
                This yields one image instance from the ground
                truth and the model predictions.

                .. code-block:: python

                    {
                        'gt_instance': {
                            'image': image numpy array,
                            'height': height,
                            'width': width,
                            'gt_mask': ground truth mask of the image,
                            'labels': list of labels,
                            'image_path': image_path
                        },
                        'dt_instance': {
                            'dt_mask': model mask of the image,
                            'labels': list of prediction labels,
                        }
                    }

        Raises
        ------
            None
        """

        height, width = self.runner.get_input_shape()
        for gt_instance in self.dataset.read_all_samples():

            # This is for gray images that can't be processed.
            if gt_instance is None:
                continue

            gt_mask = create_mask_image(height, width, gt_instance)
            gt_instance['gt_mask'] = gt_mask
            image = gt_instance.get("image")
            dt_mask = self.runner.run_single_instance(image)
            dt_labels = list(np.unique(dt_mask))
            dt_instance = {
                'dt_mask': dt_mask,
                'labels': dt_labels
            }

            yield {
                'dt_instance': dt_instance,
                'gt_instance': gt_instance
            }

    def single_evaluation(self, instance, epoch=0, add_image=True):
        """
        This method runs validation on a single instance.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_segmentationevaluator.py
            function: test_single_evaluation

        Parameters
        ----------

            instance: dict
                The ground truth and the predictions instances:

                .. code-block:: python

                    instances = {
                            'gt_instance': {
                                'image': image numpy array,
                                'height': height,
                                'width': width,
                                'gt_mask': ground truth mask of the image,
                                'labels': list of labels,
                                'image_path': image_path
                            },
                            'dt_instance': {
                                'dt_mask': model mask of the image,
                                'labels': list of prediction labels,
                            }
                        }

            epoch: int
                This is the training epoch number. This
                parameter is internal for modelpack usage.
                Default validation has no use of this parameter.

            add_image: bool
                If set to True, this will draw on the image
                with bounding boxes.

        Returns
        -------
            truth values: int
                total_tp, total_fn, total_class_fp, total_local_fp

        Raises
        ------
            None
        """

        height, width = self.dataset.shape[0], self.dataset.shape[1]
        self.drawer = SegmentationDrawer()
        gt_labels = instance.get('gt_instance').get('labels')
        dt_labels = instance.get('dt_instance').get('labels')
        class_labels = np.unique(gt_labels + dt_labels)

        self.datacollection.capture_class(class_labels, self.dataset.labels)

        gt_mask = instance.get('gt_instance').get('gt_mask')
        dt_mask = instance.get('dt_instance').get('dt_mask')
        cu_tp_mask, cu_fp_mask, cu_fn_mask = None, None, None

        for cl in class_labels:

            gt_class_mask = create_mask_class(gt_mask, cl)
            dt_class_mask = create_mask_class(dt_mask, cl)
            # Evaluate background class
            if cl == 0:
                gt_class_mask = create_mask_background(gt_mask)
                dt_class_mask = create_mask_background(dt_mask)

            tp, fp, fn, tp_mask, fp_mask, fn_mask = classify_mask(
                height, gt_class_mask, dt_class_mask, dt_mask)

            cu_tp_mask = create_mask_classes(
                tp_mask, cl, cu_tp_mask)
            cu_fp_mask = create_mask_classes(
                fp_mask, cl, cu_fp_mask)
            cu_fn_mask = create_mask_classes(
                fn_mask, cl, cu_fn_mask)

            datalabel = self.datacollection.get_label_data(self.dataset.labels[cl])
            datalabel.add_tp(tp)
            datalabel.add_fp(fp)
            datalabel.add_fn(fn)
            datalabel.add_gt(tp + fn)

        # Execute this code for two pane image results
        # dst = mask2maskimage(height, width, instances)

        # Execute this code for four pane image results
        if add_image:
            dst = self.drawer.mask2mask4panes(
                height, width, instance, cu_tp_mask, cu_fp_mask, cu_fn_mask)

            if self.visualize:
                n_path = path.join(self.save_path, path.basename(
                    instance.get('gt_instance').get('image_path')))
                dst.save(n_path)
            elif self.tensorboardwriter:
                self.tensorboardwriter(dst, instance.get(
                    'gt_instance').get('image_path'), step=epoch)

        return self.datacollection.sum_outcomes()

    def group_evaluation(self):
        """
        This method performs the semantic segmentation
        evaluation of all images.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_segmentationevaluator.py
            function: test_group_evaluation

        Parameters
        ----------
            None

        Returns
        -------
            truth values: int
                total_tp, total_fn, total_fp

        Raises
        ------
            None
        """

        self.counter = 0
        height, width = self.dataset.shape[0], self.dataset.shape[1]
        self.drawer = SegmentationDrawer()

        for instances in self.instance_collector():

            gt_labels = instances.get('gt_instance').get('labels')
            dt_labels = instances.get('dt_instance').get('labels')
            class_labels = np.unique(gt_labels + dt_labels)

            self.datacollection.capture_class(
                class_labels, self.dataset.labels)

            gt_mask = instances.get('gt_instance').get('gt_mask')
            dt_mask = instances.get('dt_instance').get('dt_mask')
            cu_tp_mask, cu_fp_mask, cu_fn_mask = None, None, None

            for cl in class_labels:

                gt_class_mask = create_mask_class(gt_mask, cl)
                dt_class_mask = create_mask_class(dt_mask, cl)
                # Evaluate background class
                if cl == 0:
                    gt_class_mask = create_mask_background(gt_mask)
                    dt_class_mask = create_mask_background(dt_mask)

                tp, fp, fn, tp_mask, fp_mask, fn_mask = classify_mask(
                    height, gt_class_mask, dt_class_mask, dt_mask)

                cu_tp_mask = create_mask_classes(
                    tp_mask, cl, cu_tp_mask)
                cu_fp_mask = create_mask_classes(
                    fp_mask, cl, cu_fp_mask)
                cu_fn_mask = create_mask_classes(
                    fn_mask, cl, cu_fn_mask)

                datalabel = self.datacollection.get_label_data(
                    self.dataset.labels[cl])
                datalabel.add_tp(tp)
                datalabel.add_fp(fp)
                datalabel.add_fn(fn)
                datalabel.add_gt(tp + fn)

            # Execute this code for two pane image results
            #dst = self.drawer.mask2maskimage(height, width, instances)

            # Execute this code for four pane image results
            dst = self.drawer.mask2mask4panes(
                height, width, instances, cu_tp_mask, cu_fp_mask, cu_fn_mask)

            if self.display >= 0:
                if self.counter < self.display:
                    self.counter += 1
                else:
                    continue

            if self.visualize:
                n_path = path.join(self.save_path, path.basename(
                    instances.get('gt_instance').get('image_path')))
                dst.save(n_path)
            elif self.tensorboardwriter:
                self.tensorboardwriter(dst, instances.get(
                    'gt_instance').get('image_path'))
            else:
                continue

        return self.datacollection.sum_outcomes()

    def conclude(self, truth_values, epoch=0):
        """
        This method computes the final metrics, draws the class histogram, and
        saves the results either to tensorboard or to the local machine.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_segmentationevaluator.py
            function: test_conclude

        Parameters
        ----------

            truth values: int
                total_tp, total_fn, total_fp

            epoch: int
                This is the training epoch number. This
                parameter is internal for modelpack usage.
                Default validation has no use of this parameter.

        Returns
        -------
            summary: dict

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

        Raises
        ------
            None
        """

        metrics = SegmentationMetrics(
            segmentationdatacollection=self.datacollection)
        timings = self.runner.summarize()
        self.parameters["engine"] = self.runner.device

        try:
            model_name = path.basename(self.runner.source)
        except AttributeError:
            model_name = "Training Model"

        try:
            dataset_name = path.basename(path.normpath(self.dataset.source))
        except AttributeError:
            dataset_name = "Validation Dataset"

        mean_metrics, class_histogram_data = metrics.compute_segmentation_metrics()
        overall_metrics = metrics.compute_overall_metrics(*truth_values)

        summary = {
            "model": model_name,
            "engine": self.runner.device,
            "dataset": dataset_name,
            "numgt": int(self.datacollection.total_gt),
            "Total TP": truth_values[0],
            "Total FN": truth_values[1],
            "Total FP": truth_values[2],
            "OP": overall_metrics[0],
            "OR": overall_metrics[1],
            "OA": overall_metrics[2],
            "mAP": mean_metrics[0],
            "mAR": mean_metrics[1],
            "mACC": mean_metrics[2],
            "timings": timings
        }

        if self.visualize or self.tensorboardwriter:
            fig_class_metrics = Drawer.plot_classification(
                class_histogram_data, model=model_name)

        if self.visualize:
            fig_class_metrics.savefig(
                f'{self.save_path}/class_scores.png',
                bbox_inches="tight")
        elif self.tensorboardwriter:
            nimage_class = Drawer.figure2numpy(fig_class_metrics)
            self.tensorboardwriter(
                nimage_class,
                f"{summary.get('model')}_scores.png",
                step=epoch)
            
        if self.json_out:
            import json
            summary["class_histogram_data"] = class_histogram_data
            
            with open(self.json_out, 'w') as fp:
                json.dump(summary, fp)


        if self.tensorboardwriter:
            self.tensorboardwriter.publish_metrics(message=deepcopy(
                summary), step=epoch, validation_type="segmentation")
        else:
            header, format_summary, format_timings = self.consolewriter(
                message=deepcopy(summary), validation_type="segmentation")

            if self.visualize:
                with open(self.save_path + '/metrics.txt', 'w') as fp:
                    fp.write(header + '\n')
                    fp.write(format_summary + '\n')
                    if timings is not None:
                        fp.write(format_timings)
                fp.close()

        return summary
