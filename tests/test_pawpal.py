from datetime import date
from pawpal_system import Task, Pet


# ── Test 1: Task Completion ────────────────────────────────────────────────
def test_mark_complete_changes_status():
    """Calling mark_complete() should set is_complete to True."""
    task = Task(
        description="Morning walk",
        time_str="07:00",
        duration=30,
        frequency="daily",
        due_date=date.today(),
    )

    # Before: task should not be complete
    assert task.is_complete == False

    task.mark_complete()

    # After: task should now be complete
    assert task.is_complete == True


# ── Test 2: Task Addition ──────────────────────────────────────────────────
def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task list by 1."""
    pet = Pet(name="Buddy", species="Dog")

    # Before: pet should have no tasks
    assert len(pet.tasks) == 0

    pet.add_task(Task(
        description="Morning walk",
        time_str="07:00",
        duration=30,
        frequency="daily",
        due_date=date.today(),
    ))

    # After: pet should now have 1 task
    assert len(pet.tasks) == 1
