# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.metrics import DetectionMetrics, DetectionDataCollection
from deepview.validator.metrics.detectionutils import match_dt_gt
from deepview.validator.visualize import Drawer, DetectionDrawer
from deepview.validator.evaluators.core import Evaluator
from copy import deepcopy
from os import path
import numpy as np


class DetectionEval(Evaluator):
    """
    This class provides methods to perform detection validation.
    The common process of running validation:

        1) Grab the ground truth and the model prediction instances per image.
        2) Match the  model predictions to the ground truth.
        3) Categorize the model predictions as either true positives,
           or false positives/negatives.
        4) Draw the bounding boxes.
        5) Calculate the metrics.

    Unit-test for this class is defined under:
        file: test/deepview/validator/evaluators/test_detectionevaluator.py

    Parameters
    ----------

        runner: Runner object depending on the model.
            This object provides methods to run the detection model.

        dataset: Dataset object depending on the dataset.
            This object provides methods to read and parse the dataset.

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
        super(DetectionEval, self).__init__(
            runner=runner,
            dataset=dataset,
            datacollection=DetectionDataCollection(),
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
            file: test/deepview/validator/evaluators/test_detectionevaluator.py
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
        self.datacollection = DetectionDataCollection()

    def instance_collector(self):
        """
        This method collects the instances from the ground truth
        and the model predictions.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_detectionevaluator.py
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
                            'boxes': list bounding boxes,
                            'labels': list of labels,
                            'image_path': image_path
                        },
                        'dt_instance': {
                            'boxes': list of prediction bounding boxes,
                            'labels': list of prediction labels,
                            'scores': list of confidence scores
                        }
                    }

        Raises
        ------
            ValueError
                This method will raise an exception if provided image path
                does not exist and the provided image array
                is not a numpy.ndarray.
        """

        for gt_instance in self.dataset.read_all_samples():
            # This is for gray images that can't be processed.
            if gt_instance is None:
                continue

            if path.exists(gt_instance.get('image_path')):
                image = gt_instance.get('image_path')
            elif isinstance(gt_instance.get('image'), np.ndarray):
                image = gt_instance.get('image')
            else:
                raise ValueError(
                    "The provided image_path does not exist at: " +
                    gt_instance.get('image_path') +
                    "The provided image array is not a numpy.ndarray: " +
                    type(gt_instance.get('image'))
                )

            dt_boxes, dt_classes, dt_scores = \
                self.runner.run_single_instance(image)

            # Convert any synonym of the predicted label into the standard coco
            # label.
            if "clock" in self.dataset.labels:
                dt_classes_modified = list()
                for label in dt_classes:
                    for key in self.runner.sync_dict.keys():
                        if label == key:
                            label = self.runner.sync_dict[key]
                    dt_classes_modified.append(label)
                dt_classes = dt_classes_modified

            dt_instance = {
                'boxes': dt_boxes,
                'labels': dt_classes,
                'scores': dt_scores
            }

            yield {
                'gt_instance': gt_instance,
                'dt_instance': dt_instance
            }

    def single_evaluation(self, instance, epoch=0, add_image=True):
        """
        This method runs validation on a single instance.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_detectionevaluator.py
            function: test_single_evaluation

        Parameters
        ----------

            instance: dict
                The ground truth and the predictions instances:

                .. code-block:: python

                        instance = {
                            gt_instance = {
                                'image':image,
                                'height': height,
                                'width': width,
                                'boxes': [],
                                'labels': [],
                                'image_path': image_path
                            },
                            dt_instance = {
                                'boxes': dt_boxes,
                                'labels': dt_classes,
                                'scores': dt_scores
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
            ValueError
                This will raise the exception if the provided parameters
                in certain methods does not conform to the specified data
                type or the parameters are out of bounds. i.e.
                The thresholds provided
                are greater than 1 or less than 0.
        """

        iou_threshold = self.parameters.get("validation-iou")
        score_threshold = self.parameters.get("validation-threshold")
        self.drawer = DetectionDrawer()

        gt_boxes = instance.get('gt_instance').get('boxes')
        dt_boxes = instance.get('dt_instance').get('boxes')
        gt_labels = instance.get('gt_instance').get('labels')
        dt_labels = instance.get('dt_instance').get('labels')
        scores = instance.get('dt_instance').get('scores')

        self.datacollection.capture_class(dt_labels)
        self.datacollection.capture_class(gt_labels)
        stats = match_dt_gt(gt_boxes=gt_boxes, dt_boxes=dt_boxes)
        self.datacollection.categorize(
            *stats,
            gt_labels=gt_labels,
            dt_labels=dt_labels,
            scores=scores)

        if add_image:
            if self.visualize or self.tensorboardwriter:
                original_image = instance.get('gt_instance').get('image')
                image = self.drawer.draw_with_pillow(
                    iou_threshold, score_threshold,
                    original_image, instance, *stats
                )

            if self.visualize:
                image.save(path.join(self.save_path, path.basename(
                    instance.get('gt_instance').get('image_path'))))
            elif self.tensorboardwriter:
                nimage = np.asarray(image)
                self.tensorboardwriter(nimage, instance.get(
                    'gt_instance').get('image_path'), step=epoch)

        return self.datacollection.sum_outcomes(iou_threshold, score_threshold)

    def group_evaluation(self):
        """
        This method performs the bounding box evaluation on all images.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_detectionevaluator.py
            function: test_group_evaluation

        Parameters
        ----------
            None

        Returns
        -------
            truth values: int
                total_tp, total_fn, total_class_fp, total_local_fp

        Raises
        ------
            ValueError
                This will raise the exception if the provided parameters
                in certain methods does not conform to the specified data type
                or the parameters are out of bounds.
                i.e. The thresholds provided
                are greater than 1 or less than 0.
        """

        iou_threshold = self.parameters.get("validation-iou")
        score_threshold = self.parameters.get("validation-threshold")
        self.counter = 0
        self.drawer = DetectionDrawer()

        for instances in self.instance_collector():

            gt_boxes = instances.get('gt_instance').get('boxes')
            dt_boxes = instances.get('dt_instance').get('boxes')
            gt_labels = instances.get('gt_instance').get('labels')
            dt_labels = instances.get('dt_instance').get('labels')
            scores = instances.get('dt_instance').get('scores')

            self.datacollection.capture_class(dt_labels)
            self.datacollection.capture_class(gt_labels)
            stats = match_dt_gt(gt_boxes=gt_boxes, dt_boxes=dt_boxes)

            self.datacollection.categorize(
                *stats,
                gt_labels=gt_labels,
                dt_labels=dt_labels,
                scores=scores)

            if self.visualize or self.tensorboardwriter:
                original_image = instances.get('gt_instance').get('image')
                image = self.drawer.draw_with_pillow(
                    iou_threshold, score_threshold,
                    original_image, instances, *stats
                )

                if self.display >= 0:
                    if self.counter < self.display:
                        self.counter += 1
                    else:
                        continue

            if self.visualize:
                image.save(path.join(self.save_path, path.basename(
                    instances.get('gt_instance').get('image_path'))))
            elif self.tensorboardwriter:
                nimage = np.asarray(image)
                self.tensorboardwriter(nimage, instances.get(
                    'gt_instance').get('image_path'))
            else:
                continue

        return self.datacollection.sum_outcomes(iou_threshold, score_threshold)

    def conclude(self, truth_values, epoch=0):
        """
        This method computes the final metrics, draws the final plots, and
        saves the results either to tensorboard or to the local machine.
        Unit-test for this method is defined under:
            file: test/deepview/validator/evaluators/test_detectionevaluator.py
            function: test_conclude

        Parameters
        ----------

            truth values: int
                total_tp, total_fn, total_class_fp, total_local_fp

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
                    "LocFPErr": {'0.5': localization false positive
                                        ratio at 0.5 IoU threshold,
                                '0.75': localization false positive
                                        ratio at 0.75 IoU threshold,
                                '0.5:0.95': localization false positive
                                        ratio across 0.5-0.95 IoU thresholds
                                },
                    "ClassFPErr": { '0.5': classification false positive
                                        ratio at 0.5 IoU threshold,
                                    '0.75': classification false positive
                                        ratio at 0.75 IoU threshold,
                                    '0.5:0.95': classification false positive
                                        ratio across 0.5-0.95 IoU thresholds
                                },
                    "timings": timings
                            (input, inference, decode at min/max/avg)
                }

        Raises
        ------
            None
        """

        iou_threshold = self.parameters.get("validation-iou")
        score_threshold = self.parameters.get("validation-threshold")

        metrics = DetectionMetrics(detectiondatacollection=self.datacollection)
        timings = self.runner.summarize()
        self.parameters["engine"] = self.runner.device

        try:
            model_name = path.basename(path.normpath(self.runner.source))
        except AttributeError:
            model_name = "Training Model"

        try:
            dataset_name = path.basename(path.normpath(self.dataset.source))
        except AttributeError:
            dataset_name = "Validation Dataset"

        overall_metrics = metrics.compute_overall_metrics(*truth_values)
        mean_metrics, class_histogram_data = metrics.compute_detection_metrics(
            score_threshold)
        false_positive_ratios = metrics.get_fp_error(score_threshold)
        precision_recall_data = metrics.get_pr_data(
            score_threshold=score_threshold, iou_threshold=iou_threshold)

        summary = {
            "model": model_name,
            "dataset": dataset_name,
            "numgt": self.datacollection.total_gt,
            "Total TP": truth_values[0],
            "Total FN": truth_values[1],
            "Total Class FP": truth_values[2],
            "Total Loc FP": truth_values[3],
            "OP": overall_metrics[0],
            "mAP": {'0.5': mean_metrics[0][0],
                    '0.75': mean_metrics[0][1],
                    '0.5:0.95': mean_metrics[0][2]
                    },
            "OR": overall_metrics[1],
            "mAR": {'0.5': mean_metrics[1][0],
                    '0.75': mean_metrics[1][1],
                    '0.5:0.95': mean_metrics[1][2]
                    },
            "OA": overall_metrics[2],
            "mACC": {'0.5': mean_metrics[2][0],
                     '0.75': mean_metrics[2][1],
                     '0.5:0.95': mean_metrics[2][2]
                     },
            "LocFPErr": {'0.5': false_positive_ratios[0],
                         '0.75': false_positive_ratios[2],
                         '0.5:0.95': false_positive_ratios[4]
                         },
            "ClassFPErr": {'0.5': false_positive_ratios[1],
                           '0.75': false_positive_ratios[3],
                           '0.5:0.95': false_positive_ratios[5]
                           },
            "timings": timings
        }

        if self.visualize or self.tensorboardwriter:
            fig_class_metrics = Drawer.plot_classification(
                class_histogram_data, model=model_name)
            fig_prec_rec_curve = Drawer.plot_pr_curve(
                precision_recall_data.get("recall"),
                precision_recall_data.get("precision"),
                precision_recall_data.get("average-precision"),
                names=precision_recall_data.get("names"),
                model=model_name
            )
            fig_f1_curve = Drawer.plot_mc_curve(
                precision_recall_data.get("x-data"),
                precision_recall_data.get("f1"),
                names=precision_recall_data.get("names"),
                ylabel='F1',
                model=model_name
            )
            fig_prec_confidence_curve = Drawer.plot_mc_curve(
                precision_recall_data.get("x-data"),
                precision_recall_data.get("precision-confidence"),
                names=precision_recall_data.get("names"),
                ylabel='Precision',
                model=model_name
            )
            fig_rec_confidence_curve = Drawer.plot_mc_curve(
                precision_recall_data.get("x-data"),
                precision_recall_data.get("recall-confidence"),
                names=precision_recall_data.get("names"),
                ylabel='Recall',
                model=model_name
            )

        if self.json_out:
            import json
            summary["class_histogram_data"] = class_histogram_data
            reformat_pr_data = dict()
            for key, value in precision_recall_data.items():
                if isinstance(value, (list, np.ndarray)):
                    tmp_value = list()
                    for x in value:
                        if isinstance(x, np.ndarray):
                            tmp_value.append(x.tolist())
                        else:
                            tmp_value.append(x)

                reformat_pr_data[key] = tmp_value
            summary["precision_recall_data"] = reformat_pr_data

            with open(self.json_out, 'w', encoding='utf-8') as fp:
                json.dump(summary, fp, ensure_ascii=False, indent=4)

        if self.visualize:
            fig_class_metrics.savefig(
                f'{self.save_path}/class_scores.png',
                bbox_inches="tight")
            fig_prec_rec_curve.savefig(
                f'{self.save_path}/prec_rec_curve.png',
                bbox_inches='tight')
            fig_f1_curve.savefig(
                f'{self.save_path}/f1_curve.png',
                bbox_inches='tight')
            fig_prec_confidence_curve.savefig(
                f'{self.save_path}/precision_confidence_curve.png',
                bbox_inches='tight')
            fig_rec_confidence_curve.savefig(
                f'{self.save_path}/rec_confidence_curve.png',
                bbox_inches='tight')

        elif self.tensorboardwriter:
            nimage_class = Drawer.figure2numpy(fig_class_metrics)
            nimage_precision_recall = Drawer.figure2numpy(fig_prec_rec_curve)
            nimage_precision_confidence = Drawer.figure2numpy(
                fig_prec_confidence_curve)
            nimage_recall_confidence = Drawer.figure2numpy(
                fig_rec_confidence_curve)
            nimage_f1_curve = Drawer.figure2numpy(fig_f1_curve)

            self.tensorboardwriter(
                nimage_class,
                f"{summary.get('model')}_scores.png",
                step=epoch)
            self.tensorboardwriter(
                nimage_precision_recall,
                f"{summary.get('model')}_precision_recall.png",
                step=epoch)
            self.tensorboardwriter(
                nimage_precision_confidence,
                f"{summary.get('model')}_precision_confidence.png",
                step=epoch)
            self.tensorboardwriter(
                nimage_recall_confidence,
                f"{summary.get('model')}_recall_confidence.png",
                step=epoch)
            self.tensorboardwriter(
                nimage_f1_curve,
                f"{summary.get('model')}_f1.png",
                step=epoch)

        if self.tensorboardwriter:
            self.tensorboardwriter.publish_metrics(
                message=deepcopy(summary),
                parameters=self.parameters,
                step=epoch,
                validation_type="detection")
        else:
            header, format_summary, format_timings = self.consolewriter(
                message=deepcopy(summary),
                parameters=self.parameters,
                validation_type="detection"
            )

            if self.visualize:
                with open(self.save_path + '/metrics.txt', 'w') as fp:
                    fp.write(header + '\n')
                    fp.write(format_summary + '\n')
                    if timings is not None:
                        fp.write(format_timings)
                fp.close()
        return summary
