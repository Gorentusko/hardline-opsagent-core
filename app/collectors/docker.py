import json
import socket
import subprocess
from typing import Any


def _run(cmd: list[str], timeout: int = 8) -> dict[str, Any]:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "cmd": cmd,
            "returncode": out.returncode,
            "stdout": out.stdout.strip()[-10000:],
            "stderr": out.stderr.strip()[-3000:],
        }
    except Exception as exc:
        return {"cmd": cmd, "error": str(exc)}


def _docker_socket_get(path: str) -> dict[str, Any]:
    request = (
        f"GET {path} HTTP/1.1\r\n"
        "Host: docker\r\n"
        "Connection: close\r\n\r\n"
    ).encode()

    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect("/var/run/docker.sock")
            sock.sendall(request)
            chunks = []
            while True:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                chunks.append(chunk)

        raw = b"".join(chunks).decode("utf-8", errors="replace")
        header, _, body = raw.partition("\r\n\r\n")
        status_line = header.splitlines()[0] if header else ""
        parts = status_line.split()
        status_code = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 0
        return {
            "ok": 200 <= status_code < 300,
            "status_code": status_code,
            "body": body,
            "raw_header": header[-1000:],
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def collect_docker_state() -> dict[str, Any]:
    # Preferred path: Docker Engine API through mounted Unix socket.
    # This avoids requiring a docker CLI inside the container and works better on Docker Desktop.
    socket_result = _docker_socket_get("/containers/json")
    if socket_result.get("ok"):
        try:
            containers = json.loads(socket_result.get("body", "[]"))
        except json.JSONDecodeError:
            containers = []
        return {
            "docker_available": True,
            "collector_method": "docker_socket_api",
            "containers": containers,
            "raw": {"status_code": socket_result.get("status_code")},
        }

    # Fallback: docker CLI if someone builds a custom image with it.
    ps = _run(["docker", "ps", "--format", "{{json .}}"])
    containers = []
    if ps.get("returncode") == 0 and ps.get("stdout"):
        for line in ps["stdout"].splitlines():
            try:
                containers.append(json.loads(line))
            except json.JSONDecodeError:
                containers.append({"raw": line})

    return {
        "docker_available": ps.get("returncode") == 0,
        "collector_method": "docker_cli_fallback" if ps.get("returncode") == 0 else "unavailable",
        "containers": containers,
        "socket_error": socket_result.get("error"),
        "raw": ps,
    }
