from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from typing import Dict, List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: Optional[str] = None
    notes: Optional[str] = None
    recurrence: Optional[str] = None

    def estimate_end_time(self, start_time: time) -> time:
        pass

    def is_high_priority(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age_years: Optional[int] = None
    preferences: Dict[str, str] = field(default_factory=dict)
    needs_medication: bool = False

    def describe(self) -> str:
        pass

    def add_preference(self, key: str, value: str) -> None:
        pass


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int = 0
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def update_availability(self, minutes: int) -> None:
        pass


class DailyPlan:
    def __init__(self, tasks: Optional[List[Task]] = None) -> None:
        self.tasks: List[Task] = tasks or []
        self.reasoning: List[str] = []

    def add_task(self, task: Task) -> None:
        pass

    def total_duration(self) -> int:
        pass

    def summarize(self) -> str:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: Optional[List[Task]] = None) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks: List[Task] = tasks or []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass

    def validate_tasks(self) -> bool:
        pass

    def generate_daily_plan(self) -> DailyPlan:
        pass

    def explain_plan(self, plan: DailyPlan) -> str:
        pass
