from typing import Dict, Any

from data_watch.api.service.group.view.__util import (
    _get_group_view_request_info,
    _get_group_view_by_name_request_info,
)
from data_watch.common.decorators import async_data_request

from data_watch.common.requests import (
    __async_get_request,
)


@async_data_request
async def async_get_group_view(id: str) -> Dict[str, Any]:
    """
    Asynchronously get group view by ID.

    Args:
        id (str): Group ID

    Returns:
        Dict[str, Any]: Group view response
    """
    request_info = _get_group_view_request_info(id)
    return __async_get_request(**request_info)


@async_data_request
async def async_get_group_view_by_name(name: str) -> Dict[str, Any]:
    """
    Asynchronously get group view by name.

    Args:
        name (str): Group name

    Returns:
        Dict[str, Any]: Group view response
    """
    request_info = _get_group_view_by_name_request_info(name)
    return await __async_get_request(**request_info)
