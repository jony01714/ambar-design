"""Conversation skill: local LLM that can read the environment and call registered tools."""
from __future__ import annotations

from collections import deque

from ..core.bus import EventBus
from ..core.events import ReadingReceived, Reply, UserSaid
from ..core.ports import LanguageModel
from ..core.registry import ToolRegistry

TOOL_PREFIX = "TOOL:"


class ConversationSkill:
    def __init__(self, bus: EventBus, llm: LanguageModel, tools: ToolRegistry, history: int = 10):
        self._bus, self._llm, self._tools = bus, llm, tools
        self._recent: deque = deque(maxlen=history)
        bus.subscribe(ReadingReceived, lambda e: self._recent.append(e.reading))
        bus.subscribe(UserSaid, self._on_user)

    def _prompt(self, text: str) -> str:
        state = ", ".join(f"{r.node}/{r.kind}={r.value}" for r in self._recent) or "no readings"
        return (
            "You are Ambar, a local assistant.\n"
            f"Readings: {state}\nTools (reply with a line '{TOOL_PREFIX} name' to use one):\n"
            f"{self._tools.describe()}\nUser: {text}"
        )

    def _on_user(self, event: UserSaid) -> None:
        answer = self._llm.generate(self._prompt(event.text))
        spoken = []
        for line in answer.splitlines():
            if line.startswith(TOOL_PREFIX):
                self._tools.call(line[len(TOOL_PREFIX):].strip())
            else:
                spoken.append(line)
        self._bus.publish(Reply("\n".join(spoken).strip()))
