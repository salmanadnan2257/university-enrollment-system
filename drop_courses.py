from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6 import uic

from queries import AllQueries
# from login_page import global_std_id


class DropCoursesWindow(QMainWindow):
    closed = pyqtSignal()

    # def __init__(self):
    def __init__(self, email=None):
        super().__init__()

        # Load the UI file
        uic.loadUi('drop_courses.ui', self)

        # Set the table to be non-editable
        self.drop_courses_table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        if email is None:
            self.email = "alice20180@st.habib.edu.pk"
        else:
            self.email = email

        # Find the label by its name and set it to bold
        drop_courses_label = self.findChild(QLabel, 'drop_courses_label')
        font = drop_courses_label.font()
        font.setBold(True)
        drop_courses_label.setFont(font)
        self.all_queries = AllQueries()
        self.all_queries.update_std_id(self.all_queries.get_std_id_by_email(self.email))

        # Connect button clicks to respective methods
        self.drop_button.clicked.connect(self.drop_course)
        # self.confirm_button.clicked.connect(self.confirm_drop)

        # Set up the drop courses table
        self.setup_drop_courses_table()

    def setup_drop_courses_table(self):
        # Set column headers for the drop courses table
        headers = ["Course ID", "Course Name", "Section", "Instructor", "Days", "Start Time", "End Time", "Room",
                   "Status"]
        self.drop_courses_table_widget.setColumnCount(len(headers))
        self.drop_courses_table_widget.setHorizontalHeaderLabels(headers)

        self.drop_courses_table_widget.clearContents()
        self.drop_courses_table_widget.setRowCount(0)

        # all_courses = self.all_queries.get_all_courses_by_id(20180)
        # all_courses = self.all_queries.get_all_courses_by_id(global_std_id)
        all_courses = self.all_queries.get_all_courses_by_id()

        # Fill in the details in appropriate columns in drop_courses_table_widget
        for course in all_courses:
            course_list = AllQueries().get_course_by_id_and_section(course.course_id, course.section)
            # Get the row number
            row = self.drop_courses_table_widget.rowCount()
            # Insert a new row at the bottom
            self.drop_courses_table_widget.insertRow(row)
            # Set the course id
            self.drop_courses_table_widget.setItem(row, 0, QTableWidgetItem(str(course_list.course_list_id)))
            self.drop_courses_table_widget.setItem(row, 1, QTableWidgetItem(course_list.course_name))
            self.drop_courses_table_widget.setItem(row, 2, QTableWidgetItem(course_list.section))
            self.drop_courses_table_widget.setItem(row, 3, QTableWidgetItem(course_list.instructor))
            self.drop_courses_table_widget.setItem(row, 4, QTableWidgetItem(course_list.days))
            self.drop_courses_table_widget.setItem(row, 5, QTableWidgetItem(str(course_list.start_time) + " - " + str(course_list.end_time)))
            self.drop_courses_table_widget.setItem(row, 6, QTableWidgetItem(course_list.room))
            status = "Closed"
            if course_list.status:
                status = "Open"
            self.drop_courses_table_widget.setItem(row, 7, QTableWidgetItem(status))

    def drop_course(self):
        print("Drop Course clicked")

        # Confirm from the user
        response = QMessageBox.question(self, "Confirm Drop", "Are you sure you want to drop the selected course(s)?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        print(response)

        if response == QMessageBox.StandardButton.Yes:
            # Get the selected row
            row = self.drop_courses_table_widget.currentRow()
            # Get the course id
            course_id = self.drop_courses_table_widget.item(row, 0).text()
            # Get the section
            section = self.drop_courses_table_widget.item(row, 2).text()
            # Remove course from Course
            # self.all_queries.remove_course(20180, course_id, section)
            # self.all_queries.remove_course(global_std_id, course_id, section)
            self.all_queries.remove_course(course_id, section)

            # Update capacity
            is_capacity = self.all_queries.update_current_capacity(course_id, section, "Add")
            if not is_capacity:
                QMessageBox.warning(self, "Capacity", "Invalid capacity")
                return

            # Remove the row from the table
            self.drop_courses_table_widget.removeRow(row)

            # Add to activity log
            self.all_queries.add_data_to_activity_log(course_id=course_id, std_id=self.all_queries.get_std_id(),
                                                      activity_type="Drop", section=section)

    def closeEvent(self, event):
        print("User clicked the red 'x' on the drop courses window")
        # Handle window close event here
        # For example, you can accept or ignore the event to close the window
        # super().closeEvent(event)
        self.closed.emit()


if __name__ == "__main__":
    app = QApplication([])
    window = DropCoursesWindow()
    window.show()
    app.exec()
