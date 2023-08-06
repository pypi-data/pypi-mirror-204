from typing import Dict, Any, List

from data_watch.api.model import SearchRequest, LookupRequest
from data_watch.api.service.group.__util import (
    _get_group_request_info,
    _get_group_by_name_request_info,
    _get_groups_request_info,
    _get_groups_by_rule_id_request_info,
    _search_groups_request_info,
    _create_group_request_info,
    _update_group_request_info,
    _delete_group_request_info,
    _get_group_tags_request_info,
    _unique_group_name_request_info,
    _get_groups_by_lookup_request_info,
)
from data_watch.api.service.group.model import GroupRequest
from data_watch.common.decorators import data_request

from data_watch.common.requests import (
    __get_request,
    __post_request,
    __put_request,
    __delete_request,
)


@data_request
def get_group(id: str) -> Dict[str, Any]:
    """
    Get group by ID.

    Args:
        id (str): Group ID

    Returns:
        Dict[str, Any]: Group response
    """
    request_info = _get_group_request_info(id)
    return __get_request(**request_info)


@data_request
def get_group_by_name(group_name: str) -> Dict[str, Any]:
    """
    Get group by name.

    Args:
        group_name (str): Group name

    Returns:
        Dict[str, Any]: Group response
    """
    request_info = _get_group_by_name_request_info(group_name)
    return __get_request(**request_info)


@data_request
def get_groups() -> List[Dict[str, Any]]:
    """
    Get all groups.

    Returns:
        List[Dict[str, Any]]: List of group responses
    """
    request_info = _get_groups_request_info()
    return __get_request(**request_info)


@data_request
def get_groups_by_lookup(request: LookupRequest) -> List[Dict[str, Any]]:
    """
    Get all groups by lookup.

    Args:
        request (LookupRequest): The group information used in the group look up

    Returns:
        List[Dict[str, Any]]: List of group responses
    """
    request_info = _get_groups_by_lookup_request_info(request)
    return __post_request(**request_info)


@data_request
def get_groups_by_rule_id(rule_id: str) -> List[Dict[str, Any]]:
    """
    Get all groups by rule ID.

    Args:
        rule_id (str): Rule ID

    Returns:
        List[Dict[str, Any]]: List of group responses
    """
    request_info = _get_groups_by_rule_id_request_info(rule_id)
    return __get_request(**request_info)


@data_request
def search_groups(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Search all groups.

    Parameters:
        request (SearchRequest): A request carrying the search query

    Returns:
        List[Dict[str, Any]]: List of group responses
    """
    request_info = _search_groups_request_info(request)
    return __post_request(**request_info)


@data_request
def create_group(request: GroupRequest) -> Dict[str, Any]:
    """
    Create group.

    Args:
        request (GroupRequest): Group request

    Returns:
        Dict[str, Any]: Group response
    """
    request_info = _create_group_request_info(request)
    return __put_request(**request_info)


@data_request
def update_group(id: str, request: GroupRequest) -> Dict[str, Any]:
    """
    Update group.

    Args:
        id (str): Group ID
        request (GroupRequest): Group request

    Returns:
        Dict[str, Any]: Group response
    """
    request_info = _update_group_request_info(id, request)
    return __post_request(**request_info)


@data_request
def delete_group(id: str) -> None:
    """
    Delete group by ID.

    Args:
        id (str): Group ID

    Returns:
        None
    """
    request_info = _delete_group_request_info(id)
    return __delete_request(**request_info)


@data_request
def get_group_tags() -> List[str]:
    """
    Get all the tags used by groups

    Returns:
        List[str]: A list of all the tags used for groups
    """
    request_info = _get_group_tags_request_info()
    return __get_request(**request_info)


@data_request
def is_group_name_unique(group_name: str) -> bool:
    """
    Checks to see if the group name is unique

    Args:
        group_name (str): The new group name that is being tested

    Returns:
        Bool: A boolean representing if the name is unique
    """
    request_info = _unique_group_name_request_info(group_name)
    return __post_request(**request_info)
