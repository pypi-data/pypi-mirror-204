import logging
from multiprocessing import Pool
from typing import Any, List

from spotlight.core.pipeline.execution.rule import AbstractRule
from spotlight.core.pipeline.model.rule import RuleResult
from spotlight.core.pipeline.execution.plugin.abstract import AbstractPlugin
from spotlight.core.pipeline.execution.plugin.registry import PluginRegistry


logger = logging.getLogger(__name__)


def run_pipeline(
    data: Any,
    rules: List[AbstractRule],
    *,
    multi_processing: bool = False,
    processes: int = 5,
) -> List[RuleResult]:
    """
    Wrapper for the different pipeline types.

    Args:
        data (Any): The data being run through the pipeline
        rules (List[AbstractRule]): The rules being run on the data
        multi_processing (bool): Optional flag to run the rules over the data concurrently
        processes (int): Optional number of process to spin up when running the rules concurrently

    Returns:
        List[RuleResult]: The result of running the pipeline
    """
    plugin = PluginRegistry.get_plugin(data)
    if plugin is None:
        raise ValueError(f"Data type {type(data)} is not supported")

    if multi_processing:
        logger.debug(f"Running the multiprocessing pipeline with {processes} processes")
        return _multiprocessing_pipeline(plugin, data, rules, processes)
    return _synchronous_pipeline(plugin, data, rules)


def _synchronous_pipeline(
    plugin: AbstractPlugin, data: Any, rules: List[AbstractRule]
) -> List[RuleResult]:
    """
    Runs all the rules sequentially over the data.

    Args:
        plugin (AbstractPlugin): Plugin for running rules
        data (Any): The data being run through the pipeline
        rules(List[AbstractRule]): The rules being run on the data

    Returns:
        List[RuleResult]: The result of running the pipeline
    """
    results = [plugin.apply_rule(data, rule) for rule in rules]
    return results


def _multiprocessing_pipeline(
    plugin: AbstractPlugin, data: Any, rules: List[AbstractRule], processes: int
) -> List[RuleResult]:
    """
    Runs all the rules over the data in parallel.

    NOTE: The number of rules run in parallel is dependent on the number of processes.

    Args:
        plugin (AbstractPlugin): Plugin for running rules
        data (Any): The data being run through the pipeline
        rules (List[AbstractRule]): The rules being run on the data
        processes (int): The number of process to spin up when running the rules concurrently

    Returns:
        List[RuleResult]: The result of running the pipeline
    """
    with Pool(processes=processes) as pool:
        results = pool.map(lambda rule: plugin.apply_rule(data, rule), rules)
    return results
