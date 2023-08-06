from typing import Dict, Any, List

from data_watch.api.model import SearchRequest
from data_watch.api.service.job.__util import (
    _get_job_request_info,
    _get_jobs_request_info,
    _create_job_request_info,
    _update_job_request_info,
    _delete_job_request_info,
    _search_jobs_request_info,
    _get_job_tags_request_info,
)
from data_watch.api.service.job.model import JobRequest
from data_watch.common.decorators import async_data_request

from data_watch.common.requests import (
    __async_get_request,
    __async_post_request,
    __async_put_request,
    __async_delete_request,
)


@async_data_request
async def async_get_job(id: str) -> Dict[str, Any]:
    """
    Asynchronously get job by ID.

    Args:
        id (str): Job ID

    Returns:
        Dict[str, Any]: Job response
    """
    request_info = _get_job_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request
async def async_get_jobs() -> List[Dict[str, Any]]:
    """
    Asynchronously get all jobs.

    Returns:
        List[Dict[str, Any]]: List of job responses
    """
    request_info = _get_jobs_request_info()
    return await __async_get_request(**request_info)


@async_data_request
async def async_search_jobs(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Asynchronously search all jobs.

    Parameters:
        request (SearchRequest): A request carrying the search query

    Returns:
        List[Dict[str, Any]]: List of job responses
    """
    request_info = _search_jobs_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_create_job(request: JobRequest) -> Dict[str, Any]:
    """
    Asynchronously create job.

    Args:
        request (JobRequest): Job request

    Returns:
        Dict[str, Any]: Job response
    """
    request_info = _create_job_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request
async def async_update_job(id: str, request: JobRequest) -> Dict[str, Any]:
    """
    Asynchronously update job.

    NOTE: Groups associated to the job are not updated

    Args:
        id (str): Job ID
        request (JobRequest): Job request

    Returns:
        Dict[str, Any]: Job response
    """
    request_info = _update_job_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_delete_job(id: str) -> None:
    """
    Asynchronously delete job by ID.

    Args:
        id (str): Job ID

    Returns:
        None
    """
    request_info = _delete_job_request_info(id)
    return await __async_delete_request(**request_info)


@async_data_request
async def async_get_job_tags() -> List[str]:
    """
    Asynchronously get all the tags used by jobs

    Returns:
        List[str]: A list of all the tags used for jobs
    """
    request_info = _get_job_tags_request_info()
    return await __async_get_request(**request_info)
