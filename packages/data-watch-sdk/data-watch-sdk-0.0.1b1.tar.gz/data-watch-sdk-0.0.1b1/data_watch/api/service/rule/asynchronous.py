from typing import Dict, Any, List

from data_watch.api.model import SearchRequest, LookupRequest
from data_watch.api.service.rule.__util import (
    _get_rule_request_info,
    _get_rules_request_info,
    _create_rule_request_info,
    _update_rule_request_info,
    _delete_rule_request_info,
    _search_rules_request_info,
    _get_rule_tags_request_info,
    _declarative_update_rule_groups_request_info,
    _get_all_rules_by_groups_request_info,
)
from data_watch.api.service.rule.model import RuleRequest
from data_watch.common.decorators import async_data_request

from data_watch.common.requests import (
    __async_get_request,
    __async_post_request,
    __async_put_request,
    __async_delete_request,
)


@async_data_request
async def async_get_rule(id: str) -> Dict[str, Any]:
    """
    Asynchronously get rule by ID.

    Args:
        id (str): Rule ID

    Returns:
        Dict[str, Any]: Rule response
    """
    request_info = _get_rule_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request
async def async_get_rules() -> List[Dict[str, Any]]:
    """
    Asynchronously get all rules.

    Returns:
        List[Dict[str, Any]]: List of rule responses
    """
    request_info = _get_rules_request_info()
    return await __async_get_request(**request_info)


@async_data_request
async def async_get_rules_by_groups(request: LookupRequest) -> List[Dict[str, Any]]:
    """
    Asynchronously get all rules by groups.

    Args:
        request (LookupRequest): The group information used in the rule look up

    Returns:
        List[Dict[str, Any]]: List of rule responses
    """
    request_info = _get_all_rules_by_groups_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_search_rules(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Asynchronously search all rules.

    Parameters:
        request (SearchRequest): A request carrying the search query

    Returns:
        List[Dict[str, Any]]: List of rule responses
    """
    request_info = _search_rules_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_create_rule(request: RuleRequest) -> Dict[str, Any]:
    """
    Asynchronously create rule.

    Args:
        request (RuleRequest): Rule request

    Returns:
        Dict[str, Any]: Rule response
    """
    request_info = _create_rule_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request
async def async_update_rule(id: str, request: RuleRequest) -> Dict[str, Any]:
    """
    Asynchronously update rule.

    Args:
        id (str): Rule ID
        request (RuleRequest): Rule request

    Returns:
        Dict[str, Any]: Rule response
    """
    request_info = _update_rule_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_declarative_update_rule_groups(
    id: str, group_ids: List[str]
) -> Dict[str, Any]:
    """
    Asynchronously sets the state of the rule's groups to the ones passed in.

    Args:
        id (str): Rule ID
        group_ids (List[str]): List of group ids to put the rule in

    Returns:
        Dict[str, Any]: Rule group response
    """
    request_info = _declarative_update_rule_groups_request_info(id, group_ids)
    return await __async_post_request(**request_info)


@async_data_request
async def async_delete_rule(id: str) -> None:
    """
    Asynchronously delete rule by ID.

    Args:
        id (str): Rule ID

    Returns:
        None
    """
    request_info = _delete_rule_request_info(id)
    return await __async_delete_request(**request_info)


@async_data_request
async def async_get_rule_tags() -> List[str]:
    """
    Asynchronously get all the tags used by rules

    Returns:
        List[str]: A list of all the tags used for rules
    """
    request_info = _get_rule_tags_request_info()
    return await __async_get_request(**request_info)
