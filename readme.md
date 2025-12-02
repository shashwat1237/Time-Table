**University Timetable Generator**

A constraint-based, multi-room, multi-teacher, multi-class timetable scheduling engine built using Python & Pandas.

This project automatically generates weekly timetables for:

Classes / Sections

Teachers

Rooms (Classrooms, Labs, etc.)

…while respecting room types, lecture lengths, teacher availability, class availability, and two-hour lab constraints.

**Overview**

Educational institutes often manage hundreds of lectures per week across multiple departments. Manually creating a conflict-free timetable is extremely error-prone.

This project solves that problem through a fully automated scheduling system.

The system:

Loads structured CSV files describing classes, teachers, rooms, and subjects
Applies constraints (room availability, teacher availability, 1hr vs 2hr, room types)
Schedules all lectures for the full week (6 days × 7 slots)
Updates timetables for classes, teachers, and rooms
Writes the final timetable back into CSV files
Can optionally visualize any timetable using Plotly

🗂 Project Structure
Time-Table-main/
│
├── timetable2.py              # Core scheduling engine
├── display_timetable.py       # Plotly visualization script
│
├── classes.csv                # Class → subjects, teachers, lecture counts, timetable
├── teachers.csv               # Teacher timetables
├── rooms.csv                  # Room timetables + room types
├── subjects.csv               # Subjects + required room type + 1hr/2hr length
│
|
└── README.md                 

**How It Works**
**1️.Input Model (CSV Files)**

The system reads:

• subjects.csv

id

name

room_type

lecture_length (1 or 2 hour)

• classes.csv

st → subject_id → teacher_id mapping

sl → subject_id → lectures_per_week

timetable → 6×7 matrix (auto-filled by algorithm)

• teachers.csv

Teacher ID, name, timetable

• rooms.csv

Room ID, room type, timetable

**2️. Constraint Satisfaction Engine (timetable2.py)**

The engine generates conflict-free schedules using:

Greedy scheduling with priority ordering

Teacher availability checking

Class availability checking

Room type enforcement

Room availability checking

Two-hour lab block handling (requires consecutive periods)

Class priority sorting
(classes with highest total weekly lecture load scheduled first)

The solver works in two passes:

Schedule all 2-hour subjects first

Schedule all 1-hour subjects next

If any subject cannot be placed due to constraints, the system safely skips it and continues.

**3️. Output**

After running, all CSVs are automatically updated with the full timetable:

classes.csv contains a complete 6×7 grid for every class

teachers.csv contains each teacher’s schedule

rooms.csv contains each room's usage schedule

These CSVs can be opened directly in Excel or processed further.

**Usage**
**Run the Timetable Generator**
python timetable2.py


This:

Loads all CSV files

Generates a complete timetable

Writes the updated results back into:

teachers.csv

rooms.csv

classes.csv

**Visualize a Timetable**

You can visualize any timetable using Plotly.

Inside display_timetable.py, replace the timetable variable with the timetable you want to view:

timetable = classes.iloc[i]["timetable"]


Then run:

python display_timetable.py


A browser window will open with a clean table layout.

**Key Features**
✔ Supports both 1-hour and 2-hour lectures

Labs automatically require consecutive slots.

✔ Room type enforcement

Only matching rooms (e.g., physics lab, computer lab, classroom) are assigned.

✔ Fully automatic conflict resolution

No teacher, class, or room is double-booked.

✔ CSV-driven system

Easy to modify data without touching code.

✔ Scalable

Adding more:

Departments

Teachers

Rooms

Classes

…just means updating CSV files.

🔍 Algorithm Summary

Classes sorted by total lecture load

2-hour (lab) subjects scheduled first

Then 1-hour subjects

Each session checks:

Class timetable

Teacher timetable

All rooms of required room type

Consecutive slots if needed

First available conflict-free slot is chosen

Timetables updated immediately

 **Limitations**

Greedy algorithm (no backtracking)

Hard-coded 6 days × 7 slots

Scheduling fails silently for impossible constraints

CSVs must contain correct mappings (st, sl)

**Future Improvements**

Add backtracking or SAT/CP-SAT (Google OR-Tools) solver

Add GUI to choose class/teacher and display timetable

Add gap minimization & fairness optimization

Add feasibility checker before scheduling

Add ability to export as PDF


Feel free to fork, submit issues, or create pull requests.
