# PawPal+ Project Reflection

## 1. System Design

I chose these three core user actions because **they form a natural pipeline that touches every class**, which is exactly the structure of the four classes (Owner → Pet → Task → Scheduler). In practice, the flow looks like: *Create the pet → give it tasks → let the scheduler turn those tasks into a plan.*  

By identifying these actions early, the rest of the project becomes much cleaner — especially the UML — because each action maps directly onto a class responsibility. That means the write‑up, the class design, and the final behavior of the app all stay aligned.

---

### Three core user actions

### 1. Add a pet (with owner info)  
The user enters their own details and creates a pet profile (name, breed, etc.).

**Maps to:** Owner manages a list of Pets.  
**Why it's core:** Nothing else can happen until there's a pet to care for — it's the entry point.

---

### 2. Add or edit a care task for a pet  
The user adds a task like “Morning walk” with, at minimum, a duration and a priority (and optionally frequency: daily/weekly).

**Maps to:** Pet holds a list of Tasks; each Task stores description, duration, priority, frequency, completion status.  
**Why it's core:** These tasks are the raw material the scheduler organizes. The rubric explicitly requires duration + priority.

---

### 3. Generate and view today's daily plan  
The user clicks something like “Build today's plan,” and the app produces a prioritized, time‑ordered schedule (and ideally explains why it ordered things that way).

**Maps to:** Scheduler — the “brain” that sorts by priority/duration, filters out tasks when time runs out, and handles conflicts.  
**Why it's core:** This is the whole point of the app — turning a pile of tasks + constraints into the sample output (08:00 — Morning walk (30 min) [priority: high]).

---
 
Together, these three actions naturally flow into one another and ensure that every class is used in the way it was designed. Because **they form a natural pipeline that touches every class**, the UML diagram ends up clean, consistent, and easy to justify — each class has a clear purpose, and each user action directly activates that purpose.

---

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Here's a write-up for section 1a that you can use directly:

---

## 1a. Initial Design

PawPal+ is built around four classes, each with a distinct responsibility that maps directly to one stage of the pet care pipeline.

---

**Owner**
The Owner class is the entry point of the system. It stores the owner's name and maintains a list of all their pets. Its responsibility is simply to hold and provide access to Pet objects. Nothing else in the system runs until an Owner exists with at least one Pet attached.

---

**Pet**
The Pet class is a container for a single animal's profile and care tasks. It stores the pet's name and breed, and it maintains the list of Task objects that belong to that pet. It is responsible for accepting new tasks and allowing existing tasks to be edited. Pet acts as the bridge between the Owner above it and the Tasks below it.

---

**Task**
The Task class represents a single care activity such as a morning walk, feeding, or medication. It stores everything needed to describe and schedule that activity — what it is, when it starts, how long it takes, how often it repeats, and whether it has been completed. Its one behavior is `mark_complete()`, which automatically advances the due date forward by the correct number of days based on frequency, so the task reappears on its own without the user having to re-enter it.

---

**Scheduler**
The Scheduler is the brain of the system. Unlike the other three classes it holds no data of its own — it is pure logic. It takes a Pet and a target date, filters that pet's tasks down to only those due on that date, sorts them by scheduled time, checks for conflicts where one task's duration would overlap another task's start time, and returns a formatted daily plan along with any warnings. Every other class exists to feed the Scheduler clean, well-structured data so it can do this job correctly.

---

This four-class design was chosen because it forms a natural pipeline: Owner → Pet → Task → Scheduler. Each class has one clear responsibility and the system flows in one direction, which keeps the logic easy to follow and easy to test.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
1. Rename breed to species in Pet

Reflects that the dropdown will offer Dog, Cat, Bird, Fish, Other.

Label it "Pet Type" in the Streamlit UI.

2. Revert edit_task() to delete only
pythondef edit_task(self, index: int) -> None:
    if 0 <= index < len(self.tasks):
        del self.tasks[index]

3. Remove priority entirely

It is a stretch feature. Removed from Task attributes and removed as a sort key in Scheduler.

4. Remove priority_rank() from Task

No priority means no need for this method. Safe to remove.

5. Remove filter_by_time_budget() from Scheduler

No time budget constraint means this method has no job. Safe to remove.

6. Remove available_minutes parameter from generate_daily_plan()

Was tied to the time budget feature. Safe to remove.

7. Remove get_tasks_for_date() from Pet

Date filtering belongs to Scheduler only. Keeps Pet as a pure data container.

8. Dropdowns handle all input validation

Eliminates the need for .strip().lower() defensive coding and any fallback handling for unexpected values.

9. mark_complete() filled in (not a stub)

This one had to be real from the start since the whole recurring task system depends on it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
