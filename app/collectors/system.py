import os
import shutil
import subprocess
import time
from typing import Any


def _run(cmd: list[str], timeout: int = 5) -> dict[str, Any]:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "cmd": cmd,
            "returncode": out.returncode,
            "stdout": out.stdout.strip()[-6000:],
            "stderr": out.stderr.strip()[-2000:],
        }
    except Exception as exc:
        return {"cmd": cmd, "error": str(exc)}


def collect_system_state() -> dict[str, Any]:
    disk = shutil.disk_usage("/")
    return {
        "timestamp": int(time.time()),
        "hostname": os.uname().nodename,
        "uptime": _run(["uptime"]),
        "disk_root": {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "used_percent": round((disk.used / disk.total) * 100, 2),
        },
        "memory": _run(["free", "-m"]),
        "process_snapshot": _run(["ps", "aux"]),
    }
