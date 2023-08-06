import json
from typing import List

from data_watch.api.model import SearchRequest, LookupRequest
from data_watch.api.service.rule.model import RuleRequest


def _get_rule_request_info(id: str) -> dict:
    return {"endpoint": f"config/datawatch/rule/{id}"}


def _get_rules_request_info() -> dict:
    return {"endpoint": f"config/datawatch/rule"}


def _get_all_rules_by_groups_request_info(request: LookupRequest) -> dict:
    return {"endpoint": f"config/datawatch/rule", "json": request.request_dict()}


def _search_rules_request_info(request: SearchRequest) -> dict:
    return {"endpoint": f"config/datawatch/rule", "json": request.request_dict()}


def _create_rule_request_info(request: RuleRequest) -> dict:
    return {"endpoint": f"config/datawatch/rule", "json": request.request_dict()}


def _update_rule_request_info(id: str, request: RuleRequest) -> dict:
    return {"endpoint": f"config/datawatch/rule/{id}", "json": request.request_dict()}


def _declarative_update_rule_groups_request_info(id: str, group_ids: List[str]) -> dict:
    return {"endpoint": f"config/datawatch/rule/{id}/group", "json": group_ids}


def _delete_rule_request_info(id: str) -> dict:
    return {"endpoint": f"config/datawatch/rule/{id}"}


def _get_rule_tags_request_info() -> dict:
    return {"endpoint": f"config/datawatch/rule/tags"}
