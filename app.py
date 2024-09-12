import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_object("config.Config")

# Configurações do SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_manager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Modelo para usuários
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Modelo para tarefas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="open")
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)


# Inicializar o banco de dados (criar as tabelas)
with app.app_context():
    db.create_all()


# Função para criar um usuário
def create_user(username, password):
    try:
        if User.query.filter_by(username=username).first():
            return False  # Usuário já existe
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Erro ao criar o usuário: {e}")
        return False


# Função para validar o usuário
def validate_user(username):
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            print("Usuário não encontrado.")
        return user
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {e}")
        return None


# Função para criar tarefa
def create_task(title, description, creator_id, assignee_id=None):
    try:
        new_task = Task(
            title=title,
            description=description,
            creator_id=creator_id,
            assignee_id=assignee_id,
        )
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao criar tarefa: {e}")


# Função para obter todas as tarefas
def get_all_tasks():
    return Task.query.all()


# Função para obter uma tarefa pelo ID
def get_task(task_id):
    return Task.query.get_or_404(task_id)


# Rota da página inicial
@app.route("/")
def home():
    return redirect(url_for("login"))


# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            user = validate_user(username)
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                flash("Login realizado com sucesso!")
                return redirect(url_for("dashboard"))
            else:
                flash("Usuário ou senha incorretos.")
        except Exception as e:
            print(f"Erro ao validar o usuário: {e}")
            flash("Erro interno do servidor. Tente novamente mais tarde.")
    return render_template("login.html")


# Rota de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username and password:
            if create_user(username, password):
                flash("Conta criada com sucesso! Faça login.")
                return redirect(url_for("login"))
            else:
                flash("Usuário já existe.")
        else:
            flash("Por favor, preencha todos os campos.")
    return render_template("register.html")


# Rota para criar uma nova tarefa
@app.route("/tasks/create", methods=["POST"])
def create_task_route():
    title = request.form["title"]
    description = request.form["description"]
    creator_id = session.get("user_id")
    assignee_id = request.form.get("assignee_id")
    create_task(title, description, creator_id, assignee_id)
    flash("Tarefa criada com sucesso!")
    return redirect(url_for("dashboard"))


# Rota para listar e criar tarefas
@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        creator_id = session.get("user_id")
        assignee_id = request.form.get("assignee_id")
        create_task(title, description, creator_id, assignee_id)
        flash("Tarefa criada com sucesso!")
        return redirect(url_for("tasks"))

    tasks = get_all_tasks()
    return render_template("tasks.html", tasks=tasks)


# Rota para editar uma tarefa
@app.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = get_task(task_id)
    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form["description"]
        task.status = request.form["status"]
        task.assignee_id = request.form.get("assignee_id")
        db.session.commit()
        flash("Tarefa atualizada com sucesso!")
        return redirect(url_for("dashboard"))

    users = User.query.all()
    return render_template("edit_task.html", task=task, users=users)


# Rota para atualizar o status de uma tarefa
@app.route("/tasks/status/<int:task_id>", methods=["POST"])
def change_task_status(task_id):
    task = get_task(task_id)
    new_status = request.form["status"]
    task.status = new_status
    db.session.commit()
    flash("Status da tarefa atualizado com sucesso!")
    return redirect(url_for("dashboard"))


# Rota para deletar uma tarefa
@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = get_task(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Tarefa apagada com sucesso!")
    return redirect(url_for("dashboard"))


# Rota para o dashboard
@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    status = request.args.get("status", "all")

    if status != "all":
        tasks = Task.query.filter_by(status=status).all()
    else:
        tasks = get_all_tasks()

    # Obter criadores e atribuídos para as tarefas
    task_list = []
    for task in tasks:
        creator = User.query.get(task.creator_id)
        assignee = User.query.get(task.assignee_id)
        task_list.append({"task": task, "creator": creator, "assignee": assignee})

    # Obter todos os usuários para a seleção
    users = User.query.all()

    return render_template("dashboard.html", tasks=task_list, users=users)


# Rota de logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


# Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True)
