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
    due_date: Optional[str] = None  # expected format YYYY-MM-DD
    category: Optional[str] = None
    notes: Optional[str] = None
    frequency: Optional[str] = None
    completed: bool = False

    def estimate_end_time(self, start_time: time) -> time:
        """Return the end time after adding the task duration to a start time."""
        start_datetime = datetime.combine(datetime.today(), start_time)
        end_datetime = start_datetime + timedelta(minutes=self.duration_mins)
        return end_datetime.time()

    def is_high_priority(self) -> bool:
        """Return True when the task priority is high."""
        return self.priority == PriorityLevel.HIGH

    def mark_complete(self) -> None:
        """Toggle the task completion status."""
        self.completed = not self.completed

    def due_time_sort_key(self) -> str:
        """Return a sort key for due time strings in HH:MM format."""
        return self.due_time or "23:59"

    def due_date_sort_key(self) -> Tuple[str, str]:
        """Return a sort key for due date and time.

        Tasks without a due date are sorted after dated tasks.
        """
        return (self.due_date or "9999-12-31", self.due_time_sort_key())

    def _due_time_tuple(self) -> Optional[Tuple[int, int]]:
        """Return the due time as an (hour, minute) tuple if valid."""
        if not self.due_time:
            return None
        try:
            hour, minute = map(int, self.due_time.split(":"))
            return hour, minute
        except ValueError:
            return None

    def _due_date(self) -> Optional[datetime.date]:
        """Return the due date as a date object if valid."""
        if not self.due_date:
            return None
        try:
            return datetime.strptime(self.due_date, "%Y-%m-%d").date()
        except ValueError:
            return None

    def _next_occurrence_date(self) -> Optional[datetime.date]:
        """Compute the next occurrence date for recurring tasks."""
        if self.frequency not in {"daily", "weekly"}:
            return None

        current_date = self._due_date() or datetime.today().date()
        if self.frequency == "daily":
            return current_date + timedelta(days=1)
        if self.frequency == "weekly":
            return current_date + timedelta(days=7)
        return None

    def _next_occurrence(self) -> Optional["Task"]:
        """Create a fresh task instance for the next recurring occurrence.

        The returned task preserves the original task details and advances the
        due date by the interval implied by `frequency`.
        """
        next_date = self._next_occurrence_date()
        if not next_date or not self.due_time:
            return None

        return Task(
            title=self.title,
            duration_mins=self.duration_mins,
            priority=self.priority,
            due_time=self.due_time,
            due_date=next_date.isoformat(),
            category=self.category,
            notes=self.notes,
            frequency=self.frequency,
        )

    def mark_complete(self) -> Optional["Task"]:
        """Toggle the task completion status and return a next occurrence for recurring tasks."""
        self.completed = not self.completed
        if self.completed:
            return self._next_occurrence()
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
        """Return a short description of the pet."""
        age_text = f"{self.age_years} year(s) old" if self.age_years is not None else "age unknown"
        medication_text = " Needs medication." if self.needs_medication else ""
        return f"{self.name} is a {age_text} {self.species}.{medication_text}"

    def add_preference(self, key: str, value: str) -> None:
        """Store a pet preference key and value."""
        self.preferences[key] = value

    def add_task(self, task: Task) -> None:
        """Append a task to the pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int = 0
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household if not already present."""
        if pet not in self.pets:
            self.pets.append(pet)

    def update_availability(self, minutes: int) -> None:
        """Update the owner's available minutes per day."""
        self.available_minutes_per_day = minutes

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks belonging to every pet in the household."""
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
        """Add a task to the daily plan."""
        self.tasks.append(task)

    def total_duration(self) -> int:
        """Return the total duration of all tasks in the plan."""
        return sum(task.duration_mins for task in self.tasks)

    def summarize(self) -> str:
        """Return a short text summary of the plan and its tasks."""
        if not self.tasks:
            return "No tasks in the daily plan."

        lines = []
        for idx, task in enumerate(self.tasks):
            due_parts = [task.due_time or "anytime"]
            if task.due_date:
                due_parts.append(task.due_date)
            due_text = " on ".join(due_parts) if len(due_parts) > 1 else due_parts[0]
            lines.append(
                f"{idx + 1}. {task.title} - {task.duration_mins} min - due {due_text}"
            )

        lines.append(f"Total duration: {self.total_duration()} minutes")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner, pets: Optional[List[Pet]] = None, tasks: Optional[List[Task]] = None) -> None:
        self.owner = owner
        self.pets: List[Pet] = pets or []
        self.tasks: List[Task] = tasks or []

    def add_task(self, task: Task) -> None:
        """Add a local task to the scheduler's task list."""
        self.tasks.append(task)

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        if pet_name is not None:
            tasks: List[Task] = []
            for pet in self.owner.pets:
                if pet.name.lower() == pet_name.lower():
                    tasks.extend(pet.tasks)
        else:
            tasks = self.owner.get_all_tasks()

        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        return tasks

    def sort_tasks_by_due_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by due date and due time.

        Tasks without a due date or time are ordered after those with explicit scheduling.
        """
        tasks = tasks if tasks is not None else self.owner.get_all_tasks()
        return sorted(tasks, key=lambda task: task.due_date_sort_key())

    def complete_task(self, task_id: uuid.UUID) -> Optional[Task]:
        """Mark a task complete and append its next recurring occurrence.

        If the completed task has a valid `frequency` of `daily` or `weekly`, this
        returns a new task instance for the next due date.
        """
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.id == task_id:
                    next_task = task.mark_complete()
                    if next_task:
                        pet.tasks.append(next_task)
                    return next_task
        return None

    def remove_task(self, task_id: uuid.UUID) -> None:
        """Remove a task from the scheduler by its unique ID."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def detect_conflicts(self) -> List[str]:
        """Return lightweight warnings for tasks scheduled at the same exact slot.

        This method reports warnings rather than raising errors, so the app can
        continue running while still alerting the user to scheduling conflicts.
        """
        warnings: List[str] = []
        conflict_map: Dict[Tuple[str, Tuple[int, int]], List[Task]] = {}

        for task in self.owner.get_all_tasks():
            due_tuple = task._due_time_tuple()
            if task.due_time and due_tuple is None:
                continue

            slot_key = (task.due_date or "", due_tuple or (-1, -1))
            conflict_map.setdefault(slot_key, []).append(task)

        for (due_date, due_tuple), matching_tasks in conflict_map.items():
            if len(matching_tasks) > 1:
                task_titles = ", ".join(f"{task.title} ({task.category or 'task'})" for task in matching_tasks)
                date_text = f" on {due_date}" if due_date else ""
                warnings.append(
                    f"Conflict: multiple tasks are scheduled at the same time {due_tuple[0]:02d}:{due_tuple[1]:02d}{date_text}: {task_titles}."
                )

        return warnings

    def validate_tasks(self) -> ValidationResult:
        """Validate all household tasks and return any warnings."""
        warnings: List[str] = []
        tasks = self.owner.get_all_tasks()

        for task in tasks:
            if task.duration_mins <= 0:
                warnings.append(f"Task '{task.title}' has non-positive duration.")

            if task.due_time:
                due_tuple = task._due_time_tuple()
                if due_tuple is None:
                    warnings.append(f"Task '{task.title}' has invalid due_time format: '{task.due_time}'.")

        warnings.extend(self.detect_conflicts())

        total_duration = sum(task.duration_mins for task in tasks)
        if self.owner.available_minutes_per_day and total_duration > self.owner.available_minutes_per_day:
            warnings.append(
                f"Owner availability is {self.owner.available_minutes_per_day} minutes but tasks total {total_duration} minutes."
            )

        return ValidationResult(is_valid=len(warnings) == 0, warnings=warnings)

    def generate_recurring_tasks(self) -> List[Task]:
        """Generate additional tasks for each recurring task in the household."""
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
        """Return a daily plan of all household tasks sorted by due time."""
        tasks = self.owner.get_all_tasks()
        sorted_tasks = self.sort_tasks_by_due_time(tasks)

        plan = DailyPlan(tasks=list(sorted_tasks))
        plan.reasoning = [
            f"Scheduled '{task.title}' at {task.due_time or 'no specific time'}."
            for task in sorted_tasks
        ]
        return plan

    def generate_daily_plan(self) -> DailyPlan:
        """Generate and return today's plan by delegating to get_daily_plan."""
        return self.get_daily_plan()

    def explain_plan(self, plan: DailyPlan) -> str:
        """Return a text explanation of the given daily plan."""
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
