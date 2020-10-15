# To-Do List
# Author: Jason Tolbert (https://github.com/jasonalantolbert)
# Python Version: 3.8

# This program was written as part of a JetBrains Academy project.
# For more information, visit https://hyperskill.org/projects/105.


# BEGINNING OF PROGRAM


# import statements
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine("sqlite:///todo.db?check_same_thread=False")  # creates sqlalchemy engine

Base = declarative_base()  # binds table base to variable Base

today = datetime.today()  # binds current date and time to variable today


class Table(Base):  # creates task table
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=today)


Base.metadata.create_all(engine)  # adds task table to database


# creates database session and binds it to variable session
Session = sessionmaker(bind=engine)
session = Session()


def todays_tasks():  # prints todays tasks
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print(f"\n{today.strftime('Today %d %b:')}")
    if not rows:
        print("Nothing to do!")
    else:
        for index in range(len(rows)):
            print(f"{index + 1}. {rows[index].task}")


def weeks_tasks():  # prints tasks for today and the next six days
    for i in range(0, 7):
        current_date = (today + timedelta(days=i)).date()
        rows = session.query(Table).filter(Table.deadline == current_date).all()
        print(f"\n{current_date.strftime('%A %d %b:')}")
        if not rows:
            print("Nothing to do!")
        else:
            for index in range(len(rows)):
                print(f"{index + 1}. {rows[index].task}")


def all_tasks():  # prints all tasks
    rows = session.query(Table).order_by(Table.deadline).all()
    print(f"\nAll tasks:")
    for index in range(len(rows)):
        print(f"{index + 1}. {rows[index].task}. {rows[index].deadline.strftime('%#d %b')}")


def missed_tasks():  # prints past-due tasks
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    print(f"\nMissed tasks:")
    if not rows:
        print("Nothing is missed!")
    else:
        for index in range(len(rows)):
            print(f"{index + 1}. {rows[index].task}. {rows[index].deadline.strftime('%#d %b')}")


def add_task():  # allows the user to add a task
    task_name = input("Enter task\n")
    deadline = datetime.strptime(input("Enter deadline (YYYY-MM-DD)\n"), "%Y-%m-%d")
    session.add(Table(task=task_name, deadline=deadline))
    session.commit()
    print("The task has been added!")


def delete_task():  # allows the user to delete a task
    rows = session.query(Table).order_by(Table.deadline).all()
    print(f"\nChoose the number of the task you want to delete:")
    for index in range(len(rows)):
        print(f"{index + 1}. {rows[index].task}. {rows[index].deadline.strftime('%#d %b')}")
    session.delete(rows[int(input()) - 1])
    session.commit()
    print("The task has been deleted!")


def main_menu():  # to-do list menu
    option = int(input("\n1) Today's tasks\n"
                       "2) Week's tasks\n"
                       "3) All tasks\n"
                       "4) Missed tasks\n"
                       "5) Add task\n"
                       "6) Delete task\n"
                       "0) Exit\n"))

    if option == 1:
        todays_tasks()
    elif option == 2:
        weeks_tasks()
    elif option == 3:
        all_tasks()
    elif option == 4:
        missed_tasks()
    elif option == 5:
        add_task()
    elif option == 6:
        delete_task()
    elif option == 0:
        exit()


while True:  # calls main_menu() infinitely
    main_menu()


# END OF PROGRAM
