from data_watch.api.model import SearchRequest
from data_watch.api.service.job.model import JobRequest


def _get_job_request_info(id: str) -> dict:
    return {"endpoint": f"config/datawatch/job/{id}"}


def _get_jobs_request_info() -> dict:
    return {"endpoint": f"config/datawatch/job"}


def _search_jobs_request_info(request: SearchRequest) -> dict:
    return {"endpoint": f"config/datawatch/job", "json": request.request_dict()}


def _create_job_request_info(request: JobRequest) -> dict:
    return {"endpoint": f"config/datawatch/job", "json": request.request_dict()}


def _update_job_request_info(id: str, request: JobRequest) -> dict:
    return {"endpoint": f"config/datawatch/job/{id}", "json": request.request_dict()}


def _delete_job_request_info(id: str) -> dict:
    return {"endpoint": f"config/datawatch/job/{id}"}


def _get_job_tags_request_info() -> dict:
    return {"endpoint": f"config/datawatch/job/tags"}
