from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    time_str: str
    duration: int
    frequency: str
    due_date: date
    is_complete: bool = False

    def mark_complete(self) -> None:
        if self.frequency.lower() == "daily":
            self.due_date = self.due_date + timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            self.due_date = self.due_date + timedelta(days=7)
        self.is_complete = False


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def edit_task(self, index: int) -> None:
        if 0 <= index < len(self.tasks):
            del self.tasks[index]


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_pet(self, name: str):
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None


class Scheduler:

    @staticmethod
    def generate_daily_plan(pet: Pet, target_date: date):
        todays_tasks = [t for t in pet.tasks if t.due_date == target_date]
        todays_tasks.sort(key=lambda t: t.time_str)
        warnings = Scheduler.detect_overlaps(todays_tasks)
        plan_output = []
        for i, task in enumerate(todays_tasks, start=1):
            line = (f"#{i}  {task.time_str} — {task.description} "
                    f"({task.duration} min)")
            plan_output.append(line)
        return plan_output, warnings

    @staticmethod
    def detect_overlaps(tasks: list) -> list:
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