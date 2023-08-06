import copy
from typing import Optional, List, Tuple

from spotlight.api.group.asynchronous import async_get_groups_by_lookup
from spotlight.api.group.model import GroupResponse
from spotlight.api.job import (
    async_create_job,
    async_update_job,
)
from spotlight.api.job.model import JobRequest, JobResponse
from spotlight.api.rule.asynchronous import async_get_rules_by_groups
from spotlight.api.rule.model import RuleResponse
from spotlight.api.model import LookupRequest
from spotlight.core.common.enum import Status
from spotlight.core.pipeline.execution.rule import SQLRule
from spotlight.core.pipeline.model.pipeline import PipelineResult


async def __async_get_rule_and_group_info(
    group_names: Optional[List[str]] = None, group_ids: Optional[List[str]] = None
) -> Tuple[List[GroupResponse], List[RuleResponse]]:
    """
    Asynchronous helper method for getting the group of rules from the group_id or group_name.

    Args:
        group_names (Optional[List[str]]): The name of rule groups
        group_ids (Optional[List[str]]): The id of the rule groups

    Returns:
        Tuple[List[GroupResponse], List[RuleResponse]]: A list of all the groups, and rules associated with the group
        info passed in
    """
    request = LookupRequest(
        group_names=group_names if group_names else [],
        group_ids=group_ids if group_ids else [],
    )
    response = await async_get_rules_by_groups(request)
    rules = [RuleResponse(**rule) for rule in response]
    group_response = await async_get_groups_by_lookup(request)
    groups = [GroupResponse(**group) for group in group_response]
    return groups, rules


async def async_start_job(
    job_name: str,
    *,
    group_names: Optional[List[str]] = None,
    group_ids: Optional[List[str]] = None,
    metadata: Optional[dict] = None,
    tags: Optional[List[str]] = None,
) -> Tuple[JobResponse, List[SQLRule]]:
    """
    Asynchronously creates the job with the starting information.

    NOTE: You must provide the group_name or group_id but not both.

    Args:
        job_name (str): Name assigned to the job created from running this pipeline
        group_names (Optional[List[str]]): The name of rule groups
        group_ids (Optional[List[str]]): The id of the rule groups
        metadata (Optional[dict]): Metadata added to the job information
        tags (Optional[List[str]]): Tags added to the job

    Returns:
        Tuple[JobResponse, List[Rule]]: The created job and the rules used in the job
    """
    groups, rules = await __async_get_rule_and_group_info(
        group_names=group_names, group_ids=group_ids
    )
    request = JobRequest(
        name=job_name,
        status=Status.IN_PROGRESS,
        group_ids=[group.id for group in groups],
        metadata=metadata,
        tags=tags,
    )
    response = await async_create_job(request)
    job = JobResponse(**response)
    return job, [SQLRule.from_rule_response(rule) for rule in rules]


async def async_stop_job(
    job: JobResponse,
    pipeline_result: PipelineResult,
    *,
    tags: Optional[List[str]] = None,
) -> JobResponse:
    """
    Asynchronously stops the job and updates it with all the results.

    Args:
        job (JobResponse): The job being updated
        pipeline_result (PipelineResult): The result of the piepline
        tags (Optional[List[str]]): Tags added to the job

    Returns:
        JobResponse: The updated job
    """
    combined_metadata = copy.deepcopy(job.metadata)
    combined_metadata.update(pipeline_result.metadata.request_dict())
    request = JobRequest(
        name=job.name,
        status=pipeline_result.status,
        start_time=pipeline_result.start_time,
        end_time=pipeline_result.end_time,
        metadata=combined_metadata,
        tags=tags or job.tags,
    )
    response = await async_update_job(job.id, request)
    job = JobResponse(**response)
    return job
