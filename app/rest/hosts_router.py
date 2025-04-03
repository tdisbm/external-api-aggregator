from typing import List

from fastapi import APIRouter, HTTPException

from app.components.dto.Host import Host
from app.database.repository.host_repository import (
    get_hosts, get_host, get_hosts_audit_date_ordered,
    get_hosts_vuln_count_ordered, get_hosts_last_vuln_date_scan_ordered,
    get_hosts_by_agent
)

hosts_router = APIRouter()


@hosts_router.get("/hosts/read/details/{hostname_or_external_id}/", response_model=Host)
async def read_host(hostname_or_external_id: str):
    host = get_host(hostname_or_external_id)
    if host:
        return host
    raise HTTPException(
        status_code=404,
        detail=f"No host with hostname or external id {hostname_or_external_id} found"
    )


@hosts_router.get("/hosts/read/batch/", response_model=List[Host])
async def read_hosts(skip: int, limit: int):
    return get_hosts(skip=skip, limit=limit)


@hosts_router.get("/hosts/read/newest/", response_model=List[Host])
async def read_hosts_audit_newest(skip: int, limit: int):
    return get_hosts_audit_date_ordered(skip=skip, limit=limit, newest_first=True)


@hosts_router.get("/hosts/read/oldest/", response_model=List[Host])
async def read_hosts_audit_oldest(skip: int, limit: int):
    return get_hosts_audit_date_ordered(skip=skip, limit=limit, newest_first=False)


@hosts_router.get("/hosts/read/vuln-count/most/", response_model=List[Host])
async def read_hosts_vuln_top(skip: int, limit: int) -> List[Host]:
    return get_hosts_vuln_count_ordered(skip=skip, limit=limit, vulnerable_first=True)


@hosts_router.get("/hosts/read/vuln-count/least/", response_model=List[Host])
async def read_hosts_vuln_bottom(skip: int, limit: int) -> List[Host]:
    return get_hosts_vuln_count_ordered(skip=skip, limit=limit, vulnerable_first=False)


@hosts_router.get("/hosts/read/vuln-date/newest/", response_model=List[Host])
async def read_hosts_vuln_scan_newest(skip: int, limit: int) -> List[Host]:
    return get_hosts_last_vuln_date_scan_ordered(skip=skip, limit=limit, newest_first=True)


@hosts_router.get("/hosts/read/vuln-date/oldest/", response_model=List[Host])
async def read_hosts_vuln_scan_oldest(skip: int, limit: int) -> List[Host]:
    return get_hosts_last_vuln_date_scan_ordered(skip=skip, limit=limit, newest_first=False)


@hosts_router.get("/hosts/read/agent/", response_model=List[Host])
async def read_hosts_by_agent(agent_name: str, skip: int, limit: int):
    return get_hosts_by_agent(agent_name=agent_name, skip=skip, limit=limit)
