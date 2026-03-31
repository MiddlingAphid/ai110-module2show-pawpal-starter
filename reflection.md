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
