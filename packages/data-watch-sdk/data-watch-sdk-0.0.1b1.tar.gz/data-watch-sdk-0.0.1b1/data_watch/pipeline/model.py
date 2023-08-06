from collections import defaultdict
from typing import List

from data_watch.api.service.rule.model import RuleResponse
from data_watch.common.base import Base
from data_watch.common.enum import Status


class RuleResult(Base):
    """
    This is a model for the results of running a rule.
    """

    start_time: int
    end_time: int
    status: Status
    flagged_results: int
    rule: RuleResponse


class Metadata(Base):
    """
    This is a model that contains the metadata from running a set of rules.
    """

    results: List[RuleResult]
    succeeded: int
    failed: int
    warned: int
    total_rules: int

    @classmethod
    def from_rule_results(cls, results: List[RuleResult]):
        counts = defaultdict(int)
        for result in results:
            counts[result.status] += 1

        return cls(
            results=results,
            succeeded=counts[Status.SUCCESS.value],
            failed=counts[Status.FAILURE.value],
            warned=counts[Status.WARNING.value],
            total_rules=len(results),
        )


class DataQualityResult(Base):
    """
    This is a model of the data quality pipeline result
    """

    status: Status
    metadata: Metadata

    @classmethod
    def from_rule_results(cls, results: List[RuleResult]):
        metadata = Metadata.from_rule_results(results)
        return cls(status=cls.get_status(metadata), metadata=metadata)

    @staticmethod
    def get_status(metadata: Metadata) -> Status:
        if metadata.failed > 0:
            return Status.FAILURE
        elif metadata.warned > 0:
            return Status.WARNING
        else:
            return Status.SUCCESS
