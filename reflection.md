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

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
