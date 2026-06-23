import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("OPSAGENT_APP_NAME", "Hardline OpsAgent Core")
    env: str = os.getenv("OPSAGENT_ENV", "demo")
    bind_host: str = os.getenv("OPSAGENT_BIND_HOST", "0.0.0.0")
    bind_port: int = int(os.getenv("OPSAGENT_BIND_PORT", "8088"))

    llm_provider: str = os.getenv("OPSAGENT_LLM_PROVIDER", "mock").lower()
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_model: str = os.getenv(
        "OPENROUTER_MODEL",
        "meta-llama/llama-3.1-8b-instruct:free",
    )

    max_llm_calls_per_run: int = int(os.getenv("OPSAGENT_MAX_LLM_CALLS_PER_RUN", "1"))
    max_input_chars: int = int(os.getenv("OPSAGENT_MAX_INPUT_CHARS", "12000"))
    llm_timeout_seconds: int = int(os.getenv("OPSAGENT_LLM_TIMEOUT_SECONDS", "45"))

    report_dir: str = os.getenv("OPSAGENT_REPORT_DIR", "/app/data/reports")
    state_dir: str = os.getenv("OPSAGENT_STATE_DIR", "/app/data/state")


settings = Settings()
