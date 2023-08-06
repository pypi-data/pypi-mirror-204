import logging
import duckdb
import pandas as pd

from data_watch.api.service.rule.model import RuleResponse
from data_watch.common.date.function import current_timestamp
from data_watch.common.enum import Status, Severity
from data_watch.pipeline.model import RuleResult


logger = logging.getLogger(__name__)


def apply_rule(data: pd.DataFrame, rule: RuleResponse) -> RuleResult:
    """
    Runs the rule on the data.

    Args:
        data (pd.DataFrame): The data being tested
        rule (RuleResponse): The rule being applied to the data

    Result:
        RuleResult: The result of the rule
    """
    logger.debug(f"Running rule {rule.name}")
    query = f"""
        SELECT *
        FROM data
        WHERE {rule.predicate}
    """
    start_time = current_timestamp()
    result = duckdb.query(query).to_df()
    end_time = current_timestamp()
    result = build_rule_result(rule, start_time, end_time, result)
    logger.debug(f"Rule result: {result}")
    logger.info(
        f"Rule completed [name={rule.name}, flagged_results={result.flagged_results}, threshold={rule.threshold}]: {result.status}"
    )
    return result


def build_rule_result(
    rule: RuleResponse, start_time: int, end_time: int, result: pd.DataFrame
) -> RuleResult:
    """
    Helper method for building the rule result.

    Args:
        rule (RuleResponse): The rule being applied to the data
        start_time (int): The timestamp from when the job started
        end_time (int): The timestamp from when the job ended
        result (pd.DataFrame): All the rules that failed the test

    Result:
        RuleResult: The result of the rule
    """
    status = get_rule_status(result, rule.threshold, rule.severity)
    return RuleResult(
        start_time=start_time,
        end_time=end_time,
        status=status,
        flagged_results=len(result),
        rule=rule.copy(),
    )


def get_rule_status(result: pd.DataFrame, threshold: int, severity: Severity) -> Status:
    """
    Helper method for determining the Status of the rule.

    Args:
        result (pd.DataFrame): All the rows that failed the rule
        threshold (int): The number of results needed to cause the rule to fail
        severity (Severity): The severity level of the rule

    Returns:
        Status: The status of the rule
    """
    success = len(result) < threshold
    if success:
        return Status.SUCCESS
    elif severity == Severity.WARN:
        return Status.WARNING
    else:
        return Status.FAILURE
