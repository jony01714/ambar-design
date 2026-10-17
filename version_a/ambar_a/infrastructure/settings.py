"""Configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    broker: str = "localhost"
    db_path: str = "ambar.db"
    llm_url: str = "http://localhost:11434/api/generate"
    llm_model: str = "llama3.2"
    co2_limit: float = 1000.0

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            broker=os.getenv("AMBAR_BROKER", cls.broker),
            db_path=os.getenv("AMBAR_DB", cls.db_path),
            llm_url=os.getenv("AMBAR_LLM_URL", cls.llm_url),
            llm_model=os.getenv("AMBAR_LLM_MODEL", cls.llm_model),
            co2_limit=float(os.getenv("AMBAR_CO2_LIMIT", cls.co2_limit)),
        )
