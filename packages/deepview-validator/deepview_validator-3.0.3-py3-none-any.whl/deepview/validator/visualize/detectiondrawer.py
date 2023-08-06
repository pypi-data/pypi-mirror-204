# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.visualize.core import Drawer
from PIL import Image, ImageDraw, ImageFont


class DetectionDrawer(Drawer):
    """
    This class provides methods to draw detection visualizations
    such as bounding boxes.
    Unit-test for this class is defined under:
        file: test/test_detectiondrawer.py

    Parameters
    ----------
        None

    Raises
    ------
        None
    """

    def __init__(self):
        super(DetectionDrawer, self).__init__()

    @staticmethod
    def __drawRect(image_draw, color, text, textpos, boxpos):
        """
        This function draws bouding boxes and texts on the image.
        Unit-test for this function is defined under:
            file: test/test_detectiondrawer.py
            function: test_draw_with_pillow

        Parameters
        ----------

            image_draw: PIL ImageDraw object
                The image to draw on.

            color: str
                Name to color the bounding box.

            text: str
                Text to describe the bounding box.

            testpos: tuple
                (x, y) position of the text.

            boxpos: tuple
                ((x1, y1), (x2, y2)) position of the box.

        Returns
        -------
            None

        Raises
        -------
            None
        """

        font = ImageFont.load_default()
        text_width, text_height = font.getsize(text)
        box_text_x1 = boxpos[0][0]
        box_text_x2 = box_text_x1 + text_width

        if textpos[1] > boxpos[0][1]:
            box_text_y1 = boxpos[1][1] - text_height
        else:
            box_text_y1 = boxpos[0][1] - text_height

        box_text_y2 = box_text_y1 + text_height

        image_draw.rectangle(
            boxpos,
            outline=color,
            width=3
        )
        image_draw.rectangle(
            [(box_text_x1, box_text_y1), (box_text_x2, box_text_y2)],
            fill=color
        )
        image_draw.text(
            textpos,
            text,
            font=font,
            align='left',
            fill="black"
        )

    def draw_with_pillow(
            self,
            iou_t,
            score_t,
            nimage,
            instance,
            matches,
            extras,
            _,
            iou_list):
        """
        This method draws detection bounding boxes and texts on the image
        with distinct colors.

            - RoyalBlue = ground truth or false negatives.
            - LimeGreen = true positives.
            - OrangeRed = false positives.

        Unit-test for this method is defined under:
            file: test/test_detectiondrawer.py
            function: test_draw_with_pillow

        Parameters
        ----------

            iou_t: float
                The validation IoU threshold between 0 and 1.

            score_t: float
                The validation score threshold between 0 and 1.

            nimage: (H, W, 3) np.ndarray
                Image represented as an numpy array.

            instance: dict
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

            matches: np.ndarray or list
                This contains the indices of matches
                [[index_dt, index_gt], ...].

            extras: np.ndarray or list
                This contains indices of extra predictions (local FP).

            iou_list: np.ndarray or list
                This contains IoU values of each match in respective order.

        Returns
        -------
            images: PIL image
                The image with drawn bounding boxes and text.
        """

        image = Image.fromarray(nimage)
        image_draw = ImageDraw.Draw(image)
        width = instance.get('gt_instance').get('width')
        height = instance.get('gt_instance').get('height')

        # Draw Ground Truths
        for label, box in zip(
            instance.get('gt_instance').get('labels'),
            instance.get('gt_instance').get('boxes')
        ):

            p1 = (float(box[0]) * width, float(box[1]) * height)
            p2 = (float(box[2]) * width, float(box[3]) * height)
            self.__drawRect(image_draw, "RoyalBlue",
                            f"{label} ", (p1[0], p2[1] - 12), (p1, p2))

        # Draw Predictions
        for match in matches:
            dt_label = instance.get('dt_instance').get('labels')[match[0]]
            gt_label = instance.get('gt_instance').get('labels')[match[1]]
            box = instance.get('dt_instance').get('boxes')[match[0]]
            iou = iou_list[match[0]]
            score = instance.get('dt_instance').get('scores')[match[0]]

            text = f"{dt_label} {round(score * 100, 2)}% {round(float(iou), 2)}"
            p1 = (float(box[0]) * width, float(box[1]) * height)
            p2 = (float(box[2]) * width, float(box[3]) * height)

            if dt_label == gt_label:
                if float(iou) >= iou_t:
                    color = "LimeGreen"
                else:
                    color = "OrangeRed"
            else:
                color = "OrangeRed"

            if score >= score_t:
                self.__drawRect(image_draw, color, text,
                                (p1[0], p1[1] - 10), (p1, p2))

        # Draw Extra Predictions
        for extra_index in extras:
            dt_label = instance.get('dt_instance').get('labels')[extra_index]
            box = instance.get('dt_instance').get('boxes')[extra_index]
            score = instance.get('dt_instance').get('scores')[extra_index]

            text = f'Extra: {dt_label} {round(score * 100, 2)}%'
            p1 = (float(box[0]) * width, float(box[1]) * height)
            p2 = (float(box[2]) * width), int(float(box[3]) * height)

            if score >= score_t:
                self.__drawRect(image_draw, "OrangeRed", text,
                                (p1[0], p1[1] - 10), (p1, p2))

        return image
