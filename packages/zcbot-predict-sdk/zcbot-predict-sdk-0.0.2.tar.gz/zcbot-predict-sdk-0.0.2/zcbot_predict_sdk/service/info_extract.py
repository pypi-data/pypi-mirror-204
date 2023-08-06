from typing import Union, Dict, List
from .base import BaseService
from ..model.callback import Callback
from ..model.param import InfoExtractParam


class InfoExtractService(BaseService):
    """品牌、型号、通用名"""

    def extract_sku(self, task_params: Union[Dict, InfoExtractParam] = None, callback: Callback = None, **kwargs):
        _task_params = task_params.dict() if isinstance(task_params, InfoExtractParam) else task_params
        return self.celery_client.apply(task_name='info_extract.sku', task_params=_task_params, callback=callback, **kwargs)
