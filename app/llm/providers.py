from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import requests

from app.config import settings


class LLMProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...


@dataclass
class MockProvider:
    def generate(self, prompt: str) -> str:
        return (
            "## Runbook Draft\n\n"
            "Provider: mock/offline\n\n"
            "1. Review the health score and findings.\n"
            "2. Prioritize critical and warning findings.\n"
            "3. Confirm backups before remediation.\n"
            "4. Apply fixes manually or through an approved change process.\n"
            "5. Re-run `/analyze` and compare the new report.\n\n"
            "No paid AI call was made for this run."
        )


@dataclass
class OpenRouterProvider:
    api_key: str
    model: str

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is required for openrouter provider.")

        trimmed = prompt[: settings.max_input_chars]
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            timeout=settings.llm_timeout_seconds,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/hardlineitgroup/hardline-opsagent-core",
                "X-Title": "Hardline OpsAgent Core",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an operations assistant. Produce concise, actionable "
                            "runbooks. Use only supplied facts. Do not invent system state."
                        ),
                    },
                    {"role": "user", "content": trimmed},
                ],
                "max_tokens": 900,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


def get_provider() -> LLMProvider:
    if settings.llm_provider == "openrouter":
        return OpenRouterProvider(settings.openrouter_api_key, settings.openrouter_model)
    return MockProvider()
