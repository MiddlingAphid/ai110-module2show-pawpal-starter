# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

The initial UML design for PawPal+ follows a hierarchical structure where an Owner manages a collection of Pet objects, each containing its own specific Task routines. A central Scheduler class acts as the system's engine, processing these entities to generate a DailyPlan that organizes activities by time and priority.

- What classes did you include, and what responsibilities did you assign to each?

The initial design of the PawPal+ system centers on five primary classes: Task, Pet, Owner, DailyPlan, and Scheduler. The Task class functions as a dataclass to store specific activity details like title, duration, and priority, while the Pet and Owner classes manage individual animal profiles and overall user availability, respectively. To handle the system's "intelligence," the Scheduler acts as the core engine that processes these inputs to generate a DailyPlan, which is responsible for organizing the final schedule and providing the specific reasoning behind the task order.

**b. Design changes**

- Did your design change during implementation?

Yes, my design evolved significantly as I moved from the initial concept to the actual implementation.

- If yes, describe at least one change and why you made it.

One major change I made was shifting the Scheduler from handling a single pet to managing a List of Pets. Originally, the system was too narrow, but I realized that a real-world owner often manages a whole household of animals. By making the scheduler aggregate tasks across all pets, I was able to implement much more effective conflict detection and a unified daily timeline. I also replaced simple string-based priorities with a formal PriorityLevel enum to ensure that the sorting logic was consistent and less prone to errors during task comparisons.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler primarily balances hard time deadlines and the PriorityLevel assigned to each task, while also checking the owner's total daily availability.

- How did you decide which constraints mattered most?

I prioritized the due_time and priority as the most critical factors because a pet's essential needs, like time-sensitive medication, must always take precedence over flexible activities like grooming.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

One major tradeoff is that the scheduler uses a "first-fit" approach based on priority rather than trying to perfectly shuffle tasks to fill every single minute of the owner's free time.

- Why is that tradeoff reasonable for this scenario?

This is a reasonable compromise because pet care is naturally unpredictable, so a slightly less "packed" schedule provides the necessary buffer for the transitions and delays that happen when working with animals.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I utilized AI primarily for brainstorming the initial system architecture and generating the boilerplate code for the Python dataclasses.

- What kinds of prompts or questions were most helpful?

The most effective prompts were those that specifically requested Mermaid.js syntax for UML diagrams and "agent mode" requests for fleshing out method logic.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

I rejected an AI suggestion to store tasks in a single global list, choosing instead to encapsulate them within specific pet objects to maintain proper data ownership.

- How did you evaluate or verify what the AI suggested?

I verified the AI's algorithmic suggestions by running them through a standalone demo script to observe how they handled real-time inputs.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested whether marking a task as complete correctly updated its status and if adding a pet successfully expanded the owner's pet list.

- Why were these tests important?

These tests were vital to ensure that the fundamental state changes in the logic layer were functioning before I integrated them with the UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I have high confidence in the core scheduling logic since it passed all automated test suites and correctly sorted tasks in the CLI demo.

- What edge cases would you test next if you had more time?

Given more time, I would test edge cases involving overlapping task durations and pets with empty task lists to ensure the scheduler fails gracefully.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the transition from a single-pet system to a multi-pet household model, which feels much more like a real-world application.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

In a future iteration, I would redesign the task input system to include an end-time calculation rather than just a fixed duration.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that being a lead architect means using AI to handle the repetitive scaffolding while I focus on the high-level logic and system relationships.
