import logging
from typing import Optional, List, Any

from spotlight.api.job.model import JobResponse
from spotlight.core.common.date.function import current_timestamp
from spotlight.core.pipeline.execution import run_pipeline
from spotlight.core.pipeline.execution.rule import AbstractRule
from spotlight.core.pipeline.model.pipeline import PipelineResult

from spotlight.core.pipeline.utils.asynchronously import (
    async_start_job,
    async_stop_job,
)
from spotlight.core.pipeline.utils.synchronously import start_job, stop_job

logger = logging.getLogger(__name__)


def __dq_pipeline(
    data: Any,
    job_name: str,
    rules: List[AbstractRule],
    multi_processing: bool = False,
    processes: int = 5,
):
    start_time = current_timestamp()
    logger.info(f"Starting data quality pipeline [{job_name=}, {start_time=}]")
    rule_results = run_pipeline(
        data, rules, multi_processing=multi_processing, processes=processes
    )
    end_time = current_timestamp()
    result = PipelineResult.build_result(job_name, start_time, end_time, rule_results)
    logger.debug(f"Data quality pipeline result: {result}")
    logger.info(
        f"Data quality pipeline finished [{job_name=}, {end_time=}]: {result.status}"
    )
    return result


def data_quality_pipeline(
    data: Any,
    job_name: str,
    *,
    group_names: Optional[List[str]] = None,
    group_ids: Optional[List[str]] = None,
    additional_rules: Optional[List[AbstractRule]] = None,
    metadata: Optional[dict] = None,
    tags: Optional[List[str]] = None,
    multi_processing: bool = False,
    processes: int = 5,
) -> JobResponse:
    """
    Runs data through a data quality pipeline.

    NOTE: You must provide the group names and/or the group ids for this method to run.
    NOTE: The number of rules run in parallel is dependent on the number of processes.

    Args:
        data (Any): Data that is run through the pipeline
        job_name (str): Name assigned to the job created from running this pipeline
        group_names (Optional[List[str]]): List of group names to use with the pipeline
        group_ids (Optional[List[str]]): List of group ids to use with the pipeline
        additional_rules (List[AbstractRule]): additional rules to run on the pipeline (specifically rules that aren't
        supported in the API i.e. AbstractCustomCodeRules)
        metadata (Optional[dict]): Metadata added to the job information
        tags (Optional[List[str]]): Tags added to the job
        multi_processing (bool): Optional flag to run the rules over the data concurrently
        processes (int): Optional number of process to spin up when running the rules concurrently

    Returns:
        JobResponse: The job response with all the information from the run
    """
    job, rules = start_job(
        job_name=job_name,
        group_names=group_names,
        group_ids=group_ids,
        metadata=metadata,
        tags=tags,
    )
    rules.extend(additional_rules or [])
    result = __dq_pipeline(data, job.name, rules, multi_processing, processes)

    job = stop_job(
        job=job,
        pipeline_result=result,
        tags=tags,
    )
    return job


async def async_data_quality_pipeline(
    data: Any,
    job_name: str,
    *,
    group_names: Optional[List[str]] = None,
    group_ids: Optional[List[str]] = None,
    additional_rules: Optional[List[AbstractRule]] = None,
    metadata: Optional[dict] = None,
    tags: Optional[List[str]] = None,
    multi_processing: bool = False,
    processes: int = 5,
) -> JobResponse:
    """
    Asynchronously runs data through a data quality pipeline.

    NOTE: You must provide the group names and/or the group ids for this method to run.
    NOTE: The number of rules run in parallel is dependent on the number of processes.

    Args:
        data (Any): Data that is run through the pipeline
        job_name (str): Name assigned to the job created from running this pipeline
        group_names (Optional[List[str]]): List of group names to use with the pipeline
        group_ids (Optional[List[str]]): List of group ids to use with the pipeline
        additional_rules (List[AbstractRule]): additional rules to run on the pipeline (specifically rules that aren't
        supported in the API i.e. AbstractCustomCodeRules)
        metadata (Optional[dict]): Metadata added to the job information
        tags (Optional[List[str]]): Tags added to the job
        multi_processing (bool): Optional flag to run the rules over the data concurrently
        processes (int): Optional number of process to spin up when running the rules concurrently

    Returns:
        JobResponse: The job response with all the information from the run
    """
    job, rules = await async_start_job(
        job_name=job_name,
        group_names=group_names,
        group_ids=group_ids,
        metadata=metadata,
        tags=tags,
    )
    rules.extend(additional_rules or [])
    result = __dq_pipeline(data, job.name, rules, multi_processing, processes)

    job = await async_stop_job(
        job=job,
        pipeline_result=result,
        tags=tags,
    )
    return job


def offline_data_quality_pipeline(
    job_name: str,
    data: Any,
    rules: List[AbstractRule],
    *,
    multi_processing: bool = False,
    processes: int = 5,
) -> PipelineResult:
    """
    Runs data through a data quality pipeline.

    NOTE: This pipeline will run locally and the results will NOT be synced to the API making the results unavailable in
    the UI
    NOTE: The number of rules run in parallel is dependent on the number of processes.

    Args:
        job_name (str): Name for the test job
        data (Any): Data that is run through the pipeline
        rules (List[RuleRequest]): A list of the rules to run on the pipeline
        multi_processing (bool): Optional flag to run the rules over the data concurrently
        processes (int): Optional number of process to spin up when running the rules concurrently

    Returns:
        dict: A dict containing the metadata of the test job
    """
    result = __dq_pipeline(data, job_name, rules, multi_processing, processes)
    return result
