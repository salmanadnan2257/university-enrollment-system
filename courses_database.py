from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an SQLite database in memory (replace 'sqlite:///:memory:' with a file path for a persistent database)
engine = create_engine('sqlite:///student.db', echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    major = Column(String, nullable=False)


# Create the table in the database
# Make condition for this to run if not made yet Base.metadata.create_all(engine)
# if not engine.dialect.has_table(engine, "student"):
# Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# # Add some data to the table
# user1 = Student(name='Alice', age=25)
# user2 = Student(name='Bob', age=30)
#
# session.add_all([user1, user2])
# session.commit()
#
# # Perform a query to retrieve data
# users = session.query(Student).all()
#
# # Print the retrieved data
# for user in users:
#     print(f"ID: {user.id}, Name: {user.name}, DOB: {user.dob}")

# Close the session
session.close()
