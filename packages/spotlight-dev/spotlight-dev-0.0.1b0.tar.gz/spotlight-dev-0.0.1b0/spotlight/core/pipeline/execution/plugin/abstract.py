from abc import ABC, abstractmethod
from typing import Any

from spotlight.core.pipeline.execution.rule.abstract import AbstractRule
from spotlight.core.pipeline.model.rule import RuleResult


class AbstractPlugin(ABC):
    @classmethod
    @abstractmethod
    def apply_rule(cls, data: Any, rule: AbstractRule) -> RuleResult:
        """
        This method applies a rule to the data provided

        Args:
            data (Any): The data associated with the plugin
            rule (AbstractRule): The rule being run on the data

        Returns:
            RuleResult: The result of the rule run
        """
        pass

    @classmethod
    @abstractmethod
    def use_plugin(cls, data: Any) -> bool:
        """
        This method returns true if the plugin should be used for the data type passed in

        NOTE: The PluginRegistry loop through all the plugin and returns the first option that returns true, so make
        sure your loaded plugins dont clash (i.e. return True for the same data types)

        Args:
            data (Any): Data to be tested

        Returns:
            bool: A flag representing if the plugin can be used with this data or not
        """
        pass
