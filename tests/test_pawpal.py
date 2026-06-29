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

    task.mark_task_complete()

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




from datetime import date, timedelta

from pawpal_system import Pet, Task, Scheduler


def test_tasks_are_sorted_chronologically():
    """Verify tasks are returned in chronological order."""
    today = date.today()
    pet = Pet(name="Buddy", species="Dog")

    # Add tasks out of order
    pet.add_task(Task("Evening walk", "18:00", 30, "daily", today))
    pet.add_task(Task("Morning walk", "07:30", 30, "daily", today))
    pet.add_task(Task("Lunch", "12:00", 15, "daily", today))

    plan, warnings = Scheduler.generate_daily_plan(pet, today)

    assert len(plan) == 3
    assert "07:30" in plan[0]
    assert "12:00" in plan[1]
    assert "18:00" in plan[2]
    assert warnings == []


def test_daily_task_recurrence():
    """Verify a daily task advances to the next day when completed."""
    today = date.today()

    task = Task(
        description="Morning walk",
        time_str="07:00",
        duration=30,
        frequency="daily",
        due_date=today,
    )

    task.mark_task_complete()

    assert task.is_complete is True
    assert task.due_date == today + timedelta(days=1)


def test_conflict_detection():
    """Verify overlapping tasks generate a warning."""
    today = date.today()
    pet = Pet(name="Buddy", species="Dog")

    # Two tasks with the same start time
    pet.add_task(Task("Morning walk", "07:00", 30, "daily", today))
    pet.add_task(Task("Breakfast", "07:00", 10, "daily", today))

    plan, warnings = Scheduler.generate_daily_plan(pet, today)

    assert len(plan) == 2
    assert len(warnings) == 1
    assert "[OVERLAP]" in warnings[0]
