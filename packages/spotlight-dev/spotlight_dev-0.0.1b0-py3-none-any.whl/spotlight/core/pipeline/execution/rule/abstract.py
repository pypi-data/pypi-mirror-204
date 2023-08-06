from abc import ABC, abstractmethod
from typing import Any

from spotlight.core.common.enum import Severity
from spotlight.core.pipeline.execution.rule.enum import RuleTypes


class AbstractRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name of the rule
        """
        pass

    @property
    @abstractmethod
    def threshold(self) -> int:
        """
        Threshold for the number of flagged results to cause a rule to fail with the specified severity
        """
        pass

    @property
    @abstractmethod
    def severity(self) -> Severity:
        """
        The severity of a rule when it fails
        """
        pass

    @abstractmethod
    def to_dict(self):
        """
        Converts a rule to dict for saving a Rule to the RuleResult metadata
        """
        pass

    def _properties(self) -> dict:
        """
        Base properties of a rule
        """
        return {
            "name": self.name,
            "threshold": self.threshold,
            "severity": self.severity.value,
        }


class AbstractCustomCodeRule(AbstractRule, ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    def to_dict(self):
        props = self._properties()
        props.update({"type": RuleTypes.CUSTOM_CODE.value})
        return props

    @abstractmethod
    def test(self, data: Any) -> Any:
        """
        Method used to test the rule against the provided data
        """
        pass
