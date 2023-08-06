def _get_group_view_request_info(id: str) -> dict:
    return {"endpoint": f"config/datawatch/group/view/{id}"}


def _get_group_view_by_name_request_info(name: str) -> dict:
    return {"endpoint": f"config/datawatch/group/view", "params": {"name": name}}
