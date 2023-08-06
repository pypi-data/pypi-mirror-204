from typing import Dict, Any

from data_watch.api.service.group.view.__util import (
    _get_group_view_request_info,
    _get_group_view_by_name_request_info,
)
from data_watch.common.decorators import data_request

from data_watch.common.requests import (
    __get_request,
)


@data_request
def get_group_view(id: str) -> Dict[str, Any]:
    """
    Get group view by ID.

    Args:
        id (str): Group ID

    Returns:
        Dict[str, Any]: Group view response
    """
    request_info = _get_group_view_request_info(id)
    return __get_request(**request_info)


@data_request
def get_group_view_by_name(name: str) -> Dict[str, Any]:
    """
    Get group view by name.

    Args:
        name (str): Group name

    Returns:
        Dict[str, Any]: Group view response
    """
    request_info = _get_group_view_by_name_request_info(name)
    return __get_request(**request_info)
