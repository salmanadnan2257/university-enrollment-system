import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import pyqtSignal
from PyQt6 import uic
from add_courses import AddCoursesWindow
from drop_courses import DropCoursesWindow
from queries import AllQueries
from view_schedule import ViewScheduleWindow
from swap_courses import SwapCoursesWindow
from activity_log import ActivityLogWindow
from attendance import AttendanceForm


class MainStudentWindow(QMainWindow):
    closed = pyqtSignal()

    # def __init__(self):
    def __init__(self, email=None):
        super().__init__()

        # Load the UI file
        uic.loadUi('main_window.ui', self)

        if email is None:
            self.email = "alice20180@st.habib.edu.pk"
        else:
            self.email = email
        
        # Define std_email and std_id so we can pass them around
        self.std_id = self.get_student_id_by_email(self.email)

        # Find the label by its name
        enrollment_label = self.findChild(QLabel, 'label')
        self.all_queries = AllQueries()
        self.all_queries.update_std_id(self.all_queries.get_std_id_by_email(self.email))

        self.should_go_back = False

        # Set the label font to bold
        font = enrollment_label.font()
        font.setBold(True)
        enrollment_label.setFont(font)

        # Connect the button clicks to their respective methods
        self.view_attendance.clicked.connect(self.handle_view_attendance)
        self.add_courses_button.clicked.connect(self.add_courses)
        self.drop_courses_button.clicked.connect(self.drop_courses)
        self.view_schedule_button.clicked.connect(self.view_schedule)
        self.swap_course_button.clicked.connect(self.swap_course)
        self.logout_button.clicked.connect(self.logout)
        self.activity_log_button.clicked.connect(self.activity_log)

        # app.aboutToQuit.connect(self.close_event)

    def handle_view_attendance(self):
        # Open the AttendanceForm
        self.attendance_window = AttendanceForm(
            parent=self,
            std_email=self.email,
            std_id=self.std_id
        )
        self.attendance_window.show()

    def get_student_id_by_email(self, email):
        # Example logic or call to queries:
        all_q = AllQueries()
        return all_q.get_std_id_by_email(email)
    
    def swap_course(self):
        print("Swap Course clicked")
        self.swap_courses_window = SwapCoursesWindow(email=self.email)
        self.swap_courses_window.show()
        self.hide()
        self.swap_courses_window.closed.connect(self.reopen_login)

    def add_courses(self):
        print("Create/Edit Timetable clicked")
        # self.add_courses_window = AddCoursesWindow()
        self.add_courses_window = AddCoursesWindow(email=self.email)
        self.add_courses_window.show()
        self.hide()
        self.add_courses_window.closed.connect(self.reopen_login)

    def drop_courses(self):
        print("Create/Edit Timetable clicked")
        # self.drop_courses_window = DropCoursesWindow()
        self.drop_courses_window = DropCoursesWindow(email=self.email)
        self.drop_courses_window.show()
        self.hide()
        self.drop_courses_window.closed.connect(self.reopen_login)

    def view_schedule(self):
        print("View Schedule clicked")
        # self.view_schedule_window = ViewScheduleWindow()
        self.view_schedule_window = ViewScheduleWindow(email=self.email)
        self.view_schedule_window.show()
        self.hide()
        self.view_schedule_window.closed.connect(self.reopen_login)

    def activity_log(self):
        print("Activity Log clicked")
        self.activity_log_window = ActivityLogWindow()
        self.activity_log_window = ActivityLogWindow(email=self.email)
        self.activity_log_window.show()
        self.hide()
        self.activity_log_window.closed.connect(self.reopen_login)

    def logout(self):
        print("Logout clicked")
        self.should_go_back = True
        # self.closed.emit()
        self.closeEvent(event=None)

    def reopen_login(self):
        self.show()

    def closeEvent(self, event):
        print("User has clicked the red 'x' on the main window")
        # Here you can accept or ignore the event to close the window
        # super().closeEvent(event)
        if not self.should_go_back:
            # sys.exit()
            # pass
            self.close()
        else:
            print("Going back to login page")
            self.should_go_back = False
            self.close()
            self.closed.emit()



if __name__ == "__main__":
    app = QApplication([])
    window = MainStudentWindow()
    window.show()
    app.exec()

# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
# from PyQt6 import uic
#
#
# class MainStudentWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # Load the UI file
#         uic.loadUi('main_window.ui', self)
#
#         # Connect the button clicks to their respective methods
#         self.create_edit_timetable_button.clicked.connect(self.create_edit_timetable)
#         self.view_schedule_button.clicked.connect(self.view_schedule)
#         self.swap_course_button.clicked.connect(self.swap_course)
#         self.logout_button.clicked.connect(self.logout)
#         self.activity_log_button.clicked.connect(self.activity_log)
#
#         app.aboutToQuit.connect(self.close_event)
#
#     def create_edit_timetable(self):
#         print("Create/Edit Timetable clicked")
#
#     def view_schedule(self):
#         print("View Schedule clicked")
#
#     def swap_course(self):
#         print("Swap Course clicked")
#
#     def logout(self):
#         print("Logout clicked")
#
#     def activity_log(self):
#         print("Activity Log clicked")
#
#     def close_event(self):
#         print("User has clicked the red x on the main window")
#         # event.accept()
#
#
# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainStudentWindow()
#     window.show()
#     app.exec()
