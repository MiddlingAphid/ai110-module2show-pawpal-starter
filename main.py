from datetime import datetime
from pawpal_system import Owner, Pet, Task, PriorityLevel, Scheduler


def main() -> None:
    owner = Owner(name="Jordan", available_minutes_per_day=180)

    pet1 = Pet(name="Mochi", species="dog", age_years=4, needs_medication=False)
    pet2 = Pet(name="Luna", species="cat", age_years=2, needs_medication=True)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(
        title="Morning walk",
        duration_mins=30,
        priority=PriorityLevel.HIGH,
        due_time="08:00",
        category="exercise",
        notes="Walk around the block",
    )

    task2 = Task(
        title="Feed breakfast",
        duration_mins=15,
        priority=PriorityLevel.MEDIUM,
        due_time="08:30",
        category="feeding",
        notes="Dry food and water",
    )

    task3 = Task(
        title="Give medication",
        duration_mins=10,
        priority=PriorityLevel.HIGH,
        due_time="09:00",
        category="health",
        notes="Luna's daily dose",
        frequency="daily",
        due_date=datetime.today().date().isoformat(),
    )

    task4 = Task(
        title="Refill water bowl",
        duration_mins=5,
        priority=PriorityLevel.LOW,
        due_time="07:45",
        category="feeding",
        notes="Fresh water for both pets",
    )

    task5 = Task(
        title="Vet check-in",
        duration_mins=10,
        priority=PriorityLevel.MEDIUM,
        due_time="08:00",
        category="health",
        notes="Call vet with updates",
    )

    pet1.add_task(task2)
    pet1.add_task(task4)
    pet2.add_task(task3)
    pet2.add_task(task5)
    pet1.add_task(task1)

    scheduler = Scheduler(owner=owner, pets=[pet1, pet2])
    next_task = scheduler.complete_task(task3.id)

    if next_task:
        print(f"Created next occurrence: {next_task.title} due {next_task.due_time} on {next_task.due_date}")

    validation = scheduler.validate_tasks()
    if validation.warnings:
        print("Schedule warnings:")
        for warning in validation.warnings:
            print(f"- {warning}")
        print()

    daily_plan = scheduler.get_daily_plan()

    print("Today's Schedule")
    print("-----------------")
    print(daily_plan.summarize())
    print()

    sorted_tasks = scheduler.sort_tasks_by_due_time()
    print("Sorted tasks by due time:")
    for task in sorted_tasks:
        print(f"- {task.title} @ {task.due_time} ({'completed' if task.completed else 'pending'})")
    print()

    mochis_tasks = scheduler.filter_tasks(pet_name="Mochi")
    print("Mochi's tasks:")
    for task in mochis_tasks:
        print(f"- {task.title} @ {task.due_time} ({'completed' if task.completed else 'pending'})")
    print()

    incomplete_tasks = scheduler.filter_tasks(completed=False)
    print("Incomplete tasks:")
    for task in incomplete_tasks:
        print(f"- {task.title} @ {task.due_time} (pet: {task.category})")


if __name__ == "__main__":
    main()
