from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time
from enum import Enum
from typing import Dict, List, Optional, Tuple


class PriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = ""
    duration_mins: int = 0
    priority: PriorityLevel = PriorityLevel.MEDIUM
    due_time: Optional[str] = None  # expected format HH:MM
    category: Optional[str] = None
    notes: Optional[str] = None
    frequency: Optional[str] = None
    completed: bool = False

    def estimate_end_time(self, start_time: time) -> time:
        start_datetime = datetime.combine(datetime.today(), start_time)
        end_datetime = start_datetime + timedelta(minutes=self.duration_mins)
        return end_datetime.time()

    def is_high_priority(self) -> bool:
        return self.priority == PriorityLevel.HIGH

    def mark_complete(self) -> None:
        self.completed = not self.completed

    def _due_time_tuple(self) -> Optional[Tuple[int, int]]:
        if not self.due_time:
            return None
        try:
            hour, minute = map(int, self.due_time.split(":"))
            return hour, minute
        except ValueError:
            return None


@dataclass
class Pet:
    name: str
    species: str
    age_years: Optional[int] = None
    preferences: Dict[str, str] = field(default_factory=dict)
    needs_medication: bool = False
    tasks: List[Task] = field(default_factory=list)

    def describe(self) -> str:
        age_text = f"{self.age_years} year(s) old" if self.age_years is not None else "age unknown"
        medication_text = " Needs medication." if self.needs_medication else ""
        return f"{self.name} is a {age_text} {self.species}.{medication_text}"

    def add_preference(self, key: str, value: str) -> None:
        self.preferences[key] = value

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int = 0
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)

    def update_availability(self, minutes: int) -> None:
        self.available_minutes_per_day = minutes

    def get_all_tasks(self) -> List[Task]:
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class ValidationResult:
    is_valid: bool
    warnings: List[str] = field(default_factory=list)


class DailyPlan:
    def __init__(self, tasks: Optional[List[Task]] = None) -> None:
        self.tasks: List[Task] = tasks or []
        self.reasoning: List[str] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def total_duration(self) -> int:
        return sum(task.duration_mins for task in self.tasks)

    def summarize(self) -> str:
        if not self.tasks:
            return "No tasks in the daily plan."

        lines = [
            f"{idx + 1}. {task.title} - {task.duration_mins} min - due {task.due_time or 'anytime'}"
            for idx, task in enumerate(self.tasks)
        ]
        lines.append(f"Total duration: {self.total_duration()} minutes")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner, pets: Optional[List[Pet]] = None, tasks: Optional[List[Task]] = None) -> None:
        self.owner = owner
        self.pets: List[Pet] = pets or []
        self.tasks: List[Task] = tasks or []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: uuid.UUID) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def validate_tasks(self) -> ValidationResult:
        warnings: List[str] = []
        tasks = self.owner.get_all_tasks()

        due_time_map: Dict[Tuple[int, int], List[Task]] = {}

        for task in tasks:
            if task.duration_mins <= 0:
                warnings.append(f"Task '{task.title}' has non-positive duration.")

            due_tuple = task._due_time_tuple()
            if task.due_time and due_tuple is None:
                warnings.append(f"Task '{task.title}' has invalid due_time format: '{task.due_time}'.")
            elif due_tuple is not None:
                due_time_map.setdefault(due_tuple, []).append(task)

        for due_tuple, matching_tasks in due_time_map.items():
            if len(matching_tasks) > 1:
                task_titles = ", ".join(task.title for task in matching_tasks)
                warnings.append(
                    f"Multiple tasks are scheduled at the same time {due_tuple[0]:02d}:{due_tuple[1]:02d}: {task_titles}."
                )

        total_duration = sum(task.duration_mins for task in tasks)
        if self.owner.available_minutes_per_day and total_duration > self.owner.available_minutes_per_day:
            warnings.append(
                f"Owner availability is {self.owner.available_minutes_per_day} minutes but tasks total {total_duration} minutes."
            )

        return ValidationResult(is_valid=len(warnings) == 0, warnings=warnings)

    def generate_recurring_tasks(self) -> List[Task]:
        recurring_tasks: List[Task] = []

        for task in self.owner.get_all_tasks():
            if task.frequency:
                generated_task = Task(
                    title=f"{task.title} ({task.frequency})",
                    duration_mins=task.duration_mins,
                    priority=task.priority,
                    due_time=task.due_time,
                    category=task.category,
                    notes=task.notes,
                    frequency=task.frequency,
                )
                recurring_tasks.append(generated_task)

        return recurring_tasks

    def get_daily_plan(self) -> DailyPlan:
        tasks = self.owner.get_all_tasks()
        sorted_tasks = sorted(
            tasks,
            key=lambda task: (
                task._due_time_tuple() is None,
                task._due_time_tuple() or (23, 59),
            ),
        )

        plan = DailyPlan(tasks=list(sorted_tasks))
        plan.reasoning = [
            f"Scheduled '{task.title}' at {task.due_time or 'no specific time'}."
            for task in sorted_tasks
        ]
        return plan

    def generate_daily_plan(self) -> DailyPlan:
        return self.get_daily_plan()

    def explain_plan(self, plan: DailyPlan) -> str:
        if not plan.tasks:
            return "No tasks to explain in the daily plan."

        lines = [
            f"{idx + 1}. {task.title} — due {task.due_time or 'anytime'}; duration {task.duration_mins} min"
            for idx, task in enumerate(plan.tasks)
        ]
        if plan.reasoning:
            lines.append("Reasoning:")
            lines.extend(plan.reasoning)
        return "\n".join(lines)
