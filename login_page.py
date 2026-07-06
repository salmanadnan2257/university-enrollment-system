import os
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QMessageBox

from main_window import MainStudentWindow
from queries import AllQueries
from verification import VerificationForm

class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        global global_std_id

        # Load the UI file
        uic.loadUi('login_page.ui', self)

        # Find the label by its name
        login_label = self.findChild(QLabel, 'login_screen_label')

        # Set the label font to bold
        font = login_label.font()
        font.setBold(True)
        font.setUnderline(True)
        login_label.setFont(font)
        self.all_queries = AllQueries()

        # Connect the button click to the handle_login method
        self.login_button.clicked.connect(self.handle_login)

        # Add a button to show/hide the password
        # self.show_hide_button = QPushButton("Show/Hide Password", self)
        self.show_hide_button.clicked.connect(self.toggle_password_visibility)
        # self.show_hide_button.setGeometry(90, 220, 201, 21)

        # Set initial state for password visibility
        self.password_visible = False
        self.toggle_password_visibility()
        # self.show_hide_button.click()

        # self.set_background()
        # app.aboutToQuit.connect(self.close_event)

    def handle_login(self):
        # Get the values from the textboxes
        # user_id = self.user_id_textbox.text()
        email = self.email_textbox.text()
        password = self.password_textbox.text()

        # if (email == '') and (password == ''):
        # current_user_id = 20180
        # user_email, user_password = self.all_queries.email_and_password(current_user_id)
        # print("Email is", email)
        # print("Password is", password)
        # print("Email ID is", user_email)
        # print("Password is", password)
        # if (email.lower() == user_email.lower()) and (password == user_password):
        # Get password by email
        user_password = self.all_queries.get_password_by_email(email)
        if user_password is None:
            print("Wrong credentials")
            QMessageBox.critical(self, "Error", "Wrong credentials")
            return
        if password == user_password:
            # Instead of directly opening MainStudentWindow,
            # we now open the VerificationForm (for MFA)
            self.verification_window = VerificationForm(self, email)
            self.verification_window.show()
            self.hide()
        else:
            print("Wrong credentials")
            QMessageBox.critical(self, "Error", "Wrong credentials")

    def toggle_password_visibility(self):
        # Toggle password visibility
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.show_hide_button.setText("Show")
            self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.show_hide_button.setText("Hide")
            self.password_textbox.setEchoMode(QLineEdit.EchoMode.Normal)

    def set_background(self):
        # Set a background image using a stylesheet
        pixmap = os.path.join(sys.path[0], "HU Banner.jpeg")
        print(sys.path[0])
        self.setStyleSheet(f"background-image: url({pixmap});"
                            # f"background-position: center;"
                            # f"background-repeat: no-repeat;"
                            f"background-color: transparent;")

    def closeEvent(self, event):
        print("Exiting the application")
        print("User has clicked the red x on the login page window")
        # event.accept()

    def reopen_login(self):
        # Clear the textboxes
        self.email_textbox.setText("")
        self.password_textbox.setText("")
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = LoginForm()
    window.show()
    app.exec()
