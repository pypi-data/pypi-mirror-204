import copy
from typing import Optional, List, Tuple

from spotlight.api.group.model import GroupResponse
from spotlight.api.group.synchronous import get_groups_by_lookup
from spotlight.api.job import create_job, update_job
from spotlight.api.job.model import JobRequest, JobResponse
from spotlight.api.rule.model import RuleResponse
from spotlight.api.model import LookupRequest
from spotlight.api.rule.synchronous import get_rules_by_groups
from spotlight.core.common.enum import Status
from spotlight.core.pipeline.execution.rule import SQLRule
from spotlight.core.pipeline.model.pipeline import PipelineResult


def __get_rule_and_group_info(
    group_names: Optional[List[str]] = None, group_ids: Optional[List[str]] = None
) -> Tuple[List[GroupResponse], List[RuleResponse]]:
    """
    Helper method for getting rules from the group_ids and group_names.

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
    rule_response = get_rules_by_groups(request)
    rules = [RuleResponse(**rule) for rule in rule_response]
    group_response = get_groups_by_lookup(request)
    groups = [GroupResponse(**group) for group in group_response]
    return groups, rules


def start_job(
    job_name: str,
    *,
    group_names: Optional[List[str]] = None,
    group_ids: Optional[List[str]] = None,
    metadata: Optional[dict] = None,
    tags: Optional[List[str]] = None,
) -> Tuple[JobResponse, List[SQLRule]]:
    """
    Creates the job with the starting information.

    Args:
        job_name (str): Name assigned to the job created from running this pipeline
        group_names (Optional[List[str]]): List of group names to use with the pipeline
        group_ids (Optional[List[str]]): List of group ids to use with the pipeline
        metadata (Optional[dict]): Metadata added to the job information
        tags (Optional[List[str]]): Tags added to the job

    Returns:
        Tuple[JobResponse, List[Rule]]: The created job and the rules used in the job
    """
    groups, rules = __get_rule_and_group_info(
        group_names=group_names, group_ids=group_ids
    )
    request = JobRequest(
        name=job_name,
        status=Status.IN_PROGRESS,
        group_ids=[group.id for group in groups],
        metadata=metadata,
        tags=tags,
    )
    response = create_job(request)
    job = JobResponse(**response)
    return job, [SQLRule.from_rule_response(rule) for rule in rules]


def stop_job(
    job: JobResponse,
    pipeline_result: PipelineResult,
    *,
    tags: Optional[List[str]] = None,
) -> JobResponse:
    """
    Stops the job and updates it with all the results.

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
    response = update_job(job.id, request)
    job = JobResponse(**response)
    return job
