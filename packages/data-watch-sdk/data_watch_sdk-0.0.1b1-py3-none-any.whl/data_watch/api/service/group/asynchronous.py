from typing import Dict, Any, List

from data_watch.api.model import SearchRequest, LookupRequest
from data_watch.api.service.group.__util import (
    _get_group_request_info,
    _get_groups_request_info,
    _create_group_request_info,
    _update_group_request_info,
    _delete_group_request_info,
    _search_groups_request_info,
    _unique_group_name_request_info,
    _get_group_by_name_request_info,
    _get_groups_by_rule_id_request_info,
    _get_group_tags_request_info,
    _get_groups_by_lookup_request_info,
)
from data_watch.api.service.group.model import GroupRequest
from data_watch.common.decorators import async_data_request

from data_watch.common.requests import (
    __async_get_request,
    __async_post_request,
    __async_put_request,
    __async_delete_request,
)


@async_data_request
async def async_get_group(id: str) -> Dict[str, Any]:
    """
    Asynchronously get group by ID.

    Args:
        id (str): Group ID

    Returns:
        Dict[str, Any]: Group response
    """
    request_info = _get_group_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request
async def async_get_group_by_name(group_name: str) -> Dict[str, Any]:
    """
    Asynchronously get group by name.

    Args:
        group_name (str): Group name

    Returns:
        Dict[str, Any]: Group response
    """
    request_info = _get_group_by_name_request_info(group_name)
    return await __async_get_request(**request_info)


@async_data_request
async def async_get_groups() -> List[Dict[str, Any]]:
    """
    Asynchronously get all groups.

    Returns:
        List[Dict[str, Any]]: List of group responses
    """
    request_info = _get_groups_request_info()
    return await __async_get_request(**request_info)


@async_data_request
async def async_get_groups_by_lookup(request: LookupRequest) -> List[Dict[str, Any]]:
    """
    Asynchronously get all groups by lookup.

    Args:
        request (LookupRequest): The group information used in the group look up

    Returns:
        List[Dict[str, Any]]: List of group responses
    """
    request_info = _get_groups_by_lookup_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_get_groups_by_rule_id(rule_id: str) -> List[Dict[str, Any]]:
    """
    Asynchronously get all groups by rule ID.

    Args:
        rule_id (str): Rule ID

    Returns:
        List[Dict[str, Any]]: List of group responses
    """
    request_info = _get_groups_by_rule_id_request_info(rule_id)
    return await __async_get_request(**request_info)


@async_data_request
async def async_search_groups(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Asynchronously search all groups.

    Parameters:
        request (SearchRequest): A request carrying the search query

    Returns:
        List[Dict[str, Any]]: List of group responses
    """
    request_info = _search_groups_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_create_group(request: GroupRequest) -> Dict[str, Any]:
    """
    Asynchronously create group.

    Args:
        request (GroupRequest): Group request

    Returns:
        Dict[str, Any]: Group response
    """
    request_info = _create_group_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request
async def async_update_group(id: str, request: GroupRequest) -> Dict[str, Any]:
    """
    Asynchronously update group.

    Args:
        id (str): Group ID
        request (GroupRequest): Group request

    Returns:
        Dict[str, Any]: Group response
    """
    request_info = _update_group_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_delete_group(id: str) -> None:
    """
    Asynchronously delete group by ID.

    Args:
        id (str): Group ID

    Returns:
        None
    """
    request_info = _delete_group_request_info(id)
    return await __async_delete_request(**request_info)


@async_data_request
async def async_get_group_tags() -> List[str]:
    """
    Asynchronously get all the tags used by groups

    Returns:
        List[str]: A list of all the tags used for groups
    """
    request_info = _get_group_tags_request_info()
    return await __async_get_request(**request_info)


@async_data_request
async def async_is_group_name_unique(group_name: str) -> bool:
    """
    Asynchronously checks to see if the group name is unique

    Args:
        group_name (str): The new group name that is being tested

    Returns:
        Bool: A boolean representing if the name is unique
    """
    request_info = _unique_group_name_request_info(group_name)
    return await __async_post_request(**request_info)
