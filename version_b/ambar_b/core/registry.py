"""Registries that let the core discover devices and tools without knowing them."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class DeviceRegistry:
    _devices: dict[str, set[str]] = field(default_factory=dict)

    def register(self, device_id: str, capabilities: set[str]) -> None:
        self._devices[device_id] = set(capabilities)

    def with_capability(self, capability: str) -> list[str]:
        return sorted(d for d, caps in self._devices.items() if capability in caps)


@dataclass
class Tool:
    name: str
    description: str
    run: Callable[[], None]


class ToolRegistry:
    """Actions the language model is allowed to trigger."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, description: str, run: Callable[[], None]) -> None:
        self._tools[name] = Tool(name, description, run)

    def call(self, name: str) -> bool:
        tool = self._tools.get(name)
        if tool is None:
            return False
        tool.run()
        return True

    def describe(self) -> str:
        return "\n".join(f"- {t.name}: {t.description}" for t in self._tools.values())
