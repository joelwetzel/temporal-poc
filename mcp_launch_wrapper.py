#!/usr/bin/env python3
"""
MCP launch wrapper: logs startup metadata, then runs a simulated mcp-server-time
in stdio mode using FastMCP.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

LOG_PATH = os.environ.get("MCP_LAUNCH_LOG", "/tmp/mcp_launches.jsonl")

record = {
    "ts": time.time(),
    "pid": os.getpid(),
    "ppid": os.getppid(),
    "argv": sys.argv,
    "cwd": os.getcwd(),
}

with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

# --- Simulated mcp-server-time MCP server ---
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("time")


@mcp.tool()
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time in a given timezone.

    Args:
        timezone: IANA timezone name, e.g. 'America/New_York' or 'UTC'.
    """
    try:
        tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        return f"Unknown timezone: {timezone}"
    now = datetime.now(tz)
    return now.isoformat()


@mcp.tool()
def convert_time(time_str: str, from_timezone: str, to_timezone: str) -> str:
    """Convert a time from one timezone to another.

    Args:
        time_str: ISO 8601 datetime string (e.g. '2026-03-25T12:00:00').
        from_timezone: Source IANA timezone name.
        to_timezone: Target IANA timezone name.
    """
    try:
        from_tz = ZoneInfo(from_timezone)
        to_tz = ZoneInfo(to_timezone)
    except ZoneInfoNotFoundError as e:
        return f"Unknown timezone: {e}"
    dt = datetime.fromisoformat(time_str).replace(tzinfo=from_tz)
    return dt.astimezone(to_tz).isoformat()


if __name__ == "__main__":
    mcp.run(transport="stdio")
