import os
import sys

import pandas
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QVBoxLayout, QWidget, \
    QTableWidgetItem, QMessageBox
from PyQt6 import uic

from queries import AllQueries


class ViewScheduleWindow(QMainWindow):
    closed = pyqtSignal()

    # def __init__(self):
    def __init__(self, email=None):
        super().__init__()

        # Load the UI file
        uic.loadUi('view_schedule.ui', self)

        # Set the table to be non-editable
        self.schedule_table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        if email is None:
            self.email = "alice20180@st.habib.edu.pk"
        else:
            self.email = email

        # Find the label by its name
        schedule_label = self.findChild(QLabel, 'schedule_label')

        # Set the label font to bold
        font = schedule_label.font()
        font.setBold(True)
        schedule_label.setFont(font)

        self.filter_mode = "Day"

        self.all_queries = AllQueries()
        self.all_queries.update_std_id(self.all_queries.get_std_id_by_email(self.email))

        # Add to activity log
        self.all_queries.add_data_to_activity_log(std_id=self.all_queries.get_std_id(),
                                                  activity_type="Filter by Day")

        # Connect the button clicks to their respective methods
        self.day_button.clicked.connect(self.filter_by_day)
        self.week_button.clicked.connect(self.filter_by_week)
        self.export_button.clicked.connect(self.export_schedule)

        # Set up the schedule table
        self.setup_schedule_table()

    def setup_schedule_table(self):
        # Set column headers for the schedule table
        headers = ["Current Day", "Course ID", "Course Name", "Section", "Instructor", "Days", "Start Time", "End Time",
                   "Room",
                   "Status"]
        self.schedule_table_widget.setColumnCount(len(headers))
        self.schedule_table_widget.setHorizontalHeaderLabels(headers)

        # all_enrolled_courses = self.all_queries.get_all_courses_by_id(20180)
        # all_enrolled_courses = self.all_queries.get_all_courses_by_id(global_std_id)
        all_enrolled_courses = self.all_queries.get_all_courses_by_id()
        self.show_setup_schedule_table(all_enrolled_courses)

    def show_setup_schedule_table(self, all_enrolled_courses):
        # Empty the tableview
        self.schedule_table_widget.clearContents()
        self.schedule_table_widget.setRowCount(0)

        # Show the current day column
        self.schedule_table_widget.showColumn(0)

        # Set the number of rows in the tableview
        # self.schedule_table_widget.setRowCount(len(all_enrolled_courses))

        # Current Day
        current_day = self.all_queries.get_current_day()

        # Fill the tableview with the courses
        for row, course in enumerate(all_enrolled_courses):
            print("row: " + str(row))
            print("type(row): " + str(type(row)))
            course_list = self.all_queries.get_course_by_id_and_section(course.course_id, course.section)
            course_days_list = self.all_queries.get_days_list(course_list.days)
            if current_day[:2] not in course_days_list:
                continue

            # Insert row
            self.schedule_table_widget.insertRow(self.schedule_table_widget.rowCount())

            current_row = self.schedule_table_widget.rowCount() - 1
            print("current_row: " + str(current_row))

            self.schedule_table_widget.setItem(current_row, 0, QTableWidgetItem(current_day))
            self.schedule_table_widget.setItem(current_row, 1, QTableWidgetItem(str(course_list.course_list_id)))
            print("course_list.course_list_id: " + str(course_list.course_list_id))
            self.schedule_table_widget.setItem(current_row, 2, QTableWidgetItem(course_list.course_name))
            self.schedule_table_widget.setItem(current_row, 3, QTableWidgetItem(course_list.section))
            self.schedule_table_widget.setItem(current_row, 4, QTableWidgetItem(course_list.instructor))
            self.schedule_table_widget.setItem(current_row, 5, QTableWidgetItem(course_list.days))
            self.schedule_table_widget.setItem(current_row, 6, QTableWidgetItem(str(course_list.start_time)))
            self.schedule_table_widget.setItem(current_row, 7, QTableWidgetItem(str(course_list.end_time)))
            self.schedule_table_widget.setItem(current_row, 8, QTableWidgetItem(course_list.room))
            status = "Closed"
            if course_list.status:
                status = "Open"
            self.schedule_table_widget.setItem(current_row, 9, QTableWidgetItem(status))

        # # Show rows that have a course id and is not none and hide the rest
        # for row in range(self.schedule_table_widget.rowCount()):
        #     if self.schedule_table_widget.item(row, 1) is not None:
        #         self.schedule_table_widget.showRow(row)
        #     else:
        #         self.schedule_table_widget.hideRow(row)

    def show_setup_schedule_table_by_week(self, all_enrolled_courses):
        # Empty the tableview
        self.schedule_table_widget.clearContents()
        self.schedule_table_widget.setRowCount(0)

        # Hide the current day column
        self.schedule_table_widget.hideColumn(0)

        # # Set the number of rows in the tableview
        self.schedule_table_widget.setRowCount(len(all_enrolled_courses))

        # Fill the tableview with the courses
        for row, course in enumerate(all_enrolled_courses):
            course_list = self.all_queries.get_course_by_id_and_section(course.course_id, course.section)
            # self.schedule_table_widget.setItem(row, 0, QTableWidgetItem("Monday"))
            self.schedule_table_widget.setItem(row, 1, QTableWidgetItem(str(course_list.course_list_id)))
            self.schedule_table_widget.setItem(row, 2, QTableWidgetItem(course_list.course_name))
            self.schedule_table_widget.setItem(row, 3, QTableWidgetItem(course_list.section))
            self.schedule_table_widget.setItem(row, 4, QTableWidgetItem(course_list.instructor))
            self.schedule_table_widget.setItem(row, 5, QTableWidgetItem(course_list.days))
            self.schedule_table_widget.setItem(row, 6, QTableWidgetItem(str(course_list.start_time)))
            self.schedule_table_widget.setItem(row, 7, QTableWidgetItem(str(course_list.end_time)))
            self.schedule_table_widget.setItem(row, 8, QTableWidgetItem(course_list.room))
            status = "Closed"
            if course_list.status:
                status = "Open"
            self.schedule_table_widget.setItem(row, 9, QTableWidgetItem(status))

    def filter_by_day(self):
        print("Filter by Day clicked")
        all_enrolled_courses = self.all_queries.get_all_courses_by_id()
        self.show_setup_schedule_table(all_enrolled_courses)

        self.filter_mode = "Day"

        # Add to activity log
        self.all_queries.add_data_to_activity_log(std_id=self.all_queries.get_std_id(),
                                                  activity_type="Filter by Day")

    def filter_by_week(self):
        print("Filter by Week clicked")

        all_enrolled_courses = self.all_queries.get_all_courses_by_id()
        self.show_setup_schedule_table_by_week(all_enrolled_courses)

        self.filter_mode = "Week"

        # Add to activity log
        self.all_queries.add_data_to_activity_log(std_id=self.all_queries.get_std_id(),
                                                  activity_type="Filter by Week")

    def export_schedule(self):
        print("Export Schedule clicked")

        # All columns of the table
        if self.filter_mode == "Day":
            columns = ["Current Day", "Course ID", "Course Name", "Section", "Instructor", "Days", "Start Time",
                       "End Time", "Room", "Status"]
            QMessageBox.information(self, "Export Not Available", "Exporting the day schedule is not available.")
            return
        else:
            columns = ["Course ID", "Course Name", "Section", "Instructor", "Days", "Start Time",
                       "End Time", "Room", "Status"]

        print()
        print()
        print("self.schedule_table_widget.columnCount(): " + str(self.schedule_table_widget.columnCount()))
        print("self.schedule_table_widget.rowCount(): " + str(self.schedule_table_widget.rowCount()))

        visible_column_count = 0
        for column in range(self.schedule_table_widget.columnCount()):
            if not self.schedule_table_widget.isColumnHidden(column):
                visible_column_count += 1

        print("visible_column_count: " + str(visible_column_count))

        # Get the data from the table in 2D List
        data = []
        for row in range(self.schedule_table_widget.rowCount()):
            data.append([])
            for column in range(1, visible_column_count + 1):
                data[row].append(self.schedule_table_widget.item(row, column).text())

        print("columns: " + str(columns))
        print("data: " + str(data))

        if self.filter_mode == "Day":
            QMessageBox.information(self, "Export Not Available", "Exporting the day schedule is not available.")
            return 
        else:
            excel_file_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/schedule_by_week.xlsx'
        schedule_pandas = pandas.DataFrame(data=data, columns=columns)
        self.save_data(excel_file_path, schedule_pandas)

        # Add to activity log
        self.all_queries.add_data_to_activity_log(std_id=self.all_queries.get_std_id(),
                                                  activity_type="Export Schedule")

    def save_data(self, excel_file_path, df):
        is_file_found = False
        counter = 0
        name = excel_file_path.split('/')[-1].split('.')[:-1]
        name = '.'.join(name)
        print(name)
        while not is_file_found:
            # Check if the file exists
            try:
                pandas.read_excel(excel_file_path)
                counter += 1
                excel_file_path = excel_file_path.split('/')[:-1]
                excel_file_path = '/'.join(excel_file_path) + f'/{name} ({counter}).xlsx'
            except FileNotFoundError:
                # If it doesn't exist, save the file
                print('entered')
                df.to_excel(excel_file_path, index=False)
                is_file_found = True

    def reopen_login(self):
        self.show()

    def closeEvent(self, event):
        print("User has clicked the red 'x' on the view schedule window")
        # Here you can accept or ignore the event to close the window
        # super().closeEvent(event)
        self.closed.emit()


if __name__ == "__main__":
    app = QApplication([])
    window = ViewScheduleWindow()
    window.show()
    app.exec()