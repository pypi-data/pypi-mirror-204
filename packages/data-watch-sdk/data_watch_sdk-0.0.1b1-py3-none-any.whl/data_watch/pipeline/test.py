import logging
from typing import Any, List

from data_watch.api.service.group.view.model import GroupViewResponse
from data_watch.api.service.rule.model import RuleRequest, RuleResponse
from data_watch.common.date.function import current_timestamp
from data_watch.pipeline import run_pipeline


logger = logging.getLogger(__name__)


def data_quality_pipeline_test(
    job_name: str,
    data: Any,
    rules: List[RuleRequest],
    *,
    multi_processing: bool = False,
    processes: int = 5,
) -> dict:
    """
    Runs data through a data quality pipeline.

    NOTE: This pipeline will run locally and the results will NOT be synced to the API making them unavailable in the UI
    NOTE: The number of rules run in parallel is dependent on the number of processes.

    Args:
        job_name (str): Name for the test job
        data (Any): Data that is run through the pipeline
        rules (List[RuleRequest]): A list of the rules to run on the pipeline
        multi_processing (bool): Optional flag to run the rules over the data concurrently
        processes (int): Optional number of process to spin up when running the rules concurrently

    Returns:
        dict: A dict containing the metadata of the test job
    """
    rules = [_rule_response_to_request(rule) for rule in rules]
    start_time = current_timestamp()
    logger.info(f"Starting data quality pipeline [{job_name=}, {start_time=}]")
    result = run_pipeline(
        data, rules, multi_processing=multi_processing, processes=processes
    )
    end_time = current_timestamp()
    logger.debug(f"Data quality pipeline result: {result}")
    logger.info(
        f"Data quality pipeline finished [{job_name=}, {end_time=}]: {result.status}"
    )

    return {
        "job_name": job_name,
        "result": result,
        "start_time": start_time,
        "end_time": end_time,
    }


def _rule_response_to_request(rule: RuleRequest) -> RuleResponse:
    return RuleResponse(
        id="0",
        name=rule.name,
        description=rule.description,
        predicate=rule.predicate,
        threshold=rule.threshold,
        severity=rule.severity,
        tags=rule.tags + ["TEST", "LOCAL"],
        created_by="local-user",
        created_at=0,
        updated_by=None,
        updated_at=None,
    )
