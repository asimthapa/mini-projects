from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime, timedelta
import operator

base = declarative_base()


class Table(base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default="Random string")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.task}"


def main():
    engine = create_db()
    session = create_session(engine)
    while True:
        display_menu()
        user_in = int(input())
        if user_in == 1:
            # Today's tasks
            today = datetime.today()
            tasks = get_tasks(session, "deadline", ("eqt", today.date()))

            print(f"\nToday {today.day} {today.strftime('%b')}")
            if len(tasks) == 0:
                print("Nothing to do!")
            else:
                print_tasks(tasks)

        elif user_in == 2:
            # Week's tasks, 7 days from today
            today = datetime.today()
            for i in range(7):
                new_date = today + timedelta(days=i)
                tasks = get_tasks(session, "deadline", ("eqt", new_date.date()))
                print(f"\n{new_date.strftime('%A')} {new_date.day} {new_date.strftime('%b')}")
                if len(tasks) == 0:
                    print("Nothing to do!\n")
                else:
                    print_tasks(tasks)

        elif user_in == 3:
            # All tasks
            print("All tasks:")
            tasks = get_tasks(session)
            if len(tasks) == 0:
                print("Nothing to do!\n")
            else:
                print_tasks(tasks, print_deadline=True)

        elif user_in == 4:
            # Missed tasks
            tasks = get_tasks(session, "deadline", ("lt", datetime.today().date()))
            if len(tasks) == 0:
                print("Nothing is missed!\n")
            else:
                print_tasks(tasks, print_deadline=True)

        elif user_in == 5:
            # Add task
            task = input("\nEnter task\n")
            deadline = input("Enter deadline\n")
            add_task(session, task, deadline)
            print("The task has been added!\n")

        elif user_in == 6:
            # Delete task
            print("\nChoose the number of the task you want to delete:")
            tasks = get_tasks(session)
            print_tasks(tasks, print_deadline=True)
            del_id = int(input()) - 1
            delete_task(session, tasks[del_id].task, tasks[del_id].deadline)
            print("The task has been deleted!\n")
        elif user_in == 0:
            end()


def display_menu():
    menu_opt = ["Today's tasks", "Week's tasks", "All tasks", "Missed tasks", "Add task", "Delete task", "Exit"]
    for i, opt in enumerate(menu_opt):
        if opt == "Exit":
            print(f"0) {opt}")
        else:
            print(f"{i+1}) {opt}")


def end():
    print("\nBye!")
    exit(0)


def print_tasks(tasks, print_deadline=False):
    for i, task_info in enumerate(tasks):
        if print_deadline:
            print(f"{i + 1}. {task_info}. {task_info.deadline.day} {task_info.deadline.strftime('%b')}")
        else:
            print(f"{i + 1}. {task_info}")
    print()


def get_tasks(session, table_field=None, query_filter=(), sort_by="deadline"):
    ops = {
        'eqt': operator.eq,
        'lt': operator.lt,
        'gt': operator.gt
    }
    if sort_by.lower() == "deadline":
        sort_by = Table.deadline
    elif sort_by.lower() == "tasks":
        sort_by = Table.task

    if table_field is None:
        tasks = session.query(Table).order_by(sort_by).all()
    else:
        if table_field.lower() == "task":
            table_field = Table.task
        elif table_field.lower() == "deadline":
            table_field = Table.deadline

        tasks = session.query(Table).filter(ops[query_filter[0]](table_field, query_filter[1])).order_by(sort_by).all()

    return tasks


def add_task(session, task, deadline):
    deadline = date.fromisoformat(deadline)
    new_row = Table(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()


def delete_task(session, task, deadline):
    session.query(Table).filter(Table.task == task and Table.deadline == deadline).delete()
    session.commit()


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def create_db():
    engine = create_engine(f'sqlite:///todo.db?check_same_thread=False')
    base.metadata.create_all(engine)
    return engine


if __name__ == '__main__':
    main()
