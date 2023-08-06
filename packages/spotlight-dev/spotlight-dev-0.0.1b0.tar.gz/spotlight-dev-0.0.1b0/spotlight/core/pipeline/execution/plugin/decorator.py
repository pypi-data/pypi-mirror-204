from typing import Union, Callable, Any
from trycast import isassignable

from spotlight.core.pipeline.execution.plugin.abstract import AbstractPlugin
from spotlight.core.pipeline.execution.plugin.registry import PluginRegistry
from spotlight.core.pipeline.model.rule import RuleResult


def plugin(
    apply_rule: Callable[[Any, Any], RuleResult] = None,
    *,
    name: str = "Unnamed",
    data_type: type = None,
    register: bool = True
) -> Union[Callable, Any]:
    """
    This is a decorator to create a plugin from the apply method

    Args:
        apply_rule (Callable[[Any, Any], RuleResult]): The apply rule method for a plugin
        name (str): Name of the plugin
        data_type (type): The data type used with the plugin
        register (bool): A flag to register a plugin in the PluginRegistry or not
    """

    def wrap(fxn):
        if data_type is None:
            raise ValueError("Missing data_type")

        @classmethod
        def _apply_rule(cls, data: Any, rule: Any) -> RuleResult:
            return fxn(data, rule)

        @classmethod
        def _use_plugin(cls, data: Any) -> bool:
            return isassignable(data, data_type)

        new_plugin = type(
            name,
            (AbstractPlugin,),
            {"apply_rule": _apply_rule, "use_plugin": _use_plugin},
        )
        if register:
            PluginRegistry.register(new_plugin)
        return new_plugin

    if apply_rule is None:
        return wrap

    return wrap(apply_rule)
