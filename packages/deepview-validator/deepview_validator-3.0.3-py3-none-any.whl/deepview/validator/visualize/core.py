# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

import matplotlib.pyplot as plt
import numpy as np
import io


class Drawer:
    """
    This class is an abstract class that provides common methods
    between other visualizer classes.
    Unit-test for this class is defined under:
        file: test/test_drawer.py

    Parameters
    ----------
        None

    Raises
    ------
        None
    """

    def __init__(self):
        pass

    @staticmethod
    def figure2numpy(figure):
        """
        This method converts a matplotlib.pyplot figure into a numpy
        array so that it can be posted to tensorboard.
        Unit-test for this method is defined under:
            file: test/test_drawer.py
            function: test_figure2numpy

        Parameters
        ----------

            figure: matplotlib.pyplot
                This is the figure to convert to a numpy array.

        Returns
        -------
            figure: np.ndarray
                The figure that is represented as a numpy array

        Raises
        ------
            None
        """

        io_buf = io.BytesIO()
        figure.savefig(io_buf, format='raw')
        io_buf.seek(0)
        nimage = np.reshape(
            np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
            newshape=(
                int(figure.bbox.bounds[3]),
                int(figure.bbox.bounds[2]),
                -1)
        )
        io_buf.close()
        return nimage

    @staticmethod
    def plot_classification(class_histogram_data, model="Training Model"):
        """
        This method plots the bar charts showing the
        precision, recall, and accuracy per class.
        It also shows the number of true positives,
        false positives, and false negatives per class.
        Unit-test for this method is defined under:
            file: test/test_drawer.py
            function: test_plot_classification

        Parameters
        ----------

            class_histogram_data: dict.
                This contains information about the metrics per class.

                .. code-block:: python

                    {
                        'label_1': {
                            'precision 0.5': The calculated precision at
                                        IoU threshold 0.5 for the class,
                            'recall 0.5': The calculated recall at
                                        IoU threshold 0.5 for the class,
                            'accuracy 0.5': The calculated accuracy at
                                        IoU threshold 0.5 for the class,
                            'tp 0.5': The number of true posituves
                                    for the class,
                            'fn 0.5': The number of false negatives
                                    for the class,
                            'class fp 0.5': The number of classification
                                    false positives for the class,
                            'local fp 0.5': The number of localization
                                    false positives for the class,
                            'gt': The number of grounds truths for the class
                        },
                        'label_2': ...
                    }

            model: str
                The name of the model.

        Returns
        -------
            fig: matplotlib.pyplot
                This shows two histograms on the left that compares
                the precision, recall, and accuracy
                and on the right compares then number
                of true positives, false positives,
                and false negatives
                for each class.

        Raises
        ------
            None
        """

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10))
        # Score = [[prec c1, prec c2, prec c3], [rec c1, rec c2, rec c3], [acc
        # c1, acc c2, acc c3]]
        X = np.arange(len(class_histogram_data))
        labels, precision, recall, accuracy = list(), list(), list(), list()
        tp, fp, fn = list(), list(), list()

        for cls, value, in class_histogram_data.items():
            labels.append(cls)
            precision.append(round(value.get('precision') * 100, 2))
            recall.append(round(value.get('recall') * 100, 2))
            accuracy.append(round(value.get('accuracy') * 100, 2))
            tp.append(value.get('tp'))
            fn.append(value.get('fn'))
            fp.append(value.get('fp'))

        ax1.bar(X + 0.0, precision, color='m', width=0.25)
        ax1.bar(X + 0.25, recall, color='y', width=0.25)
        ax1.bar(X + 0.5, accuracy, color='c', width=0.25)

        ax2.bar(X + 0.0, tp, color='LimeGreen', width=0.25)
        ax2.bar(X + 0.25, fn, color='RoyalBlue', width=0.25)
        ax2.bar(X + 0.5, fp, color='OrangeRed', width=0.25)

        ax1.set_ylabel('Score (%)')
        ax2.set_ylabel("Total Number")
        fig.suptitle(f"{model} Evaluation Table")

        ax1.xaxis.set_ticks(range(len(labels)), labels, rotation='vertical')
        ax2.xaxis.set_ticks(range(len(labels)), labels, rotation='vertical')

        colors = {'precision': 'm', 'recall': 'y', 'accuracy': 'c'}
        labels = list(colors.keys())
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label])
                   for label in labels]
        ax1.legend(handles, labels)
        colors = {
            'true positives': 'green',
            'false negatives': 'blue',
            'false positives': 'red'}
        labels = list(colors.keys())
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label])
                   for label in labels]
        ax2.legend(handles, labels)

        return fig

    @staticmethod
    def plot_pr_curve(px, py, ap, names=(), model="Training Model"):
        """
        This method plots the precision-recall
        curve based on the implementation from:
        https://github.com/ultralytics/yolov5/blob/master/utils/metrics.py#L318
        Unit-test for this method is defined under:
            file: test/deepview/validator/test_visualize.py
            function: test_plot_pr_curve

        Parameters
        ----------

            px: (NxM) np.ndarray
                N => number of classes and M is the number of recall values.

            py: (NxM) np.ndarray
                N => number of classes, M => number of precision values.

            ap: (NxM) np.ndarray
                N => number of classes, M => 10 denoting each IoU threshold
                from (0.5 to 0.95 at 0.05 intervals).

            names: list
                This contains unique string labels captured.

            model: str
                The name of the model tested.

        Returns
        -------
            fig: matplotlib.pyplot
                The precision recall plot where recall is denoted
                on the x-axis and precision is denoted
                on the y-axis.

        Raises
        ------
            None
        """

        fig, ax = plt.subplots(1, 1, figsize=(9, 6), tight_layout=True)

        if 0 < len(names) < 21:  # display per-class legend if < 21 classes
            for i, y in enumerate(py):
                # plot(recall, precision)
                ax.plot(
                    px[i],
                    y,
                    linewidth=1,
                    label=f'{names[i]} {ap[i, 0]:.3f}'
                )
        else:
            # plot(recall, precision)
            ax.plot(px, py, linewidth=1, color='grey')

        ax.plot(
            np.mean(px, axis=0),
            np.mean(py, axis=0),
            linewidth=3,
            color='blue',
            label='all classes %.3f mAP@0.5' % ap[:, 0].mean()
        )
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.01)
        ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        ax.set_title(f'{model} Precision-Recall Curve')
        return fig

    @staticmethod
    def plot_mc_curve(
            px,
            py,
            names=(),
            xlabel='Confidence',
            ylabel='Metric',
            model="Training Model"):
        """
        This method plots Metric-Confidence curve
        based on the implementation from:
        https://github.com/ultralytics/yolov5/blob/master/utils/metrics.py#L341
        Unit-test for this method is defined under:
            file: test/deepview/validator/test_visualize.py
            function: test_plot_mc_curve

        Parameters
        ----------

            px: (NxM) np.ndarray
                N => number of classes and M is the number of
                confidence values.

            py: (NxM) np.ndarray
                N => number of classes, M => number of
                (f1, precision, recall) values.

            x-label: str
                The x-axis metric name to plot.

            y-label: str
                The y-axis metric name to plot.

            names: list
                This contains unique string labels captured.

            model: str
                The name of the model tested.

        Returns
        -------
            fig: matplotlib.pyplot
                This method is used to plot precision vs. confidence,
                recall vs. confidence, and f1 vs. confidence curves
                where confidence is situated on the x-axis.

        Raises
        ------
            None
        """

        def smooth(y, f=0.05):
            # Box filter of fraction f
            # number of filter elements (must be odd)
            nf = round(len(y) * f * 2) // 2 + 1
            p = np.ones(nf // 2)  # ones padding
            yp = np.concatenate((p * y[0], y, p * y[-1]), 0)  # y padded
            return np.convolve(
                yp, np.ones(nf) / nf, mode='valid'
            )  # y-smoothed

        # Metric-confidence curve
        fig, ax = plt.subplots(1, 1, figsize=(9, 6), tight_layout=True)

        if 0 < len(names) < 21:  # display per-class legend if < 21 classes
            for i, y in enumerate(py):
                # plot(confidence, metric)
                ax.plot(px, y, linewidth=1, label=f'{str(names[i])}')
        else:
            # plot(confidence, metric)
            ax.plot(px, py.T, linewidth=1, color='grey')

        y = smooth(py.mean(0), 0.05)
        ax.plot(
            px,
            y,
            linewidth=3,
            color='blue',
            label=f'all classes {y.max():.2f} at {px[y.argmax()]:.3f}')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        ax.set_title(f'{model} {ylabel}-Confidence Curve')
        return fig
