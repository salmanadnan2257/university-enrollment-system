import sys
import traceback
from datetime import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem, QMessageBox, QTableWidget
from PyQt6.QtCore import pyqtSignal

from queries import AllQueries


# from login_page import global_std_id


class SwapCoursesWindow(QMainWindow):
    closed = pyqtSignal()

    # def __init__(self):
    def __init__(self, email=None):
        super().__init__()

        # Load the UI file
        uic.loadUi('swap_courses.ui', self)

        # Set the table to be non-editable
        self.swap_courses_tableview.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.swap_enrolled_courses_tableview.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        if email is None:
            self.email = "alice20180@st.habib.edu.pk"
        else:
            self.email = email

        # Find the label by its name
        swap_courses_label = self.findChild(QLabel, 'swap_courses_label')

        # Set the label font to bold
        font = swap_courses_label.font()
        font.setBold(True)
        swap_courses_label.setFont(font)

        self.all_queries = AllQueries()
        self.all_queries.update_std_id(self.all_queries.get_std_id_by_email(self.email))

        # Connect the button clicks to their respective methods
        self.select_button.clicked.connect(self.select_courses)
        # self.enroll_button.clicked.connect(self.enroll)
        self.swap_button.clicked.connect(self.swap_courses)

        # Set up the course lists
        self.setup_course_lists()

    def setup_course_lists(self):
        # Set column headers for the course lists
        headers = ["Course ID", "Course Name", "Section", "Instructor", "Days", "Start Time", "End Time", "Room",
                   "Status"]
        self.swap_courses_tableview.setColumnCount(len(headers))
        self.swap_courses_tableview.setHorizontalHeaderLabels(headers)

        # Add a column for 'New Column' in the 'swap_enrolled_courses_tableview'
        self.swap_enrolled_courses_tableview.setColumnCount(len(headers))
        # headers.append("New Column")
        self.swap_enrolled_courses_tableview.setHorizontalHeaderLabels(headers)

        all_courses = self.all_queries.get_all_courses()
        # all_enrolled_courses = self.all_queries.get_all_courses_by_id(20180)
        # all_enrolled_courses = self.all_queries.get_all_courses_by_id(global_std_id)
        all_enrolled_courses = self.all_queries.get_all_courses_by_id()

        self.fill_swap_courses_tableview(all_courses)
        # self.fill_swap_enrolled_courses_tableview(all_enrolled_courses)

    def fill_swap_courses_tableview(self, all_courses):
        self.swap_courses_tableview.clearContents()
        self.swap_courses_tableview.setRowCount(0)

        # # Set the number of rows in the tableview
        # self.swap_courses_tableview.setRowCount(len(all_courses))

        # Fill the tableview with the courses
        # for row, course in enumerate(all_courses):
        for course_list in all_courses:
            # course_list = self.all_queries.get_course_by_id_and_section(course.course_list_id, course.section)
            # course_list = self.all_queries.get_course_by_id_and_section(course.course_id, course.section)
            if (not course_list.status or self.all_queries.is_user_enrolled_in_this_course
                (course_id=course_list.course_list_id,
                 section=course_list.section)):
                continue

            # Get the row number
            row = self.swap_courses_tableview.rowCount()
            print()
            print()
            print(f"row: {row}")
            # Insert a new row at the bottom
            self.swap_courses_tableview.insertRow(row)
            # Set the course id
            self.swap_courses_tableview.setItem(row, 0, QTableWidgetItem(str(course_list.course_list_id)))
            self.swap_courses_tableview.setItem(row, 1, QTableWidgetItem(course_list.course_name))
            self.swap_courses_tableview.setItem(row, 2, QTableWidgetItem(course_list.section))
            self.swap_courses_tableview.setItem(row, 3, QTableWidgetItem(course_list.instructor))
            self.swap_courses_tableview.setItem(row, 4, QTableWidgetItem(course_list.days))
            self.swap_courses_tableview.setItem(row, 5, QTableWidgetItem(str(course_list.start_time)))
            self.swap_courses_tableview.setItem(row, 6, QTableWidgetItem(str(course_list.end_time)))
            self.swap_courses_tableview.setItem(row, 7, QTableWidgetItem(course_list.room))
            status = "Closed"
            if course_list.status:
                status = "Open"
            self.swap_courses_tableview.setItem(row, 8, QTableWidgetItem(status))

        # Sort by course_id
        self.swap_courses_tableview.sortItems(0)

    def fill_swap_enrolled_courses_tableview(self, all_enrolled_courses):
        # Empty the tableview
        self.swap_enrolled_courses_tableview.clearContents()
        self.swap_enrolled_courses_tableview.setRowCount(0)

        # # Set the number of rows in the tableview
        # self.swap_enrolled_courses_tableview.setRowCount(len(all_enrolled_courses))

        # Fill the tableview with the courses
        for course in all_enrolled_courses:
            course_list = self.all_queries.get_course_by_id_and_section(course.course_id, course.section)
            # if (not course_list.status or self.all_queries.is_user_enrolled_in_this_course
            #     (course_id=course_list.course_list_id,
            #      section=course_list.section)):
            #     continue

            # Get the row number
            row = self.swap_enrolled_courses_tableview.rowCount()
            # Insert a new row at the bottom
            self.swap_enrolled_courses_tableview.insertRow(row)

            # course_list = self.all_queries.get_course_by_id_and_section(course.course_id, course.section)
            self.swap_enrolled_courses_tableview.setItem(row, 0, QTableWidgetItem(str(course_list.course_list_id)))
            self.swap_enrolled_courses_tableview.setItem(row, 1, QTableWidgetItem(course_list.course_name))
            self.swap_enrolled_courses_tableview.setItem(row, 2, QTableWidgetItem(course_list.section))
            self.swap_enrolled_courses_tableview.setItem(row, 3, QTableWidgetItem(course_list.instructor))
            self.swap_enrolled_courses_tableview.setItem(row, 4, QTableWidgetItem(course_list.days))
            self.swap_enrolled_courses_tableview.setItem(row, 5, QTableWidgetItem(str(course_list.start_time)))
            self.swap_enrolled_courses_tableview.setItem(row, 6, QTableWidgetItem(str(course_list.end_time)))
            self.swap_enrolled_courses_tableview.setItem(row, 7, QTableWidgetItem(course_list.room))
            status = "Closed"
            if course_list.status:
                status = "Open"
            self.swap_enrolled_courses_tableview.setItem(row, 8, QTableWidgetItem(status))

    def fill_swap_enrolled_courses_tableview_with_course(self, course):
        # Add the course to the enrolled courses table

        # Set the number of rows in the enrolled courses table + 1
        self.swap_enrolled_courses_tableview.setRowCount(self.swap_enrolled_courses_tableview.rowCount() + 1)

        # Get the row number
        row = self.swap_enrolled_courses_tableview.rowCount() - 1

        # Fill the tableview with the courses
        self.swap_enrolled_courses_tableview.setItem(row, 0, QTableWidgetItem(str(course.course_list_id)))
        self.swap_enrolled_courses_tableview.setItem(row, 1, QTableWidgetItem(course.course_name))
        self.swap_enrolled_courses_tableview.setItem(row, 2, QTableWidgetItem(course.section))
        self.swap_enrolled_courses_tableview.setItem(row, 3, QTableWidgetItem(course.instructor))
        self.swap_enrolled_courses_tableview.setItem(row, 4, QTableWidgetItem(course.days))
        self.swap_enrolled_courses_tableview.setItem(row, 5, QTableWidgetItem(str(course.start_time)))
        self.swap_enrolled_courses_tableview.setItem(row, 6, QTableWidgetItem(str(course.end_time)))
        self.swap_enrolled_courses_tableview.setItem(row, 7, QTableWidgetItem(course.room))
        status = "Closed"
        if course.status:
            status = "Open"
        self.swap_enrolled_courses_tableview.setItem(row, 8, QTableWidgetItem(status))

    def can_the_course_be_added(self, course_id, section, start_time, end_time, days):
        # Check if the course is already added
        # for row in range(self.show_selected_schedule_widget.rowCount()):
        #     if self.show_selected_schedule_widget.item(row, 0).text() == course_id \
        #             and self.show_selected_schedule_widget.item(row, 2).text() == section:
        #         print("Course already added")
        #         # Show a warning box
        #         QMessageBox.warning(self, "Warning", "Course already added")
        #         return False
        # for row in range(self.show_selected_schedule_widget.rowCount()):
        #     if self.show_selected_schedule_widget.item(row, 0).text() == course_id:
        #         print("Course already added")
        #         # Show a warning box
        #         QMessageBox.warning(self, "Warning", "Cannot add the same course twice")
        #         return False
        #
        # # Check if the course is already added
        # course = self.all_queries.get_course_by_std_id_and_course_id(course_id)
        # if course is not None:
        #     print("Course already added")
        #     # Show a warning box
        #     QMessageBox.warning(self, "Warning", "Cannot add the same course twice")
        #     return False

        start_timings, end_timings, all_days = self.all_queries.get_timings_of_all_courses_by_id(course_id, section)
        # Get current course start_time and end_time after converting it to time
        start_time_in_seconds = self.all_queries.time_to_seconds(datetime.strptime(start_time, '%H:%M:%S'))
        end_time_in_seconds = self.all_queries.time_to_seconds(datetime.strptime(end_time, '%H:%M:%S'))

        print(f"start_time_in_seconds: {start_time_in_seconds}")
        print(f"end_time_in_seconds: {end_time_in_seconds}")
        print()
        print()

        # Check if the timings clash
        for i in range(len(start_timings)):
            print(f"start_timings[{i}]: {start_timings[i]}")
            print(f"end_timings[{i}]: {end_timings[i]}")
            # if start_datetime.weekday() == end_datetime.weekday() == start_time.weekday():
            days_list = self.all_queries.get_days_list(days)
            previous_days_list = self.all_queries.get_days_list(all_days[i])
            print(f"days_list: {days_list}")
            print(f"previous_days_list: {previous_days_list}")
            print()
            print()
            for day in range(len(days_list)):
                print(f"days_list[{day}]: {days_list[day]}")
                print(f"previous_days_list: {previous_days_list}")
                # if start_datetime.weekday() == end_datetime.weekday() == start_time.weekday():
                if days_list[day] in previous_days_list:
                    if start_timings[i] <= start_time_in_seconds <= end_timings[i]:
                        print("Timings clash")
                        # Show a warning box
                        QMessageBox.warning(self, "Warning", "Timings clash")
                        return False
                    if start_timings[i] <= end_time_in_seconds <= end_timings[i]:
                        print("Timings clash")
                        # Show a warning box
                        QMessageBox.warning(self, "Warning", "Timings clash")
                        return False
                    if start_time_in_seconds <= start_timings[i] and end_time_in_seconds >= end_timings[i]:
                        print("Timings clash")
                        # Show a warning box
                        QMessageBox.warning(self, "Warning", "Timings clash")
                        return False
        return True

    def swap_courses(self):
        print("Swap clicked")

        response = QMessageBox.question(self, "Swap Courses", "Are you sure you want to swap the courses?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.No:
            return

        # Get the selected row from both tables
        selected_row = self.swap_courses_tableview.currentRow()
        selected_row_enrolled = self.swap_enrolled_courses_tableview.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No course selected to swap.")
            return

        if selected_row_enrolled == -1:
            QMessageBox.warning(self, "Error", "No course selected to swap with.")
            return

        # Get the course_id and section from the selected row
        course_id = self.swap_courses_tableview.item(selected_row, 0).text()
        section = self.swap_courses_tableview.item(selected_row, 2).text()
        start_time = self.swap_courses_tableview.item(selected_row, 5).text()
        end_time = self.swap_courses_tableview.item(selected_row, 6).text()
        days = self.swap_courses_tableview.item(selected_row, 4).text()

        # Get the course_id and section from the selected row in the enrolled courses table
        course_id_enrolled = self.swap_enrolled_courses_tableview.item(selected_row_enrolled, 0).text()
        section_enrolled = self.swap_enrolled_courses_tableview.item(selected_row_enrolled, 2).text()

        # if section and course_id same then show messagebox and return
        if course_id != course_id_enrolled:
            QMessageBox.warning(self, "Error", "Cannot swap different courses.")
            return

        if course_id == course_id_enrolled and section == section_enrolled:
            QMessageBox.warning(self, "Error", "Cannot swap the same course.")
            return

        # Check if the course can be added
        if not self.can_the_course_be_added(course_id, section, start_time, end_time, days):
            return

        try:
            # can_be_added = self.all_queries.swap_courses(20180, course_id, section, course_id_enrolled, section_enrolled)
            # can_be_added = self.all_queries.swap_courses(global_std_id, course_id, section, course_id_enrolled, section_enrolled)
            can_be_added = self.all_queries.swap_courses(course_id, section, course_id_enrolled, section_enrolled)
            if not can_be_added:
                QMessageBox.warning(self, "Error", "Course could not be swapped.")
                return
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            print("Return is being called")
            return

        # Remove the enrolled course from the enrolled courses table
        self.swap_enrolled_courses_tableview.removeRow(selected_row_enrolled)

        # Add the course to the enrolled courses table
        course = self.all_queries.get_course_by_id_and_section(course_id, section)
        self.fill_swap_enrolled_courses_tableview_with_course(course)

        # Add course_id_enrolled capacity
        is_capacity = self.all_queries.update_current_capacity(course_id_enrolled, section_enrolled, "Add")
        if not is_capacity:
            QMessageBox.warning(self, "Capacity", "Invalid capacity")
            return

        # Subtract course_id capacity
        is_capacity = self.all_queries.update_current_capacity(course_id, section, "Subtract")
        if not is_capacity:
            QMessageBox.warning(self, "Capacity", "Invalid capacity")
            return

        previous_course_id_new_course_id = f"{course_id_enrolled} -> {course_id}"
        previous_section_new_section = f"{section_enrolled} -> {section}"

        self.fill_swap_courses_tableview(self.all_queries.get_all_courses())

        # Add to activity log
        self.all_queries.add_data_to_activity_log(course_id=previous_course_id_new_course_id,
                                                  std_id=self.all_queries.get_std_id(),
                                                  activity_type="Swap",
                                                  section=previous_section_new_section)

    def enroll(self):
        print("Enroll clicked")

    def select_courses(self):
        print("Select clicked")
        # Get the selected row
        selected_row = self.swap_courses_tableview.currentRow()

        course_id = self.swap_courses_tableview.item(selected_row, 0).text()
        section = self.swap_courses_tableview.item(selected_row, 2).text()

        # all_enrolled_courses = self.all_queries.get_all_courses_by_std_id_and_course_id(20180, course_id)
        # all_enrolled_courses = self.all_queries.get_all_courses_by_std_id_and_course_id(global_std_id, course_id)
        all_enrolled_courses = self.all_queries.get_all_courses_by_std_id_and_course_id(course_id)
        if len(all_enrolled_courses) > 0:
            self.fill_swap_enrolled_courses_tableview(all_enrolled_courses)
        else:
            self.swap_enrolled_courses_tableview.clearContents()
            QMessageBox.warning(self, "Error", "No course can be swapped with the current course.")
            # Clear the content of the second table
            return

    def reopen_login(self):
        self.show()

    def closeEvent(self, event):
        print("User has clicked the red 'x' on the swap courses window")
        # Here you can accept or ignore the event to close the window
        # super().closeEvent(event)
        self.closed.emit()


if __name__ == "__main__":
    app = QApplication([])
    window = SwapCoursesWindow()
    window.show()
    app.exec()
