from spotlight.api.rule.model import RuleResponse
from spotlight.core.common.enum import Severity
from spotlight.core.pipeline.execution.rule.abstract import AbstractRule
from spotlight.core.pipeline.execution.rule.enum import RuleTypes


class SQLRule(AbstractRule):
    def __init__(
        self,
        name: str,
        predicate: str,
        threshold: int,
        severity: Severity,
    ):
        self._name = name
        self.predicate = predicate
        self._threshold = threshold
        self._severity = severity

    @property
    def name(self) -> str:
        return self._name

    @property
    def threshold(self) -> int:
        return self._threshold

    @property
    def severity(self) -> Severity:
        return self._severity

    def to_dict(self):
        props = self._properties()
        props.update({"type": RuleTypes.SQL.value, "predicate": self.predicate})
        return props

    @classmethod
    def from_rule_response(cls, rule: RuleResponse) -> "SQLRule":
        return cls(
            name=rule.name,
            predicate=rule.predicate,
            threshold=rule.threshold,
            severity=Severity(rule.severity),
        )
