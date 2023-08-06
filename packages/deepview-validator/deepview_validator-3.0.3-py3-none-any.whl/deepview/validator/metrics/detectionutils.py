# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import MatchingAlgorithmException
from deepview.validator.metrics.detectionmetrics import DetectionMetrics


def match_dt_gt(gt_boxes, dt_boxes):
    """
    This function attempts a best-fit of
    predictions to ground truths.
    Unit-test for this method is defined under:
        file: test/test_metrics.py
        function: test_match_dt_gt

    Parameters
    ----------

        gt_boxes: list or np.ndarray
            A list of ground truth boxes [[x1, y1, x2, y2]...].

        dt_boxes: list or np.ndarray
            A list of prediction boxes [[x1, y1, x2, y2]...].

    Returns
    -------
       indices : list
            This contains indices of the matches, extra predictions,
            missed ground truths, and
            IoU values for each match.

            * matches [[detection index, ground truth index],
                    [detection index, ground truth index], ...]
            * extras [detection index, detection index, ...]
            * missed [ground truth index, ground truth index, ...]

    Raises
    ------
        MatchingAlgorithmException
            This function will raise an exception if the method finds
            invalid values for IoU and ground truth index such as -1
    """

    # Rows is prediction, columns is ground truth
    iou_grid, iou_list = list(), list()
    index_matches, index_extra_dt = list(), list()

    if len(gt_boxes) > 0:
        for dti, dt in enumerate(dt_boxes):
            iou, gti = -1, -1
            iou_row = list()
            # get the best IOU and its GT index for the detection
            for id, gt in enumerate(gt_boxes):
                t_iou = DetectionMetrics.bbox_iou(dt, gt)
                # t_iou = self.metrics.compute_iou(dt, gt, width, height)
                iou_row.append(t_iou)
                if t_iou > iou:
                    iou = t_iou
                    gti = id

            iou_grid.append(iou_row)

            # At this point, (dti, gti) is the coordinates
            # for the best IOU for the detection.
            # If IOU or GTI is -1, you have problems.
            if iou == -1 or gti == -1:
                raise MatchingAlgorithmException(
                    iou, gti
                )

            iou_list.append(iou)

            # if the ground truth as already been matched, we need to see if
            # the new IOU score is higher.  If so, remove the old match,
            # add this match, and note the old match as a duplicate.
            # Otherwise, add this as a duplicate of the better match.
            if gti in [g for _, g in index_matches if g == gti]:

                for d, g in index_matches:
                    if g == gti:
                        break

                # if the new IOU is better than the previous IOU, remove
                # the old tuple, add the new one and mark the old detection as
                # a duplicate
                if iou > iou_list[d]:
                    index_matches.remove((d, gti))
                    index_matches.append((dti, gti))
                    index_extra_dt.append(d)

                # if the new detection IOU is worse, it's a dup of a better one
                else:
                    index_extra_dt.append(dti)

            # if the GT is not already matched, add it to the GT index list and
            # add the DT,GT index pair to the DT-GT index matching list
            else:
                index_matches.append((dti, gti))

        # Find the missed predictions by removing the indices that were
        # predicted.
        index_missed_gt = list(range(0, len(gt_boxes)))
        for match in index_matches:
            index_missed_gt.remove(match[1])

        # Sort the indices from smallest to largest to match box numbering [0],
        # [1] .... in original output.
        index_extra_dt.sort()
        index_missed_gt.sort()
        # Only sort by the second element of each list [[0,3], [1,2], [4,8]] ->
        # [[1,2], [0,3], [4,8]].
        index_matches.sort(key=lambda x: x[1])

    else:
        index_extra_dt = list(range(0, len(dt_boxes)))
        index_missed_gt = list()

    return [index_matches, index_extra_dt, index_missed_gt, iou_list]
