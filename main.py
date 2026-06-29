from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# ── Setup ──────────────────────────────────────────────────────────────────
owner = Owner(name="Alex Johnson")

buddy    = Pet(name="Buddy",    species="Dog")
whiskers = Pet(name="Whiskers", species="Cat")

owner.add_pet(buddy)
owner.add_pet(whiskers)

today = date.today()

# ── Tasks for Buddy (Dog) ──────────────────────────────────────────────────
buddy.add_task(Task(
    description="Morning walk",
    time_str="07:00",
    duration=30,
    frequency="daily",
    due_date=today,
))
buddy.add_task(Task(
    description="Breakfast / medication",
    time_str="07:45",
    duration=10,
    frequency="daily",
    due_date=today,
))
buddy.add_task(Task(
    description="Evening walk",
    time_str="18:00",
    duration=45,
    frequency="daily",
    due_date=today,
))

# ── Tasks for Whiskers (Cat) ───────────────────────────────────────────────
whiskers.add_task(Task(
    description="Brush fur",
    time_str="07:20",       # intentional cross-pet overlap with Buddy's walk
    duration=15,
    frequency="weekly",
    due_date=today,
))
whiskers.add_task(Task(
    description="Playtime",
    time_str="09:00",
    duration=20,
    frequency="daily",
    due_date=today,
))
whiskers.add_task(Task(
    description="Evening feeding",
    time_str="17:30",
    duration=10,
    frequency="daily",
    due_date=today,
))

# ── Section 1: Per-Pet Schedule ────────────────────────────────────────────
print("=" * 50)
print(f"  🐾  PawPal — Today's Schedule  ({today})")
print(f"  Owner: {owner.name}")
print("=" * 50)

for pet in owner.pets:
    plan, warnings = Scheduler.generate_daily_plan(pet, today)

    print(f"\n  [{pet.species.upper()}] {pet.name}")
    print("  " + "-" * 40)

    if plan:
        for line in plan:
            print(f"    {line}")
    else:
        print("    No tasks scheduled for today.")

    if warnings:
        print()
        for w in warnings:
            print(f"    ⚠️  {w}")

# ── Section 2: Full Cross-Pet Plan ─────────────────────────────────────────
print("\n" + "=" * 50)
print("  🐾  Full Schedule — All Pets Combined")
print("=" * 50)

full_plan, cross_warnings = Scheduler.generate_full_plan(owner, today)

for line in full_plan:
    print(f"    {line}")

if cross_warnings:
    print()
    for w in cross_warnings:
        print(f"    ⚠️  {w}")

# ── Section 3: Verification Checks ─────────────────────────────────────────
print("\n" + "=" * 50)
print("  ✅  Verification Checks")
print("=" * 50)

# Check 1: Full plan spans more than one pet
pet_names_in_plan = set()
for pet in owner.pets:
    for task in pet.tasks:
        if task.due_date == today:
            pet_names_in_plan.add(pet.name)

print(f"\n  [1] Pets represented in full plan: {', '.join(pet_names_in_plan)}")
print(f"      → Spans multiple pets: {'PASS' if len(pet_names_in_plan) > 1 else 'FAIL'}")

# Check 2: Tasks are sorted across all pets by time
times = [line.split("  ")[1].split(" ")[0] for line in full_plan]
print(f"\n  [2] Task times in order: {', '.join(times)}")
print(f"      → Correctly sorted:   {'PASS' if times == sorted(times) else 'FAIL'}")

# Check 3: Cross-pet overlap was detected
print(f"\n  [3] Cross-pet overlaps detected: {len(cross_warnings)}")
print(f"      → Overlap detection:  {'PASS' if cross_warnings else 'FAIL (no overlaps found)'}")

print("\n" + "=" * 50)

# ── Section 4: Filter Demo ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("  🔍  Filter Demo")
print("=" * 50)

# Mark one task complete for demo purposes
buddy.tasks[0].mark_complete()

# Gather all of today's tasks across both pets
all_todays_tasks = []
for pet in owner.pets:
    for task in pet.tasks:
        if task.due_date == today or (
            task.is_complete and (
                task.due_date - __import__('datetime').timedelta(days=1) == today or
                task.due_date - __import__('datetime').timedelta(days=7) == today
            )
        ):
            all_todays_tasks.append(task)

# Filter: incomplete only
incomplete = Scheduler.filter_tasks(all_todays_tasks, status="incomplete")
print(f"\n  Incomplete tasks ({len(incomplete)}):")
for t in incomplete:
    print(f"    ⬜  {t.time_str} — {t.description}")

# Filter: complete only
complete = Scheduler.filter_tasks(all_todays_tasks, status="complete")
print(f"\n  Completed tasks ({len(complete)}):")
for t in complete:
    print(f"    ✅  {t.time_str} — {t.description}")

# Filter: all
all_tasks = Scheduler.filter_tasks(all_todays_tasks)
print(f"\n  All tasks ({len(all_tasks)}):")
for t in all_tasks:
    marker = "✅" if t.is_complete else "⬜"
    print(f"    {marker}  {t.time_str} — {t.description}")

print("\n" + "=" * 50)
