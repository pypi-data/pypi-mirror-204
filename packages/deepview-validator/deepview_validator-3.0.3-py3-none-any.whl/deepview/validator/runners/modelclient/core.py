# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import ModelRunnerFailedConnectionException
from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.runners.core import Runner


class ModelClientRunner(Runner):
    """
    This class uses the modelclient API to run DeepViewRT models.
    Unit-test for this class is defined under:
        file: test/deepview/validator/runners/modelclient/test_core.py

    Parameters
    ----------

        model_path: str
            The path to the model.

        target: str
            The modelrunner target in the EVK. Ex. 10.10.40.205:10817.

    Raises
    ------
        ModelRunnerFailedConnectionException
            This exception will be raised if connecting to modelrunner
            is unsuccessful.

        MissingLibraryException
            This exception will be raised if certain libraries
            are not installed.
    """

    def __init__(
        self,
        model_path,
        target
    ):
        self.model_path = model_path
        self.target = target
        super(ModelClientRunner, self).__init__(model_path)

    def load_model(self):
        """
        This method loads the model to the modelrunner target.
        Unit-test for this method is defined under:
            file: test/deepview/validator/runners/modelclient/test_core.py
            function: test_load_model

        Parameters
        ----------
            None

        Returns
        -------
            None

        Raises
        ------
            ModelRunnerFailedConnectionException
                This exception will be raised if connecting to modelrunner
                is unsuccessful.

            MissingLibraryException
                This exception will be raised if the library requests
                is not installed.
        """

        try:
            import requests as req
        except ImportError:
            raise MissingLibraryException(
                "requests is needed to communicate " +
                "with the modelclient server.")

        try:
            from deepview.rt.modelclient import ModelClient
            self.client = ModelClient(
                uri=self.target,
                rtm=self.model_path,
            )
        except req.exceptions.ConnectionError:
            raise ModelRunnerFailedConnectionException(self.target)

        self.shape = req.get(self.target +
                             '/model').json()['inputs'][0]['shape'][1:]
        self.shape = (self.shape[1], self.shape[0], self.shape[2])

        self.input_name = req.get(self.target +
                                  '/model').json()['inputs'][0].get('name')
        self.outputs = req.get(self.target + '/model').json()['outputs']
        self.device = req.get(self.target).json()["engine"]
