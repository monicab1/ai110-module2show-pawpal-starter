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
## Constraints Considered by the Scheduler

The scheduler considers several constraints when generating schedules and detecting conflicts:

- **Time (`time_str`)** – Tasks are sorted by their start time, and the scheduler compares task start and end times to detect scheduling overlaps.
- **Duration (`duration`)** – Duration is used with the start time to determine when a task ends, allowing the scheduler to detect overlapping tasks.
- **Due Date (`due_date`)** – Only tasks scheduled for the selected date (or tasks completed on that date through the recurring task logic) are included in the daily schedule.
- **Frequency (`daily` or `weekly`)** – The scheduler uses a task's frequency to automatically schedule its next occurrence after it has been completed.
- **Completion Status (`is_complete`)** – The scheduler tracks whether tasks are complete and allows users to filter schedules by completed or incomplete tasks.

## Which Constraints Matter Most?

The most important constraints are **time, duration, and due date** because they directly determine when tasks should be performed and whether scheduling conflicts occur.

- **Time and duration** are the highest priority because they determine task order and enable overlap detection.
- **Due date** ensures that only tasks relevant to the selected day are displayed.
- **Frequency** supports recurring tasks by scheduling the next occurrence after completion.
- **Completion status** is mainly used to track progress and filter the schedule rather than determine when tasks occur.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

## Scheduler Tradeoff

The scheduler checks for conflicts only between **consecutive tasks after sorting them by start time**, rather than comparing every task against every other task. This keeps the conflict detection logic simple and efficient, but it assumes the tasks are sorted correctly and only reports overlaps between neighboring tasks.

### Why This Tradeoff is reasonable?

**Advantages**
- Keeps the implementation simple and easy to understand.
- Efficient by sorting the tasks once and then checking each neighboring pair.
- Suitable for the lightweight conflict detection required by the project.

**Limitation**
- Relies on tasks being sorted correctly before checking for conflicts.
- Does not perform more advanced scheduling analysis or optimization beyond detecting overlaps between adjacent tasks.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

For brainstorming, I would show each assignment step to the Ai, then follow up the step with my interpretation of the assignment step and my plan for completing the step. I ask the AI 'what are your thoughts?' Based on the feedback I adapt my plan to what I agree with and ask the AI for clear, simple explanations for the things that I do not agree with.

For debugging, I prompted the AI to create tests. I ran the tests in my VS Code terminal. I also, did live testing via the Streamlit app UI.

- What kinds of prompts or questions were most helpful?

When something was generating the wrong output, I would tell it exactly what output I was seeing. When something was missing I would ask it did it actully implement what was discussed. If it said yes but, something was still missing, I would reattach the files and ask the Ai to read the current files again.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

When I fed the AI one of the assignment steps, it told me that I had not implemented the step. I knew I had already built that step, the only difference was that the step was completed using a different chat window.

- How did you evaluate or verify what the AI suggested?

Rather than simply allow the AI to create duplicate code, I went back and verified via the Streamlit app's UI output that I had indeed implemented that step.

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
