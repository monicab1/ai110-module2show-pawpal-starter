import streamlit as st
from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ── Session State ──────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

if "show_schedule" not in st.session_state:
    st.session_state.show_schedule = False

if "editing_task" not in st.session_state:
    # Stores (pet_name, task_index) of the task currently being edited
    st.session_state.editing_task = None

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

if st.session_state.owner.pets:
    st.markdown("**Your pets:**")
    for pet in st.session_state.owner.pets:
        st.markdown(f"- {pet.name} ({pet.species})")

st.divider()

# ── Section 3: Add a Task ──────────────────────────────────────────────────
st.subheader("📋 Add a Task")

HOURS = [f"{h:02d}" for h in range(24)]

if not st.session_state.owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_options = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Assign task to", pet_options, key="add_task_pet")

    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        task_title = st.text_input("Task title", value="", placeholder="e.g. Morning walk", max_chars=36)
    with col2:
        add_hour = st.selectbox("Hour", HOURS, index=7, key="add_hour")
    with col3:
        add_min = st.number_input("Min", min_value=0, max_value=59, value=0, key="add_min")
    with col4:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)

    col4, col5 = st.columns(2)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly"])
    with col5:
        due = st.date_input("Due date", value=date.today())

    if st.button("Add Task"):
        if task_title.strip() == "":
            st.warning("Please enter a task title.")
        else:
            task_time = f"{add_hour}:{int(add_min):02d}"
            target_pet = st.session_state.owner.get_pet(selected_pet_name)
            new_task = Task(
                description=task_title.strip(),
                time_str=task_time,
                duration=int(duration),
                frequency=frequency,
                due_date=due,
            )
            target_pet.add_task(new_task)
            st.success(f"Task '{task_title}' added to {selected_pet_name}!")

st.divider()

# ── Section 4: Edit / Remove a Task ───────────────────────────────────────
with st.expander("✏️ Edit / Remove a Task"):
    if not st.session_state.owner.pets:
        st.info("Add a pet first.")
    else:
        edit_pet_name = st.selectbox(
            "Select a pet",
            ["-- Select a pet --"] + [p.name for p in st.session_state.owner.pets],
            key="edit_pet_select"
        )

        if edit_pet_name == "-- Select a pet --":
            st.caption("Select a pet above to see their tasks.")
        else:
            edit_pet = st.session_state.owner.get_pet(edit_pet_name)
            if not edit_pet or not edit_pet.tasks:
                st.caption("This pet has no tasks yet.")
            else:
                for idx, task in enumerate(edit_pet.tasks):
                    col_info, col_edit, col_del = st.columns([6, 1, 1])
                    with col_info:
                        marker = "✅" if task.is_complete else "⬜"
                        st.markdown(f"{marker} **{task.time_str}** — {task.description} ({task.duration} min, {task.frequency})")
                    with col_edit:
                        if st.button("✏️", key=f"edit_btn_{edit_pet_name}_{idx}", help="Edit this task"):
                            st.session_state.editing_task = (edit_pet_name, idx)
                    with col_del:
                        if st.button("🗑️", key=f"del_btn_{edit_pet_name}_{idx}", help="Delete this task"):
                            edit_pet.remove_task(idx)
                            st.session_state.show_schedule = False
                            st.session_state.editing_task = None
                            st.rerun()

                    if st.session_state.editing_task == (edit_pet_name, idx):
                        with st.container():
                            st.markdown("**Edit task:**")
                            cur_hour, cur_min = task.time_str.split(":")
                            e_col1, e_col2, e_col3, e_col4 = st.columns([3, 1, 1, 1])
                            with e_col1:
                                new_title = st.text_input(
                                    "Task title",
                                    value=task.description,
                                    max_chars=36,
                                    key=f"e_title_{edit_pet_name}_{idx}"
                                )
                            with e_col2:
                                e_hour = st.selectbox(
                                    "Hour",
                                    HOURS,
                                    index=HOURS.index(cur_hour),
                                    key=f"e_hour_{edit_pet_name}_{idx}"
                                )
                            with e_col3:
                                e_min = st.number_input(
                                    "Min",
                                    min_value=0,
                                    max_value=59,
                                    value=int(cur_min),
                                    key=f"e_min_{edit_pet_name}_{idx}"
                                )
                            with e_col4:
                                new_duration = st.number_input(
                                    "Duration (min)",
                                    min_value=1,
                                    max_value=240,
                                    value=task.duration,
                                    key=f"e_dur_{edit_pet_name}_{idx}"
                                )

                            e_col5, e_col6 = st.columns(2)
                            with e_col5:
                                new_frequency = st.selectbox(
                                    "Frequency",
                                    ["daily", "weekly"],
                                    index=0 if task.frequency == "daily" else 1,
                                    key=f"e_freq_{edit_pet_name}_{idx}"
                                )
                            with e_col6:
                                new_due = st.date_input(
                                    "Due date",
                                    value=date.today(),
                                    key=f"e_due_{edit_pet_name}_{idx}"
                                )

                            s_col1, s_col2 = st.columns(2)
                            with s_col1:
                                if st.button("💾 Save", key=f"save_{edit_pet_name}_{idx}"):
                                    if new_title.strip() == "":
                                        st.warning("Task title cannot be empty.")
                                    else:
                                        task.description = new_title.strip()
                                        task.time_str = f"{e_hour}:{int(e_min):02d}"
                                        task.duration = int(new_duration)
                                        task.frequency = new_frequency
                                        task.due_date = new_due
                                        task.is_complete = False
                                        st.session_state.editing_task = None
                                        st.session_state.show_schedule = False
                                        st.rerun()
                            with s_col2:
                                if st.button("Cancel", key=f"cancel_{edit_pet_name}_{idx}"):
                                    st.session_state.editing_task = None
                                    st.rerun()

