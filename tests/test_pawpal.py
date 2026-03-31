from pawpal_system import Pet, Task, PriorityLevel


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
