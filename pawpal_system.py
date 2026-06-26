from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    description: str
    time_str: str
    duration: int
    frequency: str
    due_date: date
    is_complete: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    breed: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def edit_task(self, index: int, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pet(self, name: str):
        pass


class Scheduler:

    @staticmethod
    def generate_daily_plan(pet: Pet, target_date: date):
        pass

    @staticmethod
    def detect_overlaps(tasks: list) -> list:
        pass