from data_watch.api.model import SearchRequest, LookupRequest
from data_watch.api.service.group.model import GroupRequest


def _get_group_request_info(id: str) -> dict:
    return {"endpoint": f"config/datawatch/group/{id}"}


def _get_group_by_name_request_info(name: str) -> dict:
    return {"endpoint": f"config/datawatch/group", "params": {"name": name}}


def _get_groups_request_info() -> dict:
    return {"endpoint": f"config/datawatch/group"}


def _get_groups_by_lookup_request_info(request: LookupRequest) -> dict:
    return {"endpoint": f"config/datawatch/group", "json": request.request_dict()}


def _get_groups_by_rule_id_request_info(rule_id: str) -> dict:
    return {"endpoint": f"config/datawatch/group", "params": {"rule_id": rule_id}}


def _search_groups_request_info(request: SearchRequest) -> dict:
    return {"endpoint": f"config/datawatch/group", "json": request.request_dict()}


def _create_group_request_info(request: GroupRequest) -> dict:
    return {"endpoint": f"config/datawatch/group", "json": request.request_dict()}


def _update_group_request_info(id: str, request: GroupRequest) -> dict:
    return {"endpoint": f"config/datawatch/group/{id}", "json": request.request_dict()}


def _delete_group_request_info(id: str) -> dict:
    return {"endpoint": f"config/datawatch/group/{id}"}


def _get_group_tags_request_info() -> dict:
    return {"endpoint": f"config/datawatch/group/tags"}


def _unique_group_name_request_info(name: str) -> dict:
    return {
        "endpoint": f"config/datawatch/group/unique",
        "params": {"group_name": name},
    }
