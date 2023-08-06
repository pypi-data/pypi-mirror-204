from typing import Dict, Any

from data_watch.api.service.job.view.__util import _get_job_view_request_info
from data_watch.common.decorators import data_request

from data_watch.common.requests import (
    __async_get_request,
)


@data_request
async def async_get_job_view(id: str) -> Dict[str, Any]:
    """
    Asynchronously get job view by ID.

    Args:
        id (str): Job ID

    Returns:
        Dict[str, Any]: Job view response
    """
    request_info = _get_job_view_request_info(id)
    return __async_get_request(**request_info)
