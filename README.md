# University Enrollment System

A desktop course-registration app built with PyQt6 and SQLAlchemy over SQLite. A student logs in, confirms a code sent by email, then enrolls in sections, adds, drops, or swaps courses with clash and capacity checks, views a weekly schedule (exportable to Excel), marks attendance, and reviews an activity log of everything they did.

Built as the semester project for the Databases course (CS/CE 355/373) at Habib University, 4th semester. Two-person team: Salman Adnan and Shayan Wasif. Salman's areas were the email verification (login MFA) flow, the attendance module with email confirmations, Docker packaging, and integration plus bug fixing across the screens.

## Features

- Login with email and password, followed by a 6-digit verification code sent over SMTP
- Enroll in course sections with capacity tracking (a section closes when full)
- Add, drop, and swap courses with schedule-clash detection
- Weekly and per-day schedule view, exportable to Excel via pandas/openpyxl
- Attendance screen that emails the student a confirmation for each change
- Activity log recording every add, drop, swap, and attendance change with timestamps

## Architecture

- `login_page.py` is the entry point. It opens `verification.py` (emails a code), which opens `main_window.py`, the hub for all other screens.
- Each screen is a `QMainWindow` subclass paired with a Qt Designer `.ui` file loaded at runtime with `uic.loadUi`.
- `student_database.py` defines the SQLAlchemy models (Student, Course, CourseList, Filter, Activity) against `student.db` (SQLite).
- `queries.py` (`AllQueries`) is the single data-access layer the UI classes call; it holds the logged-in student id and wraps all session queries and commits.
- `courses_database.py` is a seeding helper for the course catalog.

## Setup

