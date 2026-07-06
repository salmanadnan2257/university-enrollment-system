from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal

from queries import AllQueries


class ActivityLogWindow(QMainWindow):
    closed = pyqtSignal()

    # def __init__(self):
    def __init__(self, email=None):
        super().__init__()

        # Load the UI file
        uic.loadUi('activity_log.ui', self)

        if email is None:
            self.email = "alice20180@st.habib.edu.pk"
        else:
            self.email = email

        self.all_queries = AllQueries()
        self.all_queries.update_std_id(self.all_queries.get_std_id_by_email(self.email))

        # Find the label by its name
        activity_log_label = self.findChild(QLabel, 'activity_log_label')

        # Set the label font to bold
        font = activity_log_label.font()
        font.setBold(True)
        activity_log_label.setFont(font)

        # Set up the activity log table
        self.setup_activity_log_table()

    def setup_activity_log_table(self):
        # Set column headers for the activity log table
        headers = ["Activity ID", "Activity Name", "Course ID", "Section", "Date", "Time"]
        self.activity_label_table_widget.setColumnCount(len(headers))
        self.activity_label_table_widget.setHorizontalHeaderLabels(headers)

        # Set the table to be non-editable
        self.activity_label_table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Add all the data from activity log table to the table widget
        all_activity_log_data = self.all_queries.get_activity_by_std_id()
        self.activity_label_table_widget.setRowCount(len(all_activity_log_data))

        for row, activity_log_data in enumerate(all_activity_log_data):
            self.activity_label_table_widget.setItem(row, 0, QTableWidgetItem(str(activity_log_data.activity_id)))
            self.activity_label_table_widget.setItem(row, 1, QTableWidgetItem(activity_log_data.activity_type))
            if activity_log_data.course_id is not None and activity_log_data.course_section is not None:
                # self.activity_label_table_widget.setItem(row, 2, QTableWidgetItem("None"))
                self.activity_label_table_widget.setItem(row, 2, QTableWidgetItem(str(activity_log_data.course_id)))
            self.activity_label_table_widget.setItem(row, 3, QTableWidgetItem(activity_log_data.course_section))
            self.activity_label_table_widget.setItem(row, 4, QTableWidgetItem(str(activity_log_data.activity_date)))
            self.activity_label_table_widget.setItem(row, 5, QTableWidgetItem(str(activity_log_data.activity_time)))

    def reopen_login(self):
        self.show()

    def closeEvent(self, event):
        print("User has clicked the red 'x' on the activity log window")
        # Here you can accept or ignore the event to close the window
        # super().closeEvent(event)
        self.closed.emit()


if __name__ == "__main__":
    app = QApplication([])
    window = ActivityLogWindow()
    window.show()
    app.exec()
