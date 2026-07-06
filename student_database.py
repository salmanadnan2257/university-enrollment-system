from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Date, Time, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create an SQLite database in memory (replace 'sqlite:///:memory:' with a file path for a persistent database)
engine = create_engine('sqlite:///student.db', echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'

    std_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    major = Column(String, nullable=False)

    courses = relationship('Course', back_populates='student')
    filters = relationship('Filter', back_populates='student')
    activities = relationship('Activity', back_populates='student')


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(Integer, ForeignKey('course_list.course_list_id'), primary_key=True)
    std_id = Column(Integer, ForeignKey('student.std_id'), primary_key=True)
    section = Column(String, nullable=False, primary_key=True)
    is_temp = Column(Boolean, nullable=False)
    type = Column(String)
    # swap_id = Column(Integer, ForeignKey('course_list.id'))
    # remove_id = Column(Integer, ForeignKey('course_list.id'))
    # The id of swap_id remove_id is of this class
    swap_id = Column(Integer, ForeignKey('course.course_id'))
    remove_id = Column(Integer, ForeignKey('course.course_id'))

    # Define many-to-one relationship between Course and Student
    student = relationship('Student', back_populates='courses')
    # Define one-to-one relationship between Course and CourseList
    course_list = relationship('CourseList', foreign_keys=[course_id], back_populates='course')


class CourseList(Base):
    __tablename__ = 'course_list'

    course_list_id = Column(Integer, primary_key=True)
    section = Column(String, nullable=False, primary_key=True)
    # course_id = Column(Integer, ForeignKey('course.id'))
    course_name = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    days = Column(String, nullable=False)
    room = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    current_capacity = Column(Integer, nullable=False)

    course = relationship('Course', back_populates='course_list')
    activities = relationship('Activity', back_populates='course_list')


class Filter(Base):
    __tablename__ = 'filter'

    filter_id = Column(Integer, primary_key=True)
    std_id = Column(Integer, ForeignKey('student.std_id'))
    by_day = Column(Boolean, nullable=False)
    by_week = Column(Boolean, nullable=False)

    student = relationship('Student', back_populates='filters')


class Activity(Base):
    __tablename__ = 'activity'

    activity_id = Column(Integer, primary_key=True)
    std_id = Column(Integer, ForeignKey('student.std_id'))
    # course_id = Column(Integer, ForeignKey('course_list.course_list_id'))
    # course_id from CourseList
    course_id = Column(String, ForeignKey('course_list.course_list_id'), nullable=True)
    activity_type = Column(String, nullable=False)
    activity_date = Column(Date, nullable=False)
    activity_time = Column(Time, nullable=False)
    course_section = Column(String, nullable=True)

    student = relationship('Student', back_populates='activities')
    course_list = relationship('CourseList', back_populates='activities')


# Create the table in the database
# if not engine.dialect.has_table(engine, "student"):
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Close the session
session.close()