Requires Python 3.10+ and a desktop environment (it is a GUI app).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python login_page.py
```

Email sending is optional. To enable it, copy `.env.example`, fill in a Gmail address and App Password, and export both variables before launching:

```bash
export ATTENDANCE_SENDER_EMAIL=sender@example.com
export ATTENDANCE_SENDER_PASSWORD=your-app-password
```

Without them the app still runs: the login verification code is printed to the terminal instead of emailed, and attendance changes are saved with a warning that no confirmation email went out.

A Dockerfile and per-OS run scripts (`run-linux.sh`, `run-macos.sh`, `run-windows.ps1`) are included; they forward the host display into the container.

## Usage

`student.db` ships pre-seeded with a demo course catalog and dummy accounts. Sample logins:

- `bob123@st.habib.edu.pk` / `bob123`
- `ronaldo273@st.habib.edu.pk` / `ronaldo123`
- `babar173@st.habib.edu.pk` / `babar123`

Note: this is a coursework demo database. The accounts are fake and the passwords are stored in plaintext because the login code compares them directly; do not reuse this scheme with real credentials.

## Challenges

- Email that had to work with no credentials. The login MFA and the attendance confirmations both go out over Gmail SMTP, but anyone cloning the repo has no App Password, and a blind send would either hang or throw. The fix was to read `ATTENDANCE_SENDER_EMAIL` and `ATTENDANCE_SENDER_PASSWORD` from the environment and branch before touching `smtplib`. In `verification.py`, missing creds print the six-digit code to the terminal and pop a warning, so login still completes. In `attendance.py`, `send_attendance_email` returns `False` and `handle_mark_attendance` shows "confirmation emails could not be sent" instead of falsely claiming they were sent. The same two env vars drive both paths, and `.env.example` documents them.
- Being honest about plaintext passwords. Login in `login_page.py` calls `get_password_by_email` and does a raw `password == user_password` compare, and the `Student.password` column in `student_database.py` is a plain `String`. That is a real weakness, not a design choice worth defending. Rather than paper over it, the Usage note and the seed data call it out as a coursework limitation and warn against reusing the scheme with real credentials. Hashing (bcrypt) is left as a documented follow-up in "What I'd do differently" instead of a silent gap.
- Testing a GUI that loads `.ui` at runtime, with no display. Every screen calls `uic.loadUi('name.ui', self)` with a relative path, so the app and its smoke test only work when run from the project directory. Making it testable headless took two things: setting `QT_QPA_PLATFORM=offscreen` so no X server is needed, and patching the static `QMessageBox` methods (`information`, `warning`, `critical`) to record their calls rather than block on a modal that nobody clicks. With those in place, the login-to-main-window flow plus every sub-screen (enroll, add, drop, swap, schedule, attendance, activity log) build and query the DB in one pass.
- Excel export without clobbering old files. `view_schedule.py` builds a `pandas.DataFrame` from the table rows and writes it with `to_excel` (openpyxl backend). If `schedule_by_week.xlsx` already exists, `save_data` catches it by trying `read_excel` first and, on success, bumping the name to `schedule_by_week (1).xlsx`, `(2)`, and so on. Day-mode export is deliberately disabled: the day view hides a column, the export was writing misaligned data, so it now returns an "Export Not Available" message rather than producing a broken sheet.
- Splitting the work across a two-person team. This was built by Salman Adnan and Shayan Wasif, and the hard part was keeping the screens consistent while each of us owned different windows. Salman owned the email verification (login MFA) flow, the attendance module with its email confirmations, the Docker packaging, and the integration and bug fixing that tied the separate screens together. We used a single `AllQueries` data-access layer as the contract between screens, so the UI code on either side only had to agree on method names. That is what kept the merges tractable.
- **Writing the exhaustive project documentation honestly.** Reading the whole codebase to document it honestly turned up two classes named ViewScheduleWindow in different files, a genuine naming collision, plus a schema-incompatible Student model file that's never imported anywhere. The README also describes a specific offscreen-testing methodology that no test file in the repo actually implements, which had to be reported as unconfirmed rather than assumed true.

## What I learned

- Gate any network call on a config check and pick a truthful fallback. The `if not sender_email or not sender_password` branch in both email paths is what lets the app run for anyone offline, and returning an honest status (printed code, `False` from the send) keeps the UI from claiming an email went out when it did not.
- Relative `uic.loadUi` paths tie the program to its working directory: it runs from the project root and breaks from anywhere else. Worth knowing before packaging, and the reason the run scripts and Docker set the workdir.
- A Qt app is testable without a display. `QT_QPA_PLATFORM=offscreen` plus monkeypatched `QMessageBox` static methods turned a click-through app into a scriptable smoke test that builds every screen and asserts on the dialogs it raised. This is how the project was last verified.
- Module-level side effects are a trap. `student_database.py` creates the engine, runs `create_all`, and opens a session at import time with `echo=True`, so importing any screen spams SQL and touches the database file. That setup belongs behind a function or an app entry point.
- Shared mutable state across screens is a bug source. `AllQueries.glob_id` (defaulting to a hardcoded 20180) is set by whichever window ran last, so the query layer's correctness depends on call order. A session object owned by the main window and passed in would remove a class of "ran as the wrong student" errors.
- Export code has to assume the target file already exists. Probing with `read_excel` and auto-incrementing the filename is a cheap way to avoid silently overwriting a previous export.

## What I'd do differently

- Hash passwords. The Student table stores plaintext and login does a string compare. Even for coursework, bcrypt would have been an afternoon of work.
- Put the student id in one place. `AllQueries` carries a mutable `glob_id` that every screen updates; a session object owned by the main window would remove a whole class of "queries ran as the wrong student" bugs.
- One `AllQueries` and one DB session, injected into screens, instead of each window constructing its own.
- The attendance table is dummy data hardcoded in the UI class rather than a real table in the schema, so marks don't persist between sessions. It should have been an Attendance model like everything else.
- Replace the scattered `print` debugging with logging, and stop `student_database.py` from running `create_all` and echoing SQL as an import side effect.
- Add tests. Everything here was verified by clicking through the app; the query layer is separable enough that it could have had unit tests from day one.
