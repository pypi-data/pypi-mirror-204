from typing import Dict

from .base import BaseService
from ..model.callback import Callback
from ..model.param import InfoPredictParam


class StaplesCatalogService(BaseService):

    def predict_catalog1(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.staples1', task_params=task_params.dict(), callback=callback,
                                        **kwargs)

    def predict_catalog4(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.staples4', task_params=task_params.dict(), callback=callback,
                                        **kwargs)

    def predict_catalog6(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.staples6', task_params=task_params.dict(), callback=callback,
                                        **kwargs)

    def predict_brand(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='brand.staples', task_params=task_params.dict(), callback=callback,
                                        **kwargs)


class JslinkCatalogService(BaseService):

    def predict_catalog1(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.jslink1', task_params=task_params.dict(), callback=callback,
                                        **kwargs)

    def predict_catalog4(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.jslink4', task_params=task_params.dict(), callback=callback,
                                        **kwargs)

    def predict_brand(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='brand.jslink', task_params=task_params.dict(), callback=callback,
                                        **kwargs)


class ZjmiCatalogService(BaseService):

    def predict_catalog3(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.zjmi3', task_params=task_params.dict(), callback=callback, **kwargs)

    def predict_brand(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='brand.zjmi', task_params=task_params.dict(), callback=callback,
                                        **kwargs)
