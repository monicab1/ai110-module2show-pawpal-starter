# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output - CLI
```python
==================================================
  🐾  PawPal — Today's Schedule  (2026-06-27)
  Owner: Alex Johnson
==================================================

  [DOG] Buddy
  ----------------------------------------
    #1  07:00 — Morning walk (30 min)
    #2  07:45 — Breakfast / medication (10 min)
    #3  18:00 — Evening walk (45 min)

  [CAT] Whiskers
  ----------------------------------------
    #1  07:20 — Brush fur (15 min)
    #2  09:00 — Playtime (20 min)
    #3  17:30 — Evening feeding (10 min)

==================================================
  🐾  Full Schedule — All Pets Combined
==================================================
    #1  07:00 — [Buddy] Morning walk (30 min)
    #2  07:20 — [Whiskers] Brush fur (15 min)
    #3  07:45 — [Buddy] Breakfast / medication (10 min)
    #4  09:00 — [Whiskers] Playtime (20 min)
    #5  17:30 — [Whiskers] Evening feeding (10 min)
    #6  18:00 — [Buddy] Evening walk (45 min)

    ⚠️  [CROSS-PET OVERLAP] Buddy's 'Morning walk' overlaps with Whiskers's 'Brush fur'.

==================================================
  ✅  Verification Checks
==================================================

  [1] Pets represented in full plan: Whiskers, Buddy
      → Spans multiple pets: PASS

  [2] Task times in order: 07:00, 07:20, 07:45, 09:00, 17:30, 18:00
      → Correctly sorted:   PASS

  [3] Cross-pet overlaps detected: 1
      → Overlap detection:  PASS

==================================================
```

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🖥️ Sample Output - Streamlit



## 🧪 Testing PawPal+
## Test Coverage Summary

These tests verify the core functionality of the PawPal scheduling system.

They ensure that:
- Tasks can be added to pets correctly
- Tasks can be marked complete with proper recurrence behavior
- Tasks are returned in chronological order
- The scheduler detects overlapping tasks

The suite also checks that conflict detection returns warnings
without crashing the program.

Together, the tests validate:
- Basic task management (add and complete tasks)
- Scheduling behavior (sorting and recurrence)
- Conflict detection across tasks

System Reliability **Confidence Level:** ★ ★ ★ ★ ★

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
#========================================= test session starts =========================================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Swe4me\Documents\Codepath_PawPal+\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 5 items                                                                                      

tests\test_pawpal.py .....                                                                       [100%]

========================================== 5 passed in 0.08s ==========================================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
