from asyncio import Task

from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import check_passord_hash, generate_password_hash

from app import User

app = Flask(__name__)
app.config.from_object("config.Config")
mysql = MySQL(app)


# Função para criar um novo usuário com senha hasheada
def create_user(username, password):
    try:
        cur = mysql.connection.cursor()

        # Verifica se o usuário já existe
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if cur.fetchone():
            cur.close()
            return False  # Usuário já existe

        # Cria o novo usuário
        hashed_password = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password),
        )
        mysql.connection.commit()
        cur.close()
        return True  # Usuário criado com sucesso
    except Exception as e:
        print(f"Erro ao criar o usuário: {e}")
        return False


def validate_user(username):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        if not user:
            print("Usuário não encontrado.")
        return user
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {e}")
        return None


def create_task(title, description, deadline, creator_id, assignee_id=None):
    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO tasks (title, description, deadline, creator_id, assignee_id) 
        VALUES (%s, %s, %s, %s, %s)
    """,
        (title, description, deadline, creator_id, assignee_id),
    )
    mysql.connection.commit()
    cur.close()


def get_tasks(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", [user_id])
    tasks = cur.fetchall()
    cur.close()
    return tasks


def get_user_tasks(user_id):
    return (
        db.session.query(Task, User)
        .join(User, Task.creator_id == User.id)
        .filter((Task.creator_id == user_id) | (Task.assignee_id == user_id))
        .all()
    )


def get_all_tasks():
    return (
        db.session.query(Task, User.label("creator"))
        .join(User, Task.creator_id == User.id)
        .all()
    )
