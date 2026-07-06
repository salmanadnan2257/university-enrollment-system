# verification.py

import os
import random
import smtplib

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from queries import AllQueries
from main_window import MainStudentWindow


class VerificationForm(QMainWindow):
    def __init__(self, login_parent, email):
        """
        :param login_parent: The instance of LoginForm that spawned this verification step.
        :param email: The user’s email (already verified for existence in login_page).
        """
        super().__init__(login_parent)
        uic.loadUi('verification.ui', self)

        self.login_parent = login_parent
        self.email = email
        self.all_queries = AllQueries()

        # 1) Generate a 6-digit code
        self.verification_code = str(random.randint(100000, 999999))

        # 2) Send code via SMTP
        self.send_verification_email()

        # 3) Connect the "Verify" button
        #    Make sure your verification.ui has an objectName called "verify_button"
        self.verify_button.clicked.connect(self.handle_verification)

    def send_verification_email(self):
        """
        Sends the six-digit code (self.verification_code) to self.email.
        Uses basic SMTP with TLS. You must fill in your own credentials below.
        """
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.environ.get("ATTENDANCE_SENDER_EMAIL", "")
        sender_password = os.environ.get("ATTENDANCE_SENDER_PASSWORD", "")

        if not sender_email or not sender_password:
            # No SMTP credentials configured. Don't attempt to send; fall back
            # to printing the code so the demo login still works.
            print(f"[WARN] ATTENDANCE_SENDER_EMAIL / ATTENDANCE_SENDER_PASSWORD not set. "
                  f"Verification code (demo fallback): {self.verification_code}")
            QMessageBox.warning(
                self, "Email Not Configured",
                "Email sending is not configured (set ATTENDANCE_SENDER_EMAIL and "
                "ATTENDANCE_SENDER_PASSWORD).\nFor this demo, the verification code "
                "was printed to the terminal instead."
            )
            return

        subject = "Your Verification Code"
        body = (
            f"Hello,\n\n"
            f"Your verification code is: {self.verification_code}\n\n"
            "Enter this code in the application to complete your login.\n"
        )

        # Basic plain-text email format:
        message = f"Subject: {subject}\n\n{body}"

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, self.email, message)
            print(f"[INFO] Verification code {self.verification_code} sent to {self.email}")
        except Exception as e:
            print("Error sending verification code:", e)
            QMessageBox.critical(self, "Error", "Could not send verification email. Please try again.")
            self.close()

    def handle_verification(self):
        """
        Triggered when user clicks "Verify". Checks the input vs. self.verification_code.
        If correct, open MainStudentWindow. Otherwise, prompt to try again.
        """
        # The QLineEdit in verification.ui is assumed to be named "verification_textbox"
        entered_code = self.verification_textbox.text().strip()

        if entered_code == self.verification_code:
            QMessageBox.information(self, "Success", "Verification successful!")

            # Load the main student window
            self.main_student_window = MainStudentWindow(email=self.email)
            self.main_student_window.show()

            # Update your global ID logic
            self.all_queries.glob_id = self.all_queries.get_std_id_by_email(self.email)
            self.all_queries.update_std_id(self.all_queries.glob_id)
            print("self.all_queries.glob_id: " + str(self.all_queries.glob_id))

            # If you want the main window to be able to reopen the login after it’s closed:
            self.main_student_window.closed.connect(self.login_parent.reopen_login)

            # Hide the verification window
            self.hide()
        else:
            QMessageBox.critical(self, "Error", "Wrong code! Please try again.")
            self.verification_textbox.clear()
