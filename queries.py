import datetime
import sys
import traceback

from student_database import session, Student, CourseList, Course, Activity


class AllQueries:
    def __init__(self):
        self.glob_id = 20180

    # def email_and_password(self, std_id):
    def email_and_password(self):
        std_id = self.glob_id
        student = session.query(Student).filter_by(std_id=std_id).first()
        return student.email, student.password

    def get_std_id(self):
        return self.glob_id

    def get_std_id_by_email(self, email):
        student = session.query(Student).filter_by(email=email).first()
        return student.std_id

    def get_password_by_email(self, email):
        student = session.query(Student).filter_by(email=email).first()
        if student is None:
            return None
        return student.password

    def get_course_by_id(self, course_id):
        # Get the course from course_list
        course = session.query(CourseList).filter_by(course_list_id=course_id).first()
        return course

    def update_std_id(self, std_id):
        # main_glob_id = std_id
        self.glob_id = std_id

    def get_current_day(self):
        # Get the current day
        current_day = datetime.datetime.now().strftime("%A")
        return current_day

    def get_all_courses(self):
        # Get all the courses from course_list
        course_list = session.query(CourseList).all()
        return course_list

    def get_course_by_std_id_and_course_id(self, course_id):
        std_id = self.glob_id
        print()
        print()
        print(f"std_id: {std_id}\ncourse_id: {course_id}")
        course = session.query(Course).filter_by(std_id=std_id, course_id=course_id,
                                                 is_temp=False).first()
        return course

    def get_course_by_id_and_section(self, course_id, section):
        # Get the course from course_list
        course = session.query(CourseList).filter_by(course_list_id=course_id,
                                                     section=section).first()
        return course

    # def get_all_courses_by_id(self, std_id):
    def get_all_courses_by_id(self):
        std_id = self.glob_id
        print()
        print()
        print("std_id: " + str(std_id))
        print("self.glob_id: " + str(self.glob_id))
        course_list = session.query(Course).filter_by(std_id=std_id, is_temp=False).all()
        return course_list

    # def get_all_courses_by_std_id_and_course_id(self, std_id, course_id):
    def get_all_courses_by_std_id_and_course_id(self, course_id):
        std_id = self.glob_id
        course_list = session.query(Course).filter_by(std_id=std_id, course_id=course_id, is_temp=False).all()
        return course_list

    # def get_all_courses_by_id_and_type(self, std_id, type):
    def get_all_courses_by_id_and_type(self, type):
        std_id = self.glob_id
        print(self.glob_id)
        course_list = session.query(Course).filter_by(std_id=std_id, type=type).all()
        print("course_list: " + str(course_list))
        print("std_id: " + str(std_id))
        print("type: " + str(type))
        return course_list

    def check_if_course_already_exist(self, course_id, section):
        std_id = self.glob_id
        course = session.query(Course).filter_by(std_id=std_id, course_id=course_id,
                                                 section=section).first()
        if course is None:
            return False
        else:
            return True

    def is_user_enrolled_in_this_course(self, course_id, section):
        std_id = self.glob_id
        course = session.query(Course).filter_by(std_id=std_id, course_id=course_id,
                                                 section=section, is_temp=False).first()
        if course is None:
            return False
        else:
            return True

    def time_to_seconds(self, t):
        return t.hour * 3600 + t.minute * 60 + t.second

    def get_timings_of_all_courses_by_id(self, exclude_id, exclude_section):
        std_id = self.glob_id
        course_list_query = session.query(Course).filter_by(std_id=std_id, is_temp=False).all()
        start_timings = []
        end_timings = []
        days = []

        for course in course_list_query:
            c_list = session.query(CourseList).filter_by(course_list_id=course.course_id,
                                                         section=course.section).first()

            if course.course_id == exclude_id and course.section == exclude_section:
                continue

            end_time = self.time_to_seconds(c_list.end_time)
            start_time = self.time_to_seconds(c_list.start_time)
            day = c_list.days

            end_timings.append(end_time)
            start_timings.append(start_time)
            days.append(day)

            print(end_time, start_time, day, type(end_time), type(start_time), type(day))
        print()

        return start_timings, end_timings, days

    def get_days_timings_of_all_courses_by_id_temp_false(self):
        std_id = self.glob_id
        course_list_query = session.query(Course).filter_by(std_id=std_id).all()
        days = []
        start_timings = []
        end_timings = []

        for course in course_list_query:
            c_list = session.query(CourseList).filter_by(course_list_id=course.course_id,
                                                         section=course.section).first()

            end_time = self.time_to_seconds(c_list.end_time)
            start_time = self.time_to_seconds(c_list.start_time)
            day = c_list.days

            end_timings.append(end_time)
            start_timings.append(start_time)
            days.append(day)

            print(end_time, start_time, day, type(end_time), type(start_time), type(day))
        print()

        return start_timings, end_timings, days

    def get_days_list(self, days):
        return [days[x:x + 2] for x in range(0, len(days), 2)]

    # def add_course(self, std_id, course_list_id, section):
    def add_course(self, course_list_id, section):
        std_id = self.glob_id
        course = session.query(CourseList).filter_by(course_list_id=course_list_id).first()
        print("course.section: " + course.section)

        is_already_added = self.check_if_course_already_exist(course_list_id, section)
        if is_already_added:
            print("Returning false")
            return False

        new_course = Course(std_id=std_id, section=section, course_id=course_list_id,
                            is_temp=True, type="Add")

        session.add(new_course)
        try:
            session.commit()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            session.rollback()
            return False
        return True

    # def remove_course(self, std_id, course_id, section):
    def remove_course(self, course_id, section):
        std_id = self.glob_id
        print("Came in here")
        course = session.query(Course).filter_by(std_id=std_id, course_id=course_id, section=section).first()
        print(f" std_id: {std_id} course_id: {course_id} section: {section}")
        session.delete(course)
        try:
            session.commit()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            session.rollback()
            return False
        return True

    # def is_temp_false_remove_type_add(self, std_id, course_type):
    def is_temp_false_remove_type_add(self, course_type):
        std_id = self.glob_id
        course_objs = session.query(Course).filter_by(std_id=std_id, type=course_type).all()
        for c in course_objs:
            c.is_temp = False
            c.type = None
        try:
            session.commit()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            session.rollback()
            return False
        return True

    # def is_temp_false_single_course(self, std_id, course_id, section):
    def is_temp_false_single_course(self, course_id, section):
        std_id = self.glob_id
        course = session.query(Course).filter_by(std_id=std_id, course_id=course_id,
                                                 section=section).first()
        course.is_temp = False
        course.type = None
        try:
            session.commit()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            session.rollback()
            return False
        return True

    def update_current_capacity(self, course_id, section, add_or_subtract):
        course = session.query(CourseList).filter_by(course_list_id=course_id,
                                                     section=section).first()
        if add_or_subtract == "Add":
            course.current_capacity += 1
        elif add_or_subtract == "Subtract":
            course.current_capacity -= 1

        if course.current_capacity == 0:
            course.status = False
        elif course.current_capacity > 0:
            course.status = True
        else:
            print("Error: current_capacity is negative")
            return False
        try:
            session.commit()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            session.rollback()
            return False
        return True

    # def swap_courses(self, std_id, course_id, section, course_id_enrolled, section_enrolled):
    def swap_courses(self, course_id, section, course_id_enrolled, section_enrolled):
        std_id = self.glob_id
        print(f"std_id: {std_id}\ncourse_id: {course_id}\nsection: {section}")
        self.remove_course(course_id_enrolled, section_enrolled)
        try:
            does_it_work = self.add_course(int(course_id), section)
            if not does_it_work:
                print("Course could not be added")
                return False
            self.is_temp_false_single_course(course_id, section)
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            print("Return is being called")
            return
        return True

    def get_activity_by_std_id(self):
        std_id = self.glob_id
        activity = session.query(Activity).filter_by(std_id=std_id).all()
        return activity

    def add_data_to_activity_log(self, std_id, activity_type, course_id=None, section=None):
        course = None
        if course_id is not None:
            course = session.query(CourseList).filter_by(course_list_id=course_id).first()

        new_activity = Activity(
            std_id=std_id,
            course_id=str(course_id) if course_id else None,
            activity_type=activity_type,
            activity_date=datetime.datetime.now().date(),
            activity_time=datetime.datetime.now().time(),
            course_section=section
        )
        session.add(new_activity)
        try:
            session.commit()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            session.rollback()
            return False
        return True

    def delete_all_data_activity_log(self):
        activity = session.query(Activity).all()
        for a in activity:
            session.delete(a)
        try:
            session.commit()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            session.rollback()
            return False
        return True

    def delete_everything_in_course_table(self):
        course_objs = session.query(Course).all()
        for c in course_objs:
            session.delete(c)
        try:
            session.commit()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            session.rollback()
            return False
        return True

    #
    # -------------- NEW METHOD FOR ATTENDANCE --------------
    #
    def insert_attendance_activity(self, std_id, day_val, date_val, status):
        """
        Inserts a new row in 'Activity' specifically for attendance.
        - activity_type = 'Attendance'
        - course_id = None (no real course)
        - Put day/date/status in course_section so it’s visible in logs
        """
        # example: "2025-03-01 (Monday) => Present"
        attendance_info = f"{date_val} ({day_val}) => {status}"

        new_activity = Activity(
            std_id=std_id,
            course_id=None,  # no actual course
            activity_type="Attendance",
            activity_date=datetime.datetime.now().date(),
            activity_time=datetime.datetime.now().time(),
            course_section=attendance_info
        )
        session.add(new_activity)
        try:
            session.commit()
        except:
            print("Error (insert_attendance_activity):", sys.exc_info()[0])
            print(traceback.format_exc())
            session.rollback()
            return False
        return True
    
    def insert_activity(self, std_id, activity_type, description, date_val, time_val):
        """
        Insert a new row in the Activity table.
        - std_id: student ID
        - activity_type: e.g. "Attendance"
        - description: a string we store in 'course_section'
        - date_val: string "YYYY-MM-DD"
        - time_val: string "HH:MM:SS"
        """
        try:
            # Convert date_val/time_val from strings to Python date/time objects
            activity_date_obj = datetime.datetime.strptime(date_val, "%Y-%m-%d").date()
            activity_time_obj = datetime.datetime.strptime(time_val, "%H:%M:%S").time()
        except ValueError:
            # fallback if parsing fails, just use "now"
            activity_date_obj = datetime.datetime.now().date()
            activity_time_obj = datetime.datetime.now().time()

        new_activity = Activity(
            std_id=std_id,
            course_id=None,               # no specific course for attendance
            activity_type=activity_type,  # e.g. "Attendance"
            activity_date=activity_date_obj,
            activity_time=activity_time_obj,
            # Store the attendance description in course_section
            course_section=description  
        )

        session.add(new_activity)
        try:
            session.commit()
            return True
        except:
            print("Error in insert_activity:")
            print(sys.exc_info()[0])
            print(traceback.format_exc())
            session.rollback()
            return False



if __name__ == "__main__":
    all_queries = AllQueries()
    all_queries.delete_all_data_activity_log()
    all_queries.delete_everything_in_course_table()
    print(all_queries.get_current_day())
