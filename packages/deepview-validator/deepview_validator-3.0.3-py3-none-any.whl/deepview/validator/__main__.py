# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.runners import DeepViewRTRunner, KerasRunner, \
    OfflineRunner, TensorRTRunner
from deepview.validator.runners.modelclient import SegmentationDeepLab, \
    SegmentationModelPack
from deepview.validator.runners.modelclient import BoxesModelPack, BoxesYolo
from deepview.validator.exceptions import UnsupportedModelExtensionException
from deepview.validator.exceptions import UnsupportedValidationTypeException
from deepview.validator.exceptions import UnsupportedApplicationException
from deepview.validator.evaluators import DetectionEval, SegmentationEval
from deepview.validator.exceptions import UnsupportedModelTypeException
from deepview.validator.datasets.utils import instantiate_dataset
from deepview.validator.datasets import Dataset
from deepview.validator.writers import Writer
from deepview.validator import version
from os import path
import argparse


def main():
    parser = argparse.ArgumentParser(
        description=('Standalone DeepView Validator.'),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-V', '--version', action='version', version=version())
    parser.add_argument('--validate',
                        help=("Type of validation to perform: "
                              "'detection' or 'segmentation'."),
                        choices=['detection', 'segmentation'],
                        default='detection',
                        type=str
                        )
    parser.add_argument('--application',
                        help=("Type of application to use: "
                              "'vaal' or 'modelclient'."),
                        choices=['vaal', 'modelclient'],
                        default='vaal',
                        type=str
                        )
    parser.add_argument('-d', '--dataset',
                        help=("absolute or relative path"
                              "to the dataset folder or yaml file."),
                        required=True,
                        type=str
                        )
    parser.add_argument('--labels_file',
                        help='absolute or relative path to the labels file.',
                        type=str
                        )
    parser.add_argument('--annotation_format',
                        help=("Specify the format of the annotations: "
                              "'yolo', 'coco', 'pascalvoc'"),
                        choices=['yolo', 'coco', 'pascalvoc'],
                        default='yolo',
                        type=str
                        )
    parser.add_argument('--offline_annotation_format',
                        help=("Specify the format of "
                              "the Offline Runner annotations: "
                              "'yolo', 'coco', 'pascalvoc'"),
                        choices=['yolo', 'coco', 'pascalvoc'],
                        default='yolo',
                        type=str
                        )
    parser.add_argument('--absolute_annotations',
                        help=("This specifies that the annotations "
                              "are not normalized to the image dimensions."),
                        action='store_true'
                        )
    parser.add_argument('--show_missing_annotations',
                        help=("This shows the image names without "
                              "annotations on the terminal"),
                        action='store_true'
                        )
    parser.add_argument('-e', '--engine',
                        help=("Compute engine for inference."
                              "'npu', 'gpu', 'cpu'"),
                        choices=['cpu', 'npu', 'gpu'],
                        default='npu',
                        type=str
                        )
    parser.add_argument('--detection_threshold',
                        help='NMS threshold for valid scores.',
                        default=0.01,
                        type=float
                        )
    parser.add_argument('--validation_threshold',
                        help=("Validation score threshold "
                              "to filter predictions."),
                        default=0.5,
                        type=float
                        )
    parser.add_argument('--detection_iou',
                        help='IoU threshold for NMS.',
                        default=0.45,
                        type=float
                        )
    parser.add_argument('--validation_iou',
                        help=("Validation IoU threshold "
                              "to consider true positives."),
                        default=0.5,
                        type=float
                        )
    parser.add_argument('-l', '--label_offset',
                        help='Label offset when matching index to label name.',
                        default=0,
                        type=int
                        )
    parser.add_argument('-b', '--box_format',
                        help=("box format to reorient the prediction "
                              "coordinates: 'xywh', 'xyxy', 'yxyx', etc).\n"),
                        choices=['xywh', 'xyxy', 'yxyx'],
                        default='xyxy',
                        type=str
                        )
    parser.add_argument(
        '-n',
        '--norm',
        help=(
            'Normalization method applied to input images.'
            '- raw (default, no processing)\n'
            '- unsigned (0...1)\n'
            '- signed (-1...1)\n'
            '- whitening (per-image standardization/whitening)\n'
            '- imagenet (standardization using imagenet)\n'),
        choices=[
            'raw',
            'unsigned',
            'signed',
            'whitening',
            'imagenet'],
        default='raw',
        type=str)
    parser.add_argument('-m', '--max_detection',
                        help='Number of maximum predictions (bounding boxes).',
                        default=100,
                        type=int
                        )
    parser.add_argument('-w', '--warmup',
                        help='The warmup iterations before processing images.',
                        default=0,
                        type=int
                        )
    parser.add_argument('-s', '--nms_type',
                        help=("NMS type to perform validation: "
                              "'standard', 'fast', 'matrix'."),
                        choices=['standard', 'fast', 'matrix'],
                        type=str
                        )
    parser.add_argument(
        '--decoder',
        help=(
            "If the model does not have embedded decoder, "
            "then apply this parameter in the command line."),
        action='store_true')
    parser.add_argument('--model_box_type',
                        help="Type of the box model: 'modelpack', 'yolo'.",
                        choices=['modelpack', 'yolo'],
                        default='modelpack',
                        type=str
                        )
    parser.add_argument('--model_segmentation_type',
                        help=("Type of the Segmentation model: "
                              "'modelpack', 'deeplab'"),
                        choices=['modelpack', 'deeplab'],
                        default='modelpack',
                        type=str
                        )
    parser.add_argument('--target',
                        help=('Provide the modelrunner target.\n'
                              'Ex. 10.10.40.205:10817'),
                        default=None,
                        type=str
                        )
    parser.add_argument('--display',
                        help=("How many images to display into tensorboard. "
                              "By default it is (-1) all the images, "
                              "but an integer can be passed."),
                        default=-1,
                        type=int
                        )
    parser.add_argument(
        '--visualize',
        help=(
            "Path to store visualizations "
            "(images with bounding boxes or segmentation masks)."),
        default=None,
        type=str
    )
    parser.add_argument('--tensorboard',
                        help=("Path to store *.tfevents files "
                              "needed for tensorboard."),
                        default=None,
                        type=str
                        )
    parser.add_argument(
        '--json_out',
        help=("Path to save the validation summary as a json file on disk."),
        default=None,
        type=str
    )
    parser.add_argument(
        'model',
        help=(
            "Model path to the DeepViewRT (rtm), "
            "Keras (H5), TFlite, TensorRT (trt) model to load."),
        metavar='model.rtm',
        type=str
    )
    args = parser.parse_args()

    parameters = {
        "validation-iou": args.validation_iou,
        "detection-iou": args.detection_iou,
        "validation-threshold": args.validation_threshold,
        "detection-threshold": args.detection_threshold,
        "nms": args.nms_type,
        "normalization": args.norm,
        "maximum_detections": args.max_detection,
        "warmup": args.warmup,
        "label offset": args.label_offset
    }

    base_dataset = Dataset()
    info_dataset = base_dataset.get_detection_dataset(
        source=args.dataset,
        labels_path=args.labels_file
        )
    dataset = instantiate_dataset(
        info_dataset=info_dataset,
        source=args.dataset,
        gformat=args.annotation_format,
        absolute=args.absolute_annotations,
        validate_type=args.validate,
        show_missing_annotations=args.show_missing_annotations
    )

    # DEEPVIEWRT EVALUATION
    if path.splitext(args.model)[1].lower() == ".rtm":

        if args.validate.lower() == "detection":

            if args.application.lower() == "vaal":

                runner = DeepViewRTRunner(
                    model_path=args.model,
                    labels=dataset.labels,
                    engine=args.engine,
                    detection_score_threshold=args.detection_threshold,
                    detection_iou_threshold=args.detection_iou,
                    label_offset=args.label_offset,
                    box_format=args.box_format,
                    norm=args.norm,
                    max_detections=args.max_detection,
                    warmup=args.warmup,
                    nms_type=args.nms_type
                )

            elif args.application.lower() == "modelclient":

                if args.model_box_type.lower() == 'modelpack':

                    runner = BoxesModelPack(
                        model_path=args.model,
                        target=f"http://{args.target}/v1",
                        labels=dataset.labels,
                        detection_iou_threshold=args.detection_iou,
                        detection_score_threshold=args.detection_threshold,
                        norm=args.norm,
                        decoder=args.decoder,
                        label_offset=args.label_offset
                    )

                elif args.model_box_type.lower() == 'yolo':

                    runner = BoxesYolo(
                        model_path=args.model,
                        target=f"http://{args.target}/v1",
                        labels=dataset.labels,
                        detection_iou_threshold=args.detection_iou,
                        detection_score_threshold=args.detection_threshold,
                        norm=args.norm,
                        decoder=args.decoder,
                        label_offset=args.label_offset
                    )

                else:
                    raise UnsupportedModelTypeException(args.model_box_type)

            else:
                raise UnsupportedApplicationException(args.application)

        elif args.validate.lower() == "segmentation":

            if args.model_segmentation_type.lower() == 'modelpack':

                runner = SegmentationModelPack(
                    model_path=args.model,
                    target=f'http://{args.target}/v1'
                )
                runner.seg_type = 'modelpack'
                dataset.shape = runner.get_input_shape()

            elif args.model_segmentation_type.lower() == 'deeplab':

                runner = SegmentationDeepLab(
                    model_path=args.model,
                    target=f'http://{args.target}/v1'
                )
                runner.seg_type = 'deeplab'
                dataset.shape = runner.get_input_shape()

        else:
            raise UnsupportedValidationTypeException(args.validate)

    # KERAS EVALUATION
    elif path.splitext(args.model)[1].lower() == ".h5":

        runner = KerasRunner(
            model_path=args.model,
            labels=dataset.labels,
            detection_iou_threshold=args.detection_iou,
            detection_score_threshold=args.detection_threshold,
            norm=args.norm,
            label_offset=args.label_offset
        )

    # TFLITE EVALUATION
    elif path.splitext(args.model)[1].lower() == ".tflite":
        raise NotImplementedError()

    # TensorRT Engine Evaluation
    elif path.splitext(args.model)[1].lower() == ".trt":

        runner = TensorRTRunner(
            engine_path=args.model,
            labels=dataset.labels,
            detection_score_threshold=args.detection_threshold,
            label_offset=args.label_offset
        )

    # Offline EVALUATION (TEXT FILES)
    elif path.splitext(args.model)[1].lower() == "":
        Writer.logger(
            "Model extension does not exist, reading text files",
            code='INFO'
        )

        parameters['detection-iou'] = None
        parameters['detection-threshold'] = None
        parameters['warmup'] = None
        parameters['maximum_detections'] = None
        parameters['normalization'] = None

        runner = OfflineRunner(
            annotation_source=args.model,
            labels=dataset.labels,
            format=args.offline_annotation_format,
            label_offset=args.label_offset
        )

    else:
        raise UnsupportedModelExtensionException(
            path.splitext(args.model)[1].lower()
        )

    if args.validate.lower() == 'detection':

        evaluator = DetectionEval(
            runner=runner,
            dataset=dataset,
            visualize=args.visualize,
            tensorboard=args.tensorboard,
            json_out=args.json_out,
            display=args.display,
            parameters=parameters
        )

        truth_values = evaluator.group_evaluation()
        evaluator.conclude(truth_values)

    elif args.validate.lower() == 'segmentation':

        evaluator = SegmentationEval(
            runner=runner,
            dataset=dataset,
            visualize=args.visualize,
            tensorboard=args.tensorboard,
            display=args.display,
            parameters=parameters
        )

        truth_values = evaluator.group_evaluation()
        evaluator.conclude(truth_values)

    else:
        raise UnsupportedValidationTypeException(args.validate)


if __name__ == '__main__':
    """
    Functionalities
        1. Validation of DeepViewRT (RTM).
        2. Validation of Keras (H5) models.
        3. Validation of TFLITE models.
        4. Validation of TensorRT engines (trt).
        5. Compatibility with TFRecord and DarkNet format datasets.
    """
    main()
