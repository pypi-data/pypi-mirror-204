from typing import Optional, List, Tuple

from data_watch.api.service.group.asynchronous import async_get_groups_by_lookup
from data_watch.api.service.group.model import GroupResponse
from data_watch.api.service.group.view.asynchronous import (
    async_get_group_view_by_name,
    async_get_group_view,
)
from data_watch.api.service.group.view.model import GroupViewResponse
from data_watch.api.service.job import (
    async_create_job,
    async_update_job,
)
from data_watch.api.service.job.model import JobRequest, JobResponse
from data_watch.api.service.rule.asynchronous import async_get_rules_by_groups
from data_watch.api.service.rule.model import RuleResponse
from data_watch.api.model import LookupRequest
from data_watch.common.date.function import current_timestamp
from data_watch.common.enum import Status


async def async_get_rule_and_group_info(
    group_names: Optional[List[str]] = None, group_ids: Optional[List[str]] = None
) -> Tuple[List[GroupResponse], List[RuleResponse]]:
    """
    Asynchronous helper method for getting the group of rules from the group_id or group_name.

    Args:
        group_names (Optional[List[str]]): The name of rule groups
        group_ids (Optional[List[str]]): The id of the rule groups

    Returns:
        Tuple[List[GroupResponse], List[RuleResponse]]: A list of all the groups, and rules associated with the group
        info passed in
    """
    request = LookupRequest(group_names=group_names, group_ids=group_ids)
    response = await async_get_rules_by_groups(request)
    rules = [RuleResponse(**rule) for rule in response]
    group_response = await async_get_groups_by_lookup(request)
    groups = [GroupResponse(**group) for group in group_response]
    return groups, rules


async def async_start_job(
    job_name: str,
    *,
    group_names: Optional[List[str]] = None,
    group_ids: Optional[List[str]] = None,
    metadata: Optional[dict] = None,
    tags: Optional[List[str]] = None,
) -> Tuple[JobResponse, List[RuleResponse]]:
    """
    Asynchronously creates the job with the starting information.

    NOTE: You must provide the group_name or group_id but not both.

    Args:
        job_name (str): Name assigned to the job created from running this pipeline
        group_names (Optional[List[str]]): The name of rule groups
        group_ids (Optional[List[str]]): The id of the rule groups
        metadata (Optional[dict]): Metadata added to the job information
        tags (Optional[List[str]]): Tags added to the job

    Returns:
        Tuple[JobResponse, List[RuleResponse]]: The created job and the rules used in the job
    """
    groups, rules = await async_get_rule_and_group_info(
        group_names=group_names, group_ids=group_ids
    )
    request = JobRequest(
        name=job_name,
        status=Status.IN_PROGRESS,
        group_ids=[group.id for group in groups],
        metadata=metadata,
        tags=tags,
    )
    response = await async_create_job(request)
    job = JobResponse(**response)
    return job, rules


async def async_stop_job(
    job: JobResponse,
    status: Status,
    start_time: int,
    end_time: int,
    *,
    metadata: Optional[dict] = None,
    tags: Optional[List[str]] = None,
) -> JobResponse:
    """
    Asynchronously stops the job and updates it with all the results.

    Args:
        job (JobResponse): The job being updated
        status (Status): The status of the job
        start_time (int): The timestamp from when the job started
        end_time (int): The timestamp from when the job ended
        metadata (Optional[dict]): Metadata added to the job information
        tags (Optional[List[str]]): Tags added to the job

    Returns:
        JobResponse: The updated job
    """
    request = JobRequest(
        name=job.name,
        status=status,
        start_time=start_time,
        end_time=end_time,
        metadata=metadata or job.metadata,
        tags=tags or job.tags,
    )
    response = await async_update_job(job.id, request)
    job = JobResponse(**response)
    return job