st.divider()

# ── Section 5: Today's Schedule ───────────────────────────────────────────
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
        st.session_state.show_schedule = True

    if st.session_state.show_schedule:
        today = date.today()

        if view_mode == "By pet":
            for pet in st.session_state.owner.pets:
                st.markdown(f"**{pet.name} ({pet.species})**")

                # Show tasks due today OR completed tasks whose slot was today
                todays_tasks = []
                for i, t in enumerate(pet.tasks):
                    is_today = t.due_date == today
                    was_today = t.is_complete and (
                        t.due_date - timedelta(days=1) == today or
                        t.due_date - timedelta(days=7) == today
                    )
                    if is_today or was_today:
                        todays_tasks.append((i, t))

                todays_tasks.sort(key=lambda x: x[1].time_str)

                if todays_tasks:
                    for i, task in todays_tasks:
                        col1, col2 = st.columns([7, 2])
                        with col1:
                            marker = "✅" if task.is_complete else "⬜"
                            st.markdown(f"{marker}  {task.time_str} — {task.description} ({task.duration} min)")
                        with col2:
                            if task.is_complete:
                                if st.button("↩️ Undo", key=f"undo_{pet.name}_{i}"):
                                    task.undo_complete(today)
                                    st.rerun()
                            else:
                                if st.button("✅ Mark Done", key=f"done_{pet.name}_{i}"):
                                    task.mark_complete()
                                    st.rerun()
                else:
                    st.caption("No tasks scheduled for today.")

                _, warnings = Scheduler.generate_daily_plan(pet, today)
                if warnings:
                    for w in warnings:
                        st.warning(w)
                st.markdown("---")

        else:
            all_tasks = []
            for pet in st.session_state.owner.pets:
                for i, task in enumerate(pet.tasks):
                    is_today = task.due_date == today
                    was_today = task.is_complete and (
                        task.due_date - timedelta(days=1) == today or
                        task.due_date - timedelta(days=7) == today
                    )
                    if is_today or was_today:
                        all_tasks.append((pet, i, task))

            all_tasks.sort(key=lambda x: x[2].time_str)

            if all_tasks:
                for pet, i, task in all_tasks:
                    col1, col2 = st.columns([7, 2])
                    with col1:
                        marker = "✅" if task.is_complete else "⬜"
                        st.markdown(f"{marker}  {task.time_str} — [{pet.name}] {task.description} ({task.duration} min)")
                    with col2:
                        if task.is_complete:
                            if st.button("↩️ Undo", key=f"undo_full_{pet.name}_{i}"):
                                task.undo_complete(today)
                                st.rerun()
                        else:
                            if st.button("✅ Mark Done", key=f"done_full_{pet.name}_{i}"):
                                task.mark_complete()
                                st.rerun()
            else:
                st.caption("No tasks scheduled for today across any pets.")

            _, cross_warnings = Scheduler.generate_full_plan(st.session_state.owner, today)
            if cross_warnings:
                for w in cross_warnings:
                    st.warning(w)
