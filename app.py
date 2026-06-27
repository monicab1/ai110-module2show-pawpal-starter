import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ── Step 2: Manage Application Memory ─────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

# ── Header ─────────────────────────────────────────────────────────────────
st.title("🐾 PawPal+")
st.caption("Your pet care planning assistant.")

st.divider()

# ── Section 1: Owner Setup ─────────────────────────────────────────────────
st.subheader("👤 Owner")

owner_name = st.text_input("Your name", value=st.session_state.owner.name)

if st.button("Save Owner"):
    st.session_state.owner.name = owner_name
    st.success(f"Owner saved: {owner_name}")

st.divider()

# ── Section 2: Add a Pet ───────────────────────────────────────────────────
st.subheader("🐾 Add a Pet")

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Fish", "Bird", "Rabbit", "Hamster", "Turtle", "Other"])

if st.button("Add Pet"):
    if pet_name.strip() == "":
        st.warning("Please enter a pet name.")
    elif st.session_state.owner.get_pet(pet_name):
        st.warning(f"{pet_name} is already added.")
    else:
        new_pet = Pet(name=pet_name, species=species)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"{pet_name} the {species} added!")

# Show current pets
if st.session_state.owner.pets:
    st.markdown("**Your pets:**")
    for pet in st.session_state.owner.pets:
        st.markdown(f"- {pet.name} ({pet.species})")

st.divider()

# ── Section 3: Add a Task ──────────────────────────────────────────────────
st.subheader("📋 Add a Task")

if not st.session_state.owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_options = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Assign task to", pet_options)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="07:00")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)

    col4, col5 = st.columns(2)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly"])
    with col5:
        due = st.date_input("Due date", value=date.today())

    if st.button("Add Task"):
        target_pet = st.session_state.owner.get_pet(selected_pet_name)
        new_task = Task(
            description=task_title,
            time_str=task_time,
            duration=int(duration),
            frequency=frequency,
            due_date=due,
        )
        target_pet.add_task(new_task)
        st.success(f"Task '{task_title}' added to {selected_pet_name}!")

st.divider()

# ── Section 4: Mark a Task Complete ───────────────────────────────────────
st.subheader("✅ Mark a Task Complete")

if not st.session_state.owner.pets:
    st.info("Add a pet and some tasks first.")
else:
    pet_options = [p.name for p in st.session_state.owner.pets]
    complete_pet_name = st.selectbox("Select pet", pet_options, key="complete_pet")
    target_pet = st.session_state.owner.get_pet(complete_pet_name)

    if not target_pet.tasks:
        st.caption("No tasks found for this pet.")
    else:
        task_options = [
            f"{t.time_str} — {t.description} ({'✅ done' if t.is_complete else 'pending'})"
            for t in target_pet.tasks
        ]
        selected_task_index = st.selectbox("Select task", range(len(task_options)),
                                           format_func=lambda i: task_options[i],
                                           key="complete_task")

        if st.button("Mark Complete"):
            target_pet.tasks[selected_task_index].mark_complete()
            st.success("Task marked complete!")


st.subheader("📅 Today's Schedule")

if not st.session_state.owner.pets:
    st.info("Add a pet and some tasks to see the schedule.")
else:
    view_mode = st.radio(
        "View mode",
        ["By pet", "All pets combined"],
        horizontal=True,
    )

    if st.button("Generate Schedule"):
        today = date.today()

        if view_mode == "By pet":
            for pet in st.session_state.owner.pets:
                st.markdown(f"**{pet.name} ({pet.species})**")
                plan, warnings = Scheduler.generate_daily_plan(pet, today)
                if plan:
                    for line in plan:
                        st.markdown(f"- {line}")
                else:
                    st.caption("No tasks scheduled for today.")
                if warnings:
                    for w in warnings:
                        st.warning(w)
                st.markdown("---")

        else:
            plan, cross_warnings = Scheduler.generate_full_plan(
                st.session_state.owner, today
            )
            if plan:
                for line in plan:
                    st.markdown(f"- {line}")
            else:
                st.caption("No tasks scheduled for today across any pets.")
            if cross_warnings:
                for w in cross_warnings:
                    st.warning(w)
