import logging
from taichu_serve import Service

logger = logging.getLogger(__name__)


class TestService(Service):
    def __init__(self, model_path):
        super(TestService, self).__init__(model_path)
        logger.info("self.model_path: %s",
                    model_path)

    def _preprocess(self, input_data, context):
        logger.info('enter _preprocess')
        
        return input_data

    def _inference(self, preprocessed_result, context):
        logger.info('enter _inference')
        
        return preprocessed_result

    def _postprocess(self, inference_result, context):
        logger.info('enter _postprocess')

        return inference_result

    def _warmup(self):
        logger.info('warmup finished')
