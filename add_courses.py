import sys
import traceback
from datetime import datetime

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QVBoxLayout, QWidget, \
    QTableWidgetItem, QMessageBox
from PyQt6 import uic
from enroll import ViewScheduleWindow
from queries import AllQueries


# from login_page import global_std_id


class AddCoursesWindow(QMainWindow):
    closed = pyqtSignal()

    # def __init__(self):
    def __init__(self, email=None):
        super().__init__()

        # Load the UI file
        uic.loadUi('add_courses.ui', self)

        if email is None:
            self.email = "alice20180@st.habib.edu.pk"
        else:
            self.email = email

        # Find the label by its name
        shopping_cart_label = self.findChild(QLabel, 'schedule_label')
        self.all_queries = AllQueries()
        self.all_queries.update_std_id(self.all_queries.get_std_id_by_email(self.email))

        # Set the label font to bold
        font = shopping_cart_label.font()
        font.setBold(True)
        shopping_cart_label.setFont(font)

        # Set the table to be non-editable
        self.schedule_table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.show_selected_schedule_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Connect the button clicks to their respective methods
        self.add_button.clicked.connect(self.add_course)
        self.remove_button.clicked.connect(self.remove_course)
        self.enroll_button.clicked.connect(self.enroll)

        # Set up the course lists
        self.setup_course_lists()

    def setup_course_lists(self):
        # Set column headers for the course lists
        headers = ["Course ID", "Course Name", "Section", "Instructor", "Days", "Start Time", "End Time", "Room",
                   "Status"]
        self.schedule_table_widget.setColumnCount(len(headers))
        self.schedule_table_widget.setHorizontalHeaderLabels(headers)

        self.show_selected_schedule_widget.setColumnCount(len(headers))
        self.show_selected_schedule_widget.setHorizontalHeaderLabels(headers)

        self.show_all_courses()
        self.show_selected_courses()

    def show_all_courses(self):
        self.schedule_table_widget.clearContents()
        self.schedule_table_widget.setRowCount(0)

        all_courses = self.all_queries.get_all_courses()
        # fill in the details in appropriate columns in schedule_table_widget
        for course in all_courses:
            if not course.status or self.all_queries.is_user_enrolled_in_this_course(course_id=course.course_list_id,
                                                                                     section=course.section):
                continue

            # Get the row number
            row = self.schedule_table_widget.rowCount()
            # Insert a new row at the bottom
            self.schedule_table_widget.insertRow(row)
            # Set the course id
            self.schedule_table_widget.setItem(row, 0, QTableWidgetItem(str(course.course_list_id)))
            # Set the course name
            self.schedule_table_widget.setItem(row, 1, QTableWidgetItem(course.course_name))
            # Set the section
            self.schedule_table_widget.setItem(row, 2, QTableWidgetItem(course.section))
            # Set the instructor
            self.schedule_table_widget.setItem(row, 3, QTableWidgetItem(course.instructor))
            # Set the days
            self.schedule_table_widget.setItem(row, 4, QTableWidgetItem(course.days))
            # Set the start time
            self.schedule_table_widget.setItem(row, 5, QTableWidgetItem(str(course.start_time)))
            # Set the end time
            self.schedule_table_widget.setItem(row, 6, QTableWidgetItem(str(course.end_time)))
            # Set the room
            self.schedule_table_widget.setItem(row, 7, QTableWidgetItem(course.room))
            # Set the status
            status = "Closed"
            if course.status:
                status = "Open"
            self.schedule_table_widget.setItem(row, 8, QTableWidgetItem(status))

        # Sort by course_id
        self.schedule_table_widget.sortItems(0)

    def show_selected_courses(self):
        # Clear the content of the table
        self.show_selected_schedule_widget.clearContents()
        self.show_selected_schedule_widget.setRowCount(0)

        # all_courses = self.all_queries.get_all_courses_by_id_and_type(20180, "Add")
        # all_courses = self.all_queries.get_all_courses_by_id_and_type(global_std_id, "Add")
        all_courses = self.all_queries.get_all_courses_by_id_and_type("Add")

        # fill in the details in appropriate columns in schedule_table_widget
        for course in all_courses:
            course_list = self.all_queries.get_course_by_id_and_section(course.course_id, course.section)

            row = self.show_selected_schedule_widget.rowCount()
            self.show_selected_schedule_widget.insertRow(row)
            self.show_selected_schedule_widget.setItem(row, 0, QTableWidgetItem(str(course_list.course_list_id)))
            self.show_selected_schedule_widget.setItem(row, 1, QTableWidgetItem(course_list.course_name))
            self.show_selected_schedule_widget.setItem(row, 2, QTableWidgetItem(course_list.section))
            self.show_selected_schedule_widget.setItem(row, 3, QTableWidgetItem(course_list.instructor))
            self.show_selected_schedule_widget.setItem(row, 4, QTableWidgetItem(course_list.days))
            self.show_selected_schedule_widget.setItem(row, 5, QTableWidgetItem(str(course_list.start_time)))
            self.show_selected_schedule_widget.setItem(row, 6, QTableWidgetItem(str(course_list.end_time)))
            self.show_selected_schedule_widget.setItem(row, 7, QTableWidgetItem(course_list.room))
            status = "Closed"
            if course_list.status:
                status = "Open"
            self.show_selected_schedule_widget.setItem(row, 8, QTableWidgetItem(status))

    def can_the_course_be_added(self, course_id, start_time, end_time, days):
        # Check if the course is already added
        # for row in range(self.show_selected_schedule_widget.rowCount()):
        #     if self.show_selected_schedule_widget.item(row, 0).text() == course_id \
        #             and self.show_selected_schedule_widget.item(row, 2).text() == section:
        #         print("Course already added")
        #         # Show a warning box
        #         QMessageBox.warning(self, "Warning", "Course already added")
        #         return False
        for row in range(self.show_selected_schedule_widget.rowCount()):
            if self.show_selected_schedule_widget.item(row, 0).text() == course_id:
                print("Course already added")
                # Show a warning box
                QMessageBox.warning(self, "Warning", "Cannot add the same course twice")
                return False

        # Check if the course is already added
        course = self.all_queries.get_course_by_std_id_and_course_id(course_id)
        if course is not None:
            print("Course already added")
            # Show a warning box
            QMessageBox.warning(self, "Warning", "Cannot add the same course twice")
            return False

        start_timings, end_timings, all_days = self.all_queries.get_days_timings_of_all_courses_by_id_temp_false()
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
            for day in range(len(days_list)):
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

    def add_course(self):
        print("Add Course clicked")
        selected_row = self.schedule_table_widget.currentRow()
        print(selected_row)
        course_id = self.schedule_table_widget.item(selected_row, 0).text()
        section = self.schedule_table_widget.item(selected_row, 2).text()

        # # Check if the course is already added
        # for row in range(self.show_selected_schedule_widget.rowCount()):
        #     if self.show_selected_schedule_widget.item(row, 0).text() == course_id \
        #             and self.show_selected_schedule_widget.item(row, 2).text() == section:
        #         print("Course already added")
        #         # Show a warning box
        #         QMessageBox.warning(self, "Warning", "Course already added")
        #         return

        start_time = self.schedule_table_widget.item(selected_row, 5).text()
        end_time = self.schedule_table_widget.item(selected_row, 6).text()
        days = self.schedule_table_widget.item(selected_row, 4).text()
        can_course_be_added = self.can_the_course_be_added(course_id, start_time, end_time, days)
        status = self.schedule_table_widget.item(selected_row, 8).text()

        if status == "Closed":
            print("Course is closed")
            # Show a warning box
            QMessageBox.warning(self, "Warning", "Course is closed")
            return

        if not can_course_be_added:
            return

        course_name = self.schedule_table_widget.item(selected_row, 1).text()
        instructor = self.schedule_table_widget.item(selected_row, 3).text()
        days = self.schedule_table_widget.item(selected_row, 4).text()
        start_time = self.schedule_table_widget.item(selected_row, 5).text()
        end_time = self.schedule_table_widget.item(selected_row, 6).text()
        room = self.schedule_table_widget.item(selected_row, 7).text()

        try:
            # does_it_work = self.all_queries.add_course(20180, int(course_id), section)
            # does_it_work = self.all_queries.add_course(global_std_id, int(course_id), section)
            does_it_work = self.all_queries.add_course(int(course_id), section)
            if not does_it_work:
                print("Course could not be added")
                # Show a warning box
                QMessageBox.warning(self, "Warning", "Course could not be added")
                return
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            print("Return is being called")
            return

        print("Adding the course to show_selected_schedule_widget")
        row = self.show_selected_schedule_widget.rowCount()
        self.show_selected_schedule_widget.insertRow(row)
        self.show_selected_schedule_widget.setItem(row, 0, QTableWidgetItem(course_id))
        self.show_selected_schedule_widget.setItem(row, 1, QTableWidgetItem(course_name))
        self.show_selected_schedule_widget.setItem(row, 2, QTableWidgetItem(section))
        self.show_selected_schedule_widget.setItem(row, 3, QTableWidgetItem(instructor))
        self.show_selected_schedule_widget.setItem(row, 4, QTableWidgetItem(days))
        self.show_selected_schedule_widget.setItem(row, 5, QTableWidgetItem(start_time))
        self.show_selected_schedule_widget.setItem(row, 6, QTableWidgetItem(end_time))
        self.show_selected_schedule_widget.setItem(row, 7, QTableWidgetItem(room))
        self.show_selected_schedule_widget.setItem(row, 8, QTableWidgetItem(status))

        # # Update capacity
        # is_capacity = self.all_queries.update_current_capacity(course_id, section, "Subtract")
        # if not is_capacity:
        #     QMessageBox.warning(self, "Capacity", "Invalid capacity")
        #     return

        # Add to activity log
        self.all_queries.add_data_to_activity_log(course_id=course_id, std_id=self.all_queries.get_std_id(),
                                                  activity_type="Add", section=section)

    def remove_course(self):
        print("Remove Course clicked")
        selected_row = self.show_selected_schedule_widget.currentRow()
        print(selected_row)
        course_id = self.show_selected_schedule_widget.item(selected_row, 0).text()
        section = self.show_selected_schedule_widget.item(selected_row, 2).text()

        try:
            # does_it_work = self.all_queries.remove_course(20180, int(course_id), section)
            # does_it_work = self.all_queries.remove_course(global_std_id, int(course_id), section)
            does_it_work = self.all_queries.remove_course(int(course_id), section)
            if not does_it_work:
                print("Course could not be removed")
                # Show a warning box
                QMessageBox.warning(self, "Warning", "Course could not be removed")
                return
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            return

        self.show_selected_schedule_widget.removeRow(selected_row)

        self.all_queries.add_data_to_activity_log(course_id=course_id, std_id=self.all_queries.get_std_id(),
                                                  activity_type="Remove", section=section)

    def enroll(self):
        print("Next clicked")
        self.view_schedule_window = ViewScheduleWindow(email=self.email)
        self.view_schedule_window.show()
        self.hide()
        self.view_schedule_window.closed.connect(self.reopen_login)

    def reopen_login(self):
        self.show()
        self.show_all_courses()
        self.show_selected_courses()

    def closeEvent(self, event):
        print("User has clicked the red 'x' on the create timetable window")
        # Here you can accept or ignore the event to close the window
        # super().closeEvent(event)
        self.closed.emit()


if __name__ == "__main__":
    app = QApplication([])
    window = AddCoursesWindow()
    window.show()
    app.exec()
