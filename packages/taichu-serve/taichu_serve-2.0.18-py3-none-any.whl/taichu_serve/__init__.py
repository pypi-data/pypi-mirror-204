__version__ = "1.0.4"

import time
import logging

from abc import ABCMeta, abstractmethod
from taichu_serve.model_server import BaseModelService

logger = logging.getLogger(__name__)


class ModelServer(BaseModelService):
    '''SingleNodeModel defines abstraction for model service which loads a
    single model.
    '''

    def __init__(self, model_path):
        super(ModelServer, self).__init__(model_path)
        self._ready = False
        self._ctx = {}

    def warmup(self):
        start_time = time.time()
        self._warmup()
        self._ready = True
        logger.info('warmup time: ' + str((time.time() - start_time) * 1000) + 'ms')

    def inference(self, data, request_id, stream=False):
        """
        Wrapper function to run preprocess, inference and postprocess functions.
        """
        logger.info('recv request: ' + request_id)

        context = self._ctx.get(request_id)
        if context is None:
            context = {}
            if stream:
                logger.info('create context for request: ' + request_id)
                self._ctx[request_id] = context

        pre_start_time = time.time()
        data = self._preprocess(data, context=context)
        infer_start_time = time.time()

        # Update preprocess latency metric
        pre_time_in_ms = (infer_start_time - pre_start_time) * 1000
        logger.info('preprocess time: ' + str(pre_time_in_ms) + 'ms')

        data = self._inference(data, context=context)
        infer_end_time = time.time()
        infer_in_ms = (infer_end_time - infer_start_time) * 1000

        logger.info('infer time: ' + str(infer_in_ms) + 'ms')
        data = self._postprocess(data, context=context)

        # Update inference latency metric
        post_time_in_ms = (time.time() - infer_end_time) * 1000
        logger.info('postprocess time: ' + str(post_time_in_ms) + 'ms')

        logger.info('latency: ' + str(pre_time_in_ms + infer_in_ms + post_time_in_ms) + 'ms')
        return data

    @abstractmethod
    def _inference(self, data, context={}):
        '''
        Internal inference methods. Run forward computation and
        return output.

        Parameters
        ----------
        data : map of NDArray
            Preprocessed inputs in NDArray format.

        Returns
        -------
        list of NDArray
            Inference output.
        '''
        return data

    @abstractmethod
    def _preprocess(self, data, context={}):
        '''
        Internal preprocess methods. Do transformation on raw
        inputs and convert them to NDArray.

        Parameters
        ----------
        data : map of object
            Raw inputs from request.

        Returns
        -------
        list of NDArray
            Processed inputs in NDArray format.
        '''
        return data

    @abstractmethod
    def _postprocess(self, data, context={}):
        '''
        Internal postprocess methods. Do transformation on inference output
        and convert them to MIME type objects.

        Parameters
        ----------
        data : map of NDArray
            Inference output.

        Returns
        -------
        list of object
            list of outputs to be sent back.
        '''
        return data

    def destroy_context(self, request_id):
        logger.info('destroy context for request: ' + request_id)
        if request_id in self._ctx:
            del self._ctx[request_id]

    @abstractmethod
    def _warmup(self):
        pass

    @property
    def model_version(self):
        return '1'

    @property
    def ready(self):
        return self._ready

    def run(self, *args, **kwargs):
        from taichu_serve.command import cli
        cli(*args, **kwargs)
