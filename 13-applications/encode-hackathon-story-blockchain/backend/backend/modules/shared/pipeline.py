from __future__ import annotations

from typing import Any, Protocol


class ProcessorStage(Protocol):
    name: str

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]: ...


class Pipeline:
    def __init__(self, stages: list[ProcessorStage]) -> None:
        self._stages = stages

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = payload
        for stage in self._stages:
            data = await stage.run(data)
        return data
