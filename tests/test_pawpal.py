from pawpal_system import Owner, Pet, Scheduler, Task, PriorityLevel


def test_task_mark_complete_toggles_status() -> None:
    task = Task(
        title="Feed lunch",
        duration_mins=15,
        priority=PriorityLevel.MEDIUM,
        due_time="12:00",
    )

    assert task.completed is False

    task.mark_complete()
    assert task.completed is True

    task.mark_complete()
    assert task.completed is False


def test_pet_add_task_increases_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.tasks)

    task = Task(
        title="Afternoon walk",
        duration_mins=20,
        priority=PriorityLevel.HIGH,
        due_time="15:00",
    )

    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1
    assert pet.tasks[0] is task


def test_sort_tasks_by_due_date_and_time_returns_chronological_order() -> None:
    owner = Owner(name="Aria")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task_early = Task(
        title="Morning walk",
        duration_mins=20,
        due_date="2025-10-01",
        due_time="08:00",
    )
    task_late = Task(
        title="Breakfast",
        duration_mins=15,
        due_date="2025-10-01",
        due_time="09:00",
    )
    task_next_day = Task(
        title="Vet check",
        duration_mins=30,
        due_date="2025-10-02",
        due_time="07:00",
    )

    pet.add_task(task_late)
    pet.add_task(task_next_day)
    pet.add_task(task_early)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_tasks_by_due_time()

    assert sorted_tasks == [task_early, task_late, task_next_day]


def test_complete_daily_task_creates_next_day_occurrence() -> None:
    owner = Owner(name="Aria")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task = Task(
        title="Feed breakfast",
        duration_mins=15,
        due_date="2025-10-01",
        due_time="08:00",
        frequency="daily",
    )
    pet.add_task(task)

    scheduler = Scheduler(owner=owner)
    next_task = scheduler.complete_task(task.id)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == "2025-10-02"
    assert next_task.due_time == task.due_time
    assert next_task.frequency == task.frequency
    assert next_task.title == task.title
    assert next_task in pet.tasks


def test_detect_conflicts_flags_duplicate_task_times() -> None:
    owner = Owner(name="Aria")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task_a = Task(
        title="Morning meds",
        duration_mins=10,
        due_date="2025-10-01",
        due_time="08:00",
    )
    task_b = Task(
        title="Breakfast",
        duration_mins=15,
        due_date="2025-10-01",
        due_time="08:00",
    )
    pet.add_task(task_a)
    pet.add_task(task_b)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "2025-10-01" in warnings[0]
    assert "Morning meds" in warnings[0]
    assert "Breakfast" in warnings[0]
