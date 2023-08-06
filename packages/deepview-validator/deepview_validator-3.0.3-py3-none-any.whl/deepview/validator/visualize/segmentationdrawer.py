# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.visualize.core import Drawer
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class SegmentationDrawer(Drawer):
    """
    This class provides methods for drawing segmentation masks on the image.
    Unit-test for this class is defined under:
        file: test/test_segmentationdrawer.py

    Parameters
    ----------
        None

    Raises
    -------
        None
    """

    def __init__(self):
        super(SegmentationDrawer, self).__init__()

    @staticmethod
    def polygon2maskimage(original_image, dt_polygon_list, gt_polygon_list):
        """
        This method masks the original image and returns the masked image
        with mask predictions on the left and ground truth masks on the right.
        Currently only supports two class: person and car.
        Unit-test for this method is defined under:
            file: test/test_segmentationdrawer.py
            function: test_polygon2maskimage

        Parameters
        ----------

            original_image: PIL Image object
                The original image opened using pillow.image.

            dt_polygon_list: list
                A list of predictions with polygon vertices
                [ [cls, x1, y1, x2, y2, x3, y3, ...] ...].

            gt_polygon_list: list
                A list of ground truth with polygon vertices
                [ [cls, x1, y1, x2, y2, x3, y3, ...] ...].

        Returns
        -------
            image: PIL image object
                The image with drawn mask where the left
                pane shows the ground truth mask and the right pane shows the
                prediction mask.

        Raises
        ------
            None
        """

        image_dt = original_image.convert("RGBA")
        new_dt = Image.new('RGBA', image_dt.size, (255, 255, 255, 0))
        img_dt = ImageDraw.Draw(new_dt)

        image_gt = original_image.convert("RGBA")
        new_gt = Image.new('RGBA', image_gt.size, (255, 255, 255, 0))
        img_gt = ImageDraw.Draw(new_gt)

        for dt_polygon in dt_polygon_list:
            img_dt.polygon(dt_polygon, fill=(255, 0, 0, 125))
            out_dt = Image.alpha_composite(image_dt, new_dt)

        for gt_polygon in gt_polygon_list:
            img_gt.polygon(gt_polygon, fill=(0, 0, 255, 125))
            out_gt = Image.alpha_composite(image_gt, new_gt)

        out_dt = out_dt.convert("RGB")
        out_gt = out_gt.convert("RGB")
        dst = Image.new('RGB', (out_dt.width + out_gt.width, out_dt.height))
        dst.paste(out_dt, (0, 0))
        dst.paste(out_gt, (out_dt.width, 0))
        return dst

    @staticmethod
    def mask2imagetransform(mask, rgba_colors, union=False):
        """
        This method will transform a numpy array of mask into an RGBA image.
        Current implementation will work only for two classes (person and car).
        Unit-test for this method is defined under:
            file: test/test_segmentationdrawer.py
            function: test_mask2imagetransform

        Parameter
        ---------

            mask: (height, width, 3) np.ndarray
                Array representing the mask.

            rgba_colors: tuple of ints
                (R,G,B,A) color

            union: bool
                Specify to mask all objects with one color (True).
                False otherwise.

        Returns
        -------
            image: PIL Image object
                The mask image.

        Raises
        ------
            None
        """
        # Transform dimension of masks from a 2D numpy array to 4D with RGBA
        # channels
        mask_4_channels = np.stack((mask,) * 4, axis=-1)

        if union:
            # Assign both person and car with color white
            mask_4_channels[mask_4_channels == 1] = 255
            # Temporarily unpack the bands for readability
            red, green, blue, _ = mask_4_channels.T
            # Areas with both person and car
            u_areas = (red == 255) & (blue == 255) & (green == 255)
            # Color person and car with blue
            mask_4_channels[..., :][u_areas.T] = rgba_colors[0]

        else:
            # Assign all person objects with color white (255, 255, 255)
            mask_4_channels[mask_4_channels == 1] = 255
            # Assign car objects with color grey ish (125, 125, 125)
            mask_4_channels[mask_4_channels == 2] = 125
            # Temporarily unpack the bands for readability
            red, green, blue, _ = mask_4_channels.T

            # Find areas with person objects ... (leaves alpha values alone...)
            person_areas = (red == 255) & (blue == 255) & (green == 255)
            # Find areas with car objects ... (leaves alpha values alone...)
            car_areas = (red == 125) & (blue == 125) & (green == 125)

            # Transpose back needed
            # Color person objects with blue
            mask_4_channels[..., :][person_areas.T] = rgba_colors[0]
            # Color car objects with red
            mask_4_channels[..., :][car_areas.T] = rgba_colors[1]

        # Convert array to image object for image processing
        im2 = Image.fromarray(mask_4_channels.astype(np.uint8))

        return im2

    def mask2maskimage(self, height, width, instances):
        """
        This method masks the original image and returns the original image
        with mask prediction on the left and mask ground truth on the right.
        Unit-test for this method is defined under:
            file: test/test_segmentationdrawer.py
            function: test_mask2maskimage

        Parameters
        ----------

            height: int
                The height of the model input shape.

            width: int
                The width of the model input shape.

            instances: dict
                This contains information such as:

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

        Returns
        -------
            image: PIL Image object
                The image with drawn masks where on the right pane
                shows the ground truth mask and on the left pane shows
                the prediction mask.

        Raises
        ------
            None
        """

        font = ImageFont.load_default()
        original_image = Image.open(instances.get(
            'gt_instance').get('image_path')).convert('RGB').copy()
        original_image = original_image.resize((width, height))

        gt_mask = instances.get('gt_instance').get('gt_mask')
        dt_mask = instances.get('dt_instance').get('dt_mask')

        # Convert array to image object for image processing
        gt_im2 = self.mask2imagetransform(
            gt_mask, rgba_colors=[
                (0, 0, 255, 130), (255, 0, 0, 130)]
            )
        dt_im2 = self.mask2imagetransform(
            dt_mask, rgba_colors=[
                (0, 0, 255, 130), (255, 0, 0, 130)]
            )

        # convert img to RGBA mode
        image_gt = original_image.convert("RGBA")
        image_dt = original_image.convert("RGBA")

        out_gt = Image.alpha_composite(image_gt, gt_im2)
        out_gt = out_gt.convert("RGB")

        out_dt = Image.alpha_composite(image_dt, dt_im2)
        out_dt = out_dt.convert("RGB")

        dst = Image.new('RGB', (out_dt.width + out_gt.width, out_dt.height))
        dst.paste(out_gt, (0, 0))
        dst.paste(out_dt, (out_dt.width, 0))

        drawtext = ImageDraw.Draw(dst)
        drawtext.text((0, 0), "GROUND TRUTH", font=font,
                      align='left', fill=(0, 0, 0))
        drawtext.text((out_dt.width, 0), "MODEL PREDICTION",
                      font=font, align='left', fill=(0, 0, 0))
        return dst

    def mask2mask4panes(
            self,
            height,
            width,
            instances,
            tp_mask,
            fp_mask,
            fn_mask):
        """
        This method creates a four pane image result:

            - The first pane shows the masks for ground truth.
            - Second pane shows masks for the model prediction.
            - Third pane shows masks for the union of ground truth and
              model prediction.
            - Fourth pane shows masks for tp, fp, fn.

        - For the first and second panes, person (blue) and car (red).
        - For the third pane, the union mask (blue).
        - For the last pane, the true positives, person (blue) car (red),
        false negatives and false positives, person (light-blue),
        car (light-red).

        Unit-test for this method is defined under:
            file: test/test_segmentationdrawer.py
            function: test_mask2mask4panes

        Parameters
        ----------

            height: int
                The height of the model input shape.

            width: int
                The width of the model input shape.

            instances: dict
                This contains information such as:

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

            tp_mask: (height, width) np.ndarray
                2D numpy array with the same size as the image and
                each element represents a pixel containing all true positives.

            fp_mask: (height, width) np.ndarray
                2D numpy array with the same size as the image and
                each element represents a pixel containing all false positives.

            fn_mask: (height, width) np.ndarray
                2D numpy array with the same size as the image and
                each element represents a pixel containing all false negatives.

        Returns
        -------
            image: PIL Image object
                The image with drawn masks panes.

        Raises
        ------
            None
        """

        font = ImageFont.load_default()
        original_image = Image.open(instances.get(
            'gt_instance').get('image_path')).convert('RGB').copy()
        original_image = original_image.resize((width, height))

        gt_mask = instances.get('gt_instance').get('gt_mask')
        dt_mask = instances.get('dt_instance').get('dt_mask')

        union_mask = np.add(dt_mask, gt_mask)
        union_mask = np.where(union_mask > 0, 1, union_mask)

        # Convert array to image object for image processing
        gt_im2 = self.mask2imagetransform(
            gt_mask, rgba_colors=[
                (0, 0, 255, 130), (255, 0, 0, 130)])
        dt_im2 = self.mask2imagetransform(
            dt_mask, rgba_colors=[
                (0, 0, 255, 130), (255, 0, 0, 130)])
        tp_im2 = self.mask2imagetransform(
            tp_mask, rgba_colors=[
                (0, 0, 255, 130), (255, 0, 0, 130)])
        fp_im2 = self.mask2imagetransform(
            fp_mask, rgba_colors=[
                (137, 207, 240, 130), (255, 114, 118, 130)])
        fn_im2 = self.mask2imagetransform(
            fn_mask, rgba_colors=[
                (137, 207, 240, 130), (255, 114, 118, 130)])
        u_im2 = self.mask2imagetransform(
            union_mask, rgba_colors=[
                (0, 0, 255, 130)], union=True)

        # convert img to RGBA mode
        image_gt = original_image.convert("RGBA")
        image_dt = original_image.convert("RGBA")
        image_union = original_image.convert("RGBA")
        image_separate = original_image.convert("RGBA")

        out_gt = Image.alpha_composite(image_gt, gt_im2).convert("RGB")
        out_dt = Image.alpha_composite(image_dt, dt_im2).convert("RGB")
        out_union = Image.alpha_composite(image_union, u_im2).convert("RGB")
        out_sep1 = Image.alpha_composite(image_separate, tp_im2)
        out_sep2 = Image.alpha_composite(out_sep1, fp_im2)
        out_sep3 = Image.alpha_composite(out_sep2, fn_im2).convert("RGB")

        dst = Image.new('RGB', (out_dt.width + out_gt.width,
                        out_dt.height + out_gt.height))
        dst.paste(out_gt, (0, 0))
        dst.paste(out_dt, (out_dt.width, 0))
        dst.paste(out_union, (0, out_dt.height))
        dst.paste(out_sep3, (out_dt.width, out_dt.height))

        drawtext = ImageDraw.Draw(dst)
        drawtext.text((0, 0), "GROUND TRUTH", font=font,
                      align='left', fill=(0, 0, 0))
        drawtext.text((out_dt.width, 0), "MODEL PREDICTION",
                      font=font, align='left', fill=(0, 0, 0))
        drawtext.text((0, out_dt.height), "GT U DT",
                      font=font, align='left', fill=(0, 0, 0))
        drawtext.text(
            (out_dt.width,
             out_dt.height),
            "TP (Blue/Red), FP/FN(Light Blue/Red)",
            font=font,
            align='left',
            fill=(
                0,
                0,
                0))
        return dst
