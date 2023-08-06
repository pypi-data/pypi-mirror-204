import logging
import pandas as pd

from spotlight.core.pipeline.execution.plugin.decorator import plugin
from spotlight.core.pipeline.execution.rule import SQLRule
from spotlight.core.pipeline.execution.rule.abstract import (
    AbstractRule,
    AbstractCustomCodeRule,
)
from spotlight.core.pipeline.model.rule import RuleResult
from spotlight.pandas.runners import (
    pandas_sql_rule_runner,
    pandas_custom_code_rule_runner,
)

logger = logging.getLogger(__name__)


@plugin(name="PandasPlugin", data_type=pd.DataFrame)
def pandas_plugin(data: pd.DataFrame, rule: AbstractRule) -> RuleResult:
    """
    This is the plugin interface for running rules on pandas dataframes

    Args:
        data (pd.DataFrame): The data being tested
        rule (AbstractRule): The rule being applied to the data

    Result:
        RuleResult: The result of the rule
    """
    if isinstance(rule, SQLRule):
        return pandas_sql_rule_runner(data, rule)
    elif isinstance(rule, AbstractCustomCodeRule):
        return pandas_custom_code_rule_runner(data, rule)
    else:
        raise ValueError(f"{type(rule)} is not supported in the pandas plugin")
