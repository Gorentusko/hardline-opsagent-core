from app.evaluators.rules import evaluate_state


def test_disk_warning():
    state = {
        "system": {"disk_root": {"used_percent": 85}},
        "docker": {"docker_available": True, "collector_method": "test", "containers": []},
    }
    result = evaluate_state(state)
    assert result["score"] < 100
    assert result["health"] in {"healthy", "degraded", "critical"}


def test_no_docker_available():
    state = {
        "system": {"disk_root": {"used_percent": 20}},
        "docker": {"docker_available": False, "containers": []},
    }
    result = evaluate_state(state)
    assert any(f["area"] == "docker" for f in result["findings"])


def test_docker_available_message():
    state = {
        "system": {"disk_root": {"used_percent": 20}},
        "docker": {"docker_available": True, "collector_method": "docker_socket_api", "containers": [{"Id": "abc"}]},
    }
    result = evaluate_state(state)
    assert any("docker_socket_api" in f["message"] for f in result["findings"])
