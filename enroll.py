from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem, QMessageBox, QTableWidget
from PyQt6 import uic
from queries import AllQueries


# from login_page import global_std_id


class ViewScheduleWindow(QMainWindow):
    closed = pyqtSignal()

    # def __init__(self):
    def __init__(self, email=None):
        super().__init__()

        # Load the UI file
        uic.loadUi('enroll.ui', self)

        # Set the table to be non-editable
        self.schedule_table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        if email is None:
            self.email = "alice20180@st.habib.edu.pk"
        else:
            self.email = email

        # Find the label by its name
        checkout_label = self.findChild(QLabel, 'schedule_label')

        self.all_queries = AllQueries()
        self.all_queries.update_std_id(self.all_queries.get_std_id_by_email(self.email))

        # Set the label font to bold
        font = checkout_label.font()
        font.setBold(True)
        checkout_label.setFont(font)

        # Connect buttons to methods
        self.enroll_button.clicked.connect(self.enroll_action)

        self.show_schedule()

    def show_schedule(self):
        self.schedule_table_widget.clearContents()
        self.schedule_table_widget.setRowCount(0)

        # Get all the courses from the database
        # all_courses = self.all_queries.get_all_courses_by_id_and_type(20180, "Add")
        # all_courses = self.all_queries.get_all_courses_by_id_and_type(global_std_id, "Add")
        all_courses = self.all_queries.get_all_courses_by_id_and_type("Add")
        # fill in the details in appropriate columns in schedule_table_widget
        for course in all_courses:
            course_list = self.all_queries.get_course_by_id(course.course_id)
            # Get the row number
            row = self.schedule_table_widget.rowCount()
            # Insert a new row at the bottom
            self.schedule_table_widget.insertRow(row)
            # Set the course id
            self.schedule_table_widget.setItem(row, 0, QTableWidgetItem(str(course_list.course_list_id)))
            self.schedule_table_widget.setItem(row, 1, QTableWidgetItem(course_list.course_name))
            self.schedule_table_widget.setItem(row, 2, QTableWidgetItem(course_list.section))
            self.schedule_table_widget.setItem(row, 3, QTableWidgetItem(course_list.instructor))
            self.schedule_table_widget.setItem(row, 4, QTableWidgetItem(course_list.days))
            self.schedule_table_widget.setItem(row, 5, QTableWidgetItem(str(course_list.start_time)))
            self.schedule_table_widget.setItem(row, 6, QTableWidgetItem(str(course_list.end_time)))
            self.schedule_table_widget.setItem(row, 7, QTableWidgetItem(course_list.room))
            status = "Closed"
            if course_list.status:
                status = "Open"
            self.schedule_table_widget.setItem(row, 8, QTableWidgetItem(status))

    def enroll_action(self):
        # Implement the enroll functionality
        print("Enroll button clicked")

        # Check if the status of all the courses is open, if anyone has closed status, show error message
        for row in range(self.schedule_table_widget.rowCount()):
            if self.schedule_table_widget.item(row, 8).text() == "Closed":
                QMessageBox.about(self, "Enroll", "You cannot enroll in a closed course")
                return

        self.all_queries.is_temp_false_remove_type_add("Add")
        # self.all_queries.is_temp_false_remove_type_add("Add")

        # Show acknowledgement message
        QMessageBox.about(self, "Enroll", "You have successfully enrolled in the selected courses")

        # Get all the course id from the schedule_table_widget
        course_ids = []
        for row in range(self.schedule_table_widget.rowCount()):
            if self.schedule_table_widget.item(row, 0).checkState():
                course_ids.append(self.schedule_table_widget.item(row, 0).text())

        course_ids_text = ""
        for course_id in course_ids:
            course_ids_text += course_id + ", "
        course_ids_text = course_ids_text[:-2]

        # Get all the sections from the schedule_table_widget
        sections = []
        for row in range(self.schedule_table_widget.rowCount()):
            if self.schedule_table_widget.item(row, 0).checkState():
                sections.append(self.schedule_table_widget.item(row, 2).text())

        sections_text = ""
        for section in sections:
            sections_text += section + ", "
        sections_text = sections_text[:-2]
        print(course_ids_text)
        print(sections_text)
        print(type(course_ids_text))
        print(type(sections_text))

        self.all_queries.add_data_to_activity_log(course_id=course_ids_text, std_id=self.all_queries.get_std_id(),
                                                  activity_type="Enroll", section=sections_text)

        # Update current capacity
        # Get the course list from course_ids and sections
        for course_id, section in zip(course_ids, sections):
            # course_list = self.all_queries.get_course_by_id_and_section(course_id, section)
            # Update the current capacity
            is_capacity = self.all_queries.update_current_capacity(course_id, section, "Subtract")
            if not is_capacity:
                QMessageBox.about(self, "Enroll", "Invalid capacity")
                return

        self.schedule_table_widget.clearContents()
        self.schedule_table_widget.setRowCount(0)

    def reopen_login(self):
        self.show()

    def closeEvent(self, event):
        print("User has clicked the red 'x' on the enroll window")
        # Here you can accept or ignore the event to close the window
        # super().closeEvent(event)
        self.closed.emit()


if __name__ == "__main__":
    app = QApplication([])
    window = ViewScheduleWindow()
    window.show()
    app.exec()
