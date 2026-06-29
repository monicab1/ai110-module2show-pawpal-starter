from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """Represents a single care task assigned to a pet."""

    description: str
    time_str: str
    duration: int
    frequency: str
    due_date: date
    is_complete: bool = False
    _original_due_date: date = field(default=None, init=False, repr=False)

    def __post_init__(self):
        self._original_due_date = self.due_date

    def mark_task_complete(self) -> None:
        """Mark the task complete and automatically schedule the next occurrence.

        This is the recurring task mechanism. Rather than creating a new Task
        instance (which would cause duplicate entries in the same session),
        we advance the due date forward using timedelta so the task
        automatically reappears on the correct next occurrence:
          - Daily tasks: due_date + 1 day  (timedelta(days=1))
          - Weekly tasks: due_date + 7 days (timedelta(days=7))
        The task is marked complete for today and becomes incomplete again
        on its next due date, satisfying the recurring task requirement.
        """
        if self.frequency.lower() == "daily":
            self.due_date = self.due_date + timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            self.due_date = self.due_date + timedelta(days=7)
        self.is_complete = True

    def undo_complete(self, today: date) -> None:
        """Reverse mark_task_complete: restore is_complete and due date."""
        self.is_complete = False
        self.due_date = today


@dataclass
class Pet:
    """Represents a pet belonging to an owner, with a list of care tasks."""

    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a new task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, index: int) -> None:
        """Remove a task from this pet's task list by index."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]


@dataclass
class Owner:
    """Represents a pet owner who manages one or more pets."""

    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_pet(self, name: str):
        """Return a pet by name (case-insensitive), or None if not found."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None


class Scheduler:
    """Provides scheduling and conflict-detection logic across pets and tasks."""

    @staticmethod
    def generate_daily_plan(pet: Pet, target_date: date):
        """Return a sorted task list and overlap warnings for a single pet on a given date."""
        todays_tasks = [
            t for t in pet.tasks
            if t.is_complete or t.due_date == target_date
        ]
        todays_tasks = [
            t for t in pet.tasks
            if t.due_date == target_date or t.is_complete
        ]
        # Only show tasks that belong to today (either still due today or completed today)
        todays_tasks = [
            t for t in pet.tasks
            if (t.due_date == target_date) or
               (t.is_complete and (t.due_date - timedelta(days=1) == target_date
                or t.due_date - timedelta(days=7) == target_date))
        ]
        todays_tasks.sort(key=lambda t: t.time_str)
        warnings = Scheduler.detect_overlaps(todays_tasks)
        plan_output = []
        for i, task in enumerate(todays_tasks, start=1):
            status = "✅" if task.is_complete else "⬜"
            line = (f"{status} #{i}  {task.time_str} — {task.description} "
                    f"({task.duration} min)")
            plan_output.append(line)
        return plan_output, warnings

    @staticmethod
    def generate_full_plan(owner, target_date: date):
        """Aggregate and sort all tasks across every pet the owner has."""
        all_tasks = []
        for pet in owner.pets:
            for task in pet.tasks:
                # Include tasks due today OR completed tasks whose original slot was today
                is_today = task.due_date == target_date
                was_today = task.is_complete and (
                    task.due_date - timedelta(days=1) == target_date or
                    task.due_date - timedelta(days=7) == target_date
                )
                if is_today or was_today:
                    all_tasks.append((pet, task))

        all_tasks.sort(key=lambda pt: pt[1].time_str)

        cross_warnings = []
        for i in range(1, len(all_tasks)):
            prev_pet, prev_task = all_tasks[i - 1]
            curr_pet, curr_task = all_tasks[i]
            ph, pm = map(int, prev_task.time_str.split(":"))
            ch, cm = map(int, curr_task.time_str.split(":"))
            prev_end = ph * 60 + pm + prev_task.duration
            curr_start = ch * 60 + cm
            if prev_end > curr_start and prev_pet != curr_pet:
                cross_warnings.append(
                    f"[CROSS-PET OVERLAP] {prev_pet.name}'s "
                    f"'{prev_task.description}' overlaps with "
                    f"{curr_pet.name}'s '{curr_task.description}'."
                )

        plan_output = []
        for i, (pet, task) in enumerate(all_tasks, start=1):
            status = "✅" if task.is_complete else "⬜"
            line = (f"{status} #{i}  {task.time_str} — [{pet.name}] {task.description} "
                    f"({task.duration} min)")
            plan_output.append(line)

        return plan_output, cross_warnings

    @staticmethod
    def filter_tasks(tasks: list, status: str = None) -> list:
        """Filter a list of tasks by completion status.
        status: 'complete', 'incomplete', or None (returns all).
        """
        if status == "complete":
            return [t for t in tasks if t.is_complete]
        elif status == "incomplete":
            return [t for t in tasks if not t.is_complete]
        return tasks

    @staticmethod
    def detect_overlaps(tasks: list) -> list:
        """Detect and return a list of time overlap warnings within a single pet's task list."""
        warnings = []
        for i in range(1, len(tasks)):
            prev = tasks[i - 1]
            curr = tasks[i]
            ph, pm = map(int, prev.time_str.split(":"))
            ch, cm = map(int, curr.time_str.split(":"))
            prev_end = ph * 60 + pm + prev.duration
            curr_start = ch * 60 + cm
            if prev_end > curr_start:
                warnings.append(
                    f"[OVERLAP] '{prev.description}' and "
                    f"'{curr.description}' overlap."
                )
        return warnings
