import celery
from nameko.standalone.rpc import ClusterRpcProxy

from vidis_algorithms_api.core import settings


class CeleryTaskLifecycle(celery.Task):
    def __init__(self):
        super(CeleryTaskLifecycle, self).__init__()
        self.layer = None
        
    def _call_remote(self, name_method: str, body: dict):
        with ClusterRpcProxy({"AMQP_URI": settings.CELERY_BROKER}) as rpc_client:
            response = getattr(rpc_client.internal_layers_service, name_method)(
                body
            )
            return response
        
    def before_start(self, task_id, args, kwargs):
        name, hsi_id, _ = args
        self.layer = self._call_remote("save_or_update", {
            "name": name,
            "type": self.name,
            "status": "computing",
            "status_detail": None,
            "path": None,
            "config": kwargs,
            "hyperspecter_id": hsi_id,
            "task_id": task_id
        })
        super().before_start(task_id, args, kwargs)

    def on_success(self, retval, task_id, args, kwargs):
        name, hsi_id, _ = args
        id = self.layer["id"]
        self.layer = self._call_remote("save_or_update", {
            "id": id,
            "name": name,
            "type": self.name,
            "status": "computed",
            "status_detail": None,
            "path": retval,
            "config": kwargs,
            "hyperspecter_id": hsi_id,
            "task_id": task_id
        })

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        name, hsi_id, _ = args
        id = self.layer["id"]
        self.layer = self._call_remote("save_or_update", {
            "id": id,
            "name": name,
            "type": self.name,
            "status": "error",
            "status_detail": einfo.value,
            "path": None,
            "config": kwargs,
            "hyperspecter_id": hsi_id,
            "task_id": task_id
        })

