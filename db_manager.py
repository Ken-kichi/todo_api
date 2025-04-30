import pytz
from datetime import datetime
from typing import Union
from models import UserRead, Message, TaskRead,UserReadAll


class DatabaseManager:

    # Task
    # create
    def create_task_record(self, conn, title, description, user_id) -> Message:
        created_time = datetime.now(pytz.timezone(
            'Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S.%f")
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO tasks (
                user_id,
                title,
                description,
                completed,
                created_at,
                updated_at
                )
                VALUES (%s,%s, %s, %s, %s, %s);
                """, (user_id, title, description, False, created_time, created_time))
        conn.commit()
        return Message(message="Task is created")

    # read_all - Manager
    def read_all_task_record(self, conn) -> Union[TaskRead, bool]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks;")
        rows = cursor.fetchall()
        conn.commit()

        if not rows:
            return False

        tasks = [
            TaskRead(
                id=str(row[0]),
                user_id=str(row[1]),
                title=str(row[2]),
                description=str(row[3]),
                completed=bool(row[4])
            )
            for row in rows
        ]
        return tasks

    # read_all - General User
    def read_all_task_record_by_general_user(self, conn, user_id) -> Union[TaskRead, bool]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
        rows = cursor.fetchall()
        conn.commit()

        if not rows:
            return False

        tasks = [
            TaskRead(
                id=str(row[0]),
                user_id=str(row[1]),
                title=str(row[2]),
                description=str(row[3]),
                completed=bool(row[4])
            )
            for row in rows
        ]
        return tasks

    # read_by_id
    def read_task_record_by_id(self, conn, id: str) -> Union[TaskRead, bool]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
        row = cursor.fetchall()
        conn.commit()

        if not row:
            return False

        task = TaskRead(
            id=str(row[0][0]),
            user_id=str(row[0][1]),
            title=str(row[0][2]),
            description=str(row[0][3]),
            completed=bool(row[0][4])
        )
        return task

    # update
    def update_task_record(self, conn, id, title, description, completed, user_id) -> Message:
        updated_time = datetime.now(pytz.timezone(
            'Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S.%f")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = %s,description=%s,completed=%s,updated_at = %s ,user_id = %s WHERE id = %s",
            (title, description, completed, updated_time, user_id, id)
        )

        conn.commit()
        return Message(message="Task is updated")

    # delete - Manager
    def delete_task_record(self, conn, id) -> Message:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))

        conn.commit()
        return Message(message="Task is deleted")

    # User
    # create
    def create_user_record(self, conn, username, full_name, email, hashed_password, is_manager) -> Message:
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO users (
                        username,
                        full_name,
                        email,
                        hashed_password,
                        is_manager
                        )
                        VALUES (%s,%s, %s, %s, %s);
                """, (username, full_name, email, hashed_password, is_manager))
        conn.commit()
        return Message(message="User is created")

    # read_all
    def read_all_user_record(self, conn)->Union[UserReadAll,bool]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        conn.commit()

        if not rows:
            return False

        users = [
            UserReadAll(
                id=str(row[0]),
                username=row[1],
                full_name=row[2],
                email=row[3],
                is_manager=row[5],
                disabled=row[6],
            ) for row in rows
        ]
        return users

    # read_by_id
    def read_user_record_by_id(self, conn, user_id: str) -> Union[UserReadAll,bool]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
        row = cursor.fetchall()

        if not row:
            return False

        user = UserReadAll(
            id=str(row[0][0]),
            username=row[0][1],
            full_name=row[0][2],
            email=row[0][3],
            is_manager=row[0][5],
            disabled=row[0][6],
        )

        return user

    # read_by_name
    def read_user_record_by_email(self, conn, email) -> Union[UserRead,bool]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = %s;", (email,))
        rows = cursor.fetchall()

        if not rows:
            return False

        user = UserRead(
             id=str(rows[0][0]),
            username=rows[0][1],
            full_name=rows[0][2],
            email=rows[0][3],
            hashed_password=rows[0][4],
            is_manager=rows[0][5],
            disabled=rows[0][6]
        )

        return user

    # update
    def update_user_record(self, conn, user_id, username, full_name, email, is_manager,disabled):
        updated_time = datetime.now(pytz.timezone(
            'Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S.%f")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = %s,full_name=%s,email=%s,is_manager = %s,disabled=%s,updated_at = %s WHERE id = %s;",
            (username, full_name, email, is_manager,disabled, updated_time, user_id)
        )

        conn.commit()
        return Message(message="User is updated")

    # delete
    def delete_user_record(self, conn, id):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))

        conn.commit()

        return Message(message="User is deleted")
