# attendance.py

import os
import smtplib
from datetime import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QComboBox

from queries import AllQueries

class AttendanceForm(QMainWindow):
    """
    Shows the user's attendance in a table with dummy data.
    The user can mark each row as Present or Absent and press
    'Mark Attendance' to confirm changes, which:
        1) Sends an email to the user with the updated info,
        2) Logs the change in the Activity table.
    """
    def __init__(self, parent=None, std_email=None, std_id=None):
        """
        :param parent: The window that spawned this form (e.g. MainStudentWindow).
        :param std_email: The student's email address.
        :param std_id: The student's ID (from the DB).
        """
        super().__init__(parent)
        uic.loadUi("attendance.ui", self)

        self.parent_window = parent
        self.std_email = std_email
        self.std_id = std_id

        # Initialize queries
        self.all_queries = AllQueries()

        # Configure the table
        self.setup_attendance_table()

        # Connect button
        self.mark_button.clicked.connect(self.handle_mark_attendance)

    def setup_attendance_table(self):
        from PyQt6.QtCore import Qt

        dummy_data = [
            ("2025-03-01", "Monday", "Present"),
            ("2025-03-02", "Tuesday", "Absent"),
            ("2025-03-03", "Wednesday", "Present"),
            ("2025-03-04", "Thursday", "Absent")
        ]

        self.attendance_table.setColumnCount(3)
        self.attendance_table.setRowCount(len(dummy_data))
        headers = ["Date", "Day", "Status"]
        self.attendance_table.setHorizontalHeaderLabels(headers)

        for row_index, (date_val, day_val, status_val) in enumerate(dummy_data):
            # Date column
            item_date = QTableWidgetItem(date_val)
            # remove editable flag -> read-only
            flags = item_date.flags()
            flags = flags & ~Qt.ItemFlag.ItemIsEditable
            item_date.setFlags(flags)
            self.attendance_table.setItem(row_index, 0, item_date)

            # Day column
            item_day = QTableWidgetItem(day_val)
            flags = item_day.flags()
            flags = flags & ~Qt.ItemFlag.ItemIsEditable
            item_day.setFlags(flags)
            self.attendance_table.setItem(row_index, 1, item_day)

            # Status column (QComboBox)
            combo_status = QComboBox()
            combo_status.addItems(["Present", "Absent"])
            combo_status.setCurrentText(status_val)
            self.attendance_table.setCellWidget(row_index, 2, combo_status)

    def handle_mark_attendance(self):
        """
        For each row, check if the user changed the status from the original dummy data.
        If changed, send an email and log it in the activity table.
        In this example, we simply re-check the final status for each row and do the needed updates.
        """
        row_count = self.attendance_table.rowCount()
        all_emails_sent = True
        for row in range(row_count):
            date_val = self.attendance_table.item(row, 0).text()
            day_val = self.attendance_table.item(row, 1).text()
            combo_status = self.attendance_table.cellWidget(row, 2)
            new_status = combo_status.currentText()

            if not self.send_attendance_email(date_val, day_val, new_status):
                all_emails_sent = False
            activity_desc = f"Attendance for {day_val} ({date_val}) changed to {new_status}"
            self.log_attendance_activity(activity_desc)

        if all_emails_sent:
            QMessageBox.information(self, "Attendance Update", "Attendance marked and emails sent!")
        else:
            QMessageBox.warning(
                self, "Attendance Update",
                "Attendance marked, but confirmation emails could not be sent.\n"
                "Set ATTENDANCE_SENDER_EMAIL and ATTENDANCE_SENDER_PASSWORD to enable email."
            )
        self.close()

    def send_attendance_email(self, date_val, day_val, status):
        """
        Sends an email about the new attendance status for date_val/day_val.
        If using Gmail with 2FA, remember to use an App Password or OAuth approach.
        """
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.environ.get("ATTENDANCE_SENDER_EMAIL", "")
        sender_password = os.environ.get("ATTENDANCE_SENDER_PASSWORD", "")

        if not sender_email or not sender_password:
            print("[WARN] ATTENDANCE_SENDER_EMAIL / ATTENDANCE_SENDER_PASSWORD not set. "
                  "Skipping attendance email.")
            return False

        subject = f"Attendance Updated: {status}"
        body = (
            "Hello,\n\n"
            f"Your attendance for {day_val}, {date_val} has been marked as '{status}'.\n"
            "If you did not request this change, please contact the administrator.\n"
            "\nRegards,\nAttendance System"
        )
        message = f"Subject: {subject}\n\n{body}"

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, self.std_email, message)
            return True
        except Exception as e:
            print("[Error] Could not send attendance email:", e)
            return False

    def log_attendance_activity(self, description):
        """
        Insert into the activity log that the user changed attendance.
        We assume there's a function in AllQueries or you can implement your own logic.
        For example:
        all_queries.insert_activity(std_id, activity_type, description, datetime, etc.)
        """
        now = datetime.now()
        activity_date = now.strftime("%Y-%m-%d")
        activity_time = now.strftime("%H:%M:%S")

        # Call the new method from queries.py
        self.all_queries.insert_activity(
            std_id=self.std_id,
            activity_type="Attendance",  # or "Attendance Change"
            description=description,
            date_val=activity_date,
            time_val=activity_time
        )

        # The above function depends on how your 'queries.py' is actually structured.
        # If you don't have such a function, create or adapt as needed.

