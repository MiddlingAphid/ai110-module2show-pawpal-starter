from pawpal_system import Owner, Pet, Task, PriorityLevel, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=180)

owner = st.session_state.owner
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

st.subheader("Pets")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species)
    owner.add_pet(new_pet)

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": pet.name, "species": pet.species} for pet in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
st.caption("Add a task for a selected pet. The scheduler will use these tasks to build a plan.")

if owner.pets:
    scheduler = Scheduler(owner=owner, pets=owner.pets)
    pet_options = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Select pet", pet_options)
    selected_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), owner.pets[0])

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox(
            "Priority",
            [PriorityLevel.LOW, PriorityLevel.MEDIUM, PriorityLevel.HIGH],
            index=2,
            format_func=lambda p: p.value,
        )

    if st.button("Add task"):
        new_task = Task(
            title=task_title,
            duration_mins=int(duration),
            priority=priority,
        )
        selected_pet.add_task(new_task)

    filtered_tasks = scheduler.filter_tasks(pet_name=selected_pet.name)
    sorted_tasks = scheduler.sort_tasks_by_due_time(filtered_tasks)

    if sorted_tasks:
        st.success(f"Showing sorted tasks for {selected_pet.name}")
        st.table(
            [
                {
                    "title": task.title,
                    "duration_mins": task.duration_mins,
                    "priority": task.priority.value,
                    "due_date": task.due_date,
                    "due_time": task.due_time,
                }
                for task in sorted_tasks
            ]
        )
    else:
        st.info(f"No tasks for {selected_pet.name} yet. Add one above.")

    conflict_warnings = scheduler.detect_conflicts()
    if conflict_warnings:
        for warning in conflict_warnings:
            st.warning(warning)
else:
    st.info("Add a pet before adding tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Use your backend scheduler to generate the daily plan.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner, pets=owner.pets)
    validation = scheduler.validate_tasks()
    if validation.warnings:
        for warning in validation.warnings:
            st.warning(warning)

    daily_plan = scheduler.generate_daily_plan()
    if daily_plan.tasks:
        st.success("Schedule generated successfully")
        st.table(
            [
                {
                    "title": task.title,
                    "due_date": task.due_date,
                    "due_time": task.due_time or "Anytime",
                    "duration_mins": task.duration_mins,
                    "priority": task.priority.value,
                }
                for task in daily_plan.tasks
            ]
        )
        st.write("### Plan explanation")
        st.write(daily_plan.summarize())
    else:
        st.info("No scheduled tasks are available yet.")
