import logging
import pandas as pd

from spotlight.api.rule.model import RuleResponse
from spotlight.core.common.enum import Severity, Status
from spotlight.core.pipeline import AbstractRule
from spotlight.core.pipeline.model.rule import RuleResult

logger = logging.getLogger(__name__)


def build_rule_result(
    rule: AbstractRule, start_time: int, end_time: int, result: pd.DataFrame
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
        rule=rule.to_dict(),
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
