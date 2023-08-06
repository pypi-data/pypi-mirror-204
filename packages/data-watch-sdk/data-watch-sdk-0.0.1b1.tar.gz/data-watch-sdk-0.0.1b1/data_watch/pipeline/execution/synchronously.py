import logging
from typing import Any, List

import pandas as pd

from data_watch.api.service.rule.model import RuleResponse
from data_watch.pipeline.model import DataQualityResult
from data_watch.pipeline.pandas import (
    pipeline as pd_pipeline,
    mp_pipeline as pd_mp_pipeline,
)


logger = logging.getLogger(__name__)


def run_pipeline(
    data: Any,
    rules: List[RuleResponse],
    *,
    multi_processing: bool = False,
    processes: int = 5,
) -> DataQualityResult:
    """
    Wrapper for the different pipeline types.

    Args:
        data (Any): The data being run through the pipeline
        rules (List[RuleResponse]): The rules being run on the data
        multi_processing (bool): Optional flag to run the rules over the data concurrently
        processes (int): Optional number of process to spin up when running the rules concurrently

    Returns:
        DataQualityResult: The result of running the pipeline
    """
    if multi_processing:
        logger.debug(f"Running the multiprocessing pipeline with {processes} processes")
        _multiprocessing_pipeline(data, rules, processes)
    return _synchronous_pipeline(data, rules)


def _synchronous_pipeline(data: Any, rules: List[RuleResponse]) -> DataQualityResult:
    """
    Runs all the rules sequentially over the data.

    Args:
        data (Any): The data being run through the pipeline
        rules(List[RuleResponse]): The rules being run on the data

    Returns:
        DataQualityResult: The result of running the pipeline
    """
    if isinstance(data, pd.DataFrame):
        result = pd_pipeline(data, rules)
    else:
        raise ValueError(f"Data type {type(data)} is not supported")

    return result


def _multiprocessing_pipeline(
    data: Any, rules: List[RuleResponse], processes: int
) -> DataQualityResult:
    """
    Runs all the rules over the data in parallel.

    NOTE: The number of rules run in parallel is dependent on the number of processes.

    Args:
        data (Any): The data being run through the pipeline
        rules (List[RuleResponse]): The rules being run on the data
        processes (int): The number of process to spin up when running the rules concurrently

    Returns:
        DataQualityResult: The result of running the pipeline
    """
    if isinstance(data, pd.DataFrame):
        result = pd_mp_pipeline(data, rules, processes)
    else:
        raise ValueError(f"Data type {type(data)} is not supported")

    return result
