"""Simple repositories that provide deterministic fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class VideoRecord:
    video_id: str
    title: str
    characters: List[str]
    duration_seconds: int


@dataclass(frozen=True)
class CodeRecord:
    code_id: str
    language: str
    source: str


class VideoRepository:
    """Return a small set of representative mock videos."""

    _records: List[VideoRecord] = [
        VideoRecord(
            video_id="heritage-demo",
            title="Traditional Craft Demonstration",
            characters=["mentor", "apprentice"],
            duration_seconds=180,
        ),
        VideoRecord(
            video_id="education-session",
            title="Classroom Tutorial",
            characters=["teacher"],
            duration_seconds=240,
        ),
    ]

    def list(self) -> Iterable[VideoRecord]:
        return list(self._records)


class CodeRepository:
    """Return illustrative code samples used by the mock tests."""

    _records: List[CodeRecord] = [
        CodeRecord(
            code_id="bubble_sort",
            language="python",
            source="""def bubble_sort(values):
    n = len(values)
    for i in range(n):
        for j in range(0, n - i - 1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
    return values
""",
        ),
        CodeRecord(
            code_id="price_calculator",
            language="javascript",
            source="""function calculateTotal(items, discount){
    const subtotal = items.reduce((acc, item) => acc + item.price * item.qty, 0);
    const discounted = subtotal * (1 - discount);
    return +(discounted * 1.08).toFixed(2);
}
""",
        ),
    ]

    def list(self) -> Iterable[CodeRecord]:
        return list(self._records)
