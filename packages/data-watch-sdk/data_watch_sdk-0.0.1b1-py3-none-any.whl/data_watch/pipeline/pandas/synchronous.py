from typing import List

import pandas as pd

from data_watch.api.service.rule.model import RuleResponse
from data_watch.pipeline.model import DataQualityResult
from data_watch.pipeline.pandas.__util import apply_rule
from multiprocessing import Pool


def pipeline(data: pd.DataFrame, rules: List[RuleResponse]) -> DataQualityResult:
    """
    Runs the all the pipeline rules on the provided dataset

    Args:
        data (pd.DataFrame): The data being put into the pipeline
        rules (List[RuleResponse]): The rules applied to the data

    Returns:
        DataQualityResult: The result of the pipeline run
    """
    results = [apply_rule(data, rule) for rule in rules]
    return DataQualityResult.from_rule_results(results)


def mp_pipeline(
    data: pd.DataFrame, rules: List[RuleResponse], processes: int
) -> DataQualityResult:
    """
    Runs the all the pipeline rules on the provided dataset in parallel using multiprocessing.

    NOTE: The number of rules run in parallel is dependent on the number of processes.

    Args:
        data (pd.DataFrame): The data being put into the pipeline
        rules (List[RuleResponse]): The rules applied to the data
        processes (int): The number of process to spin up when running the rules concurrently

    Returns:
        DataQualityResult: The result of the pipeline run
    """
    # Run pipeline
    with Pool(processes=processes) as pool:
        results = pool.map(lambda rule: apply_rule(data, rule), rules)
    return DataQualityResult.from_rule_results(results)
