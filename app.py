from flask import Flask, render_template, request, redirect ,session
from help import login_required, erro
from flask_session import Session
import pyodbc

#FLASK
app = Flask(__name__)

#SESSION
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#SQL
dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-JOMUBM1\SQLEXPRESS;"
    "Database=BaseDeDados;"
)

conexao = pyodbc.connect(dados_conexao)
print("boa")

cursor = conexao.cursor()


# Página inicial depois que faz o login
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if not session.get("name"):
            return redirect("/login")
        username = session["name"]
        return render_template("index.html", username=username)
    else:
        # Salvando o novo lembrete na base de dados
        username = session["name"]
        texto = request.form.get("texto")
        dia = request.form.get("data")
        cursor.execute(f"insert into lembretes (username, texto, dia) values ('{username}','{texto}','{dia}')")
        cursor.commit()
        return redirect("/")

#Primeira página quando entra no site
@app.route("/login", methods=["GET", "POST"])
def login():
    # Esquecer usuário
    session.clear()
    # Usuário chegou via POST
    if request.method == "POST":
        # Verificar se o usuário colocou nome e senha
        if not request.form.get("username") or not request.form.get("password"):
            return erro("Coloque um nome e uma senha")
        # Verificar se a conta existe
        count = 0
        result = cursor.execute("select * from users")
        for row in result:
            if row[0] == request.form.get("username") and row[1] == request.form.get("password"):
                count += 1
                break
        if count == 0:
            return erro("Conta não encontrada")
        # Lembrar qual usuário entrou
        session["name"] = request.form.get("username")
        # Redirect para página principal
        return redirect("/")
    # Usuário chegou via GET
    else:
        # Preencher formulário de login
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Esquecer o usuário
    session.clear()
    # Redirect para fazer login
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Verificar se o usuário preencheu todos os campos
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return erro("Coloque um nome e uma senha")
        # Verificar se o nome já existe
        count = 0
        result = cursor.execute("select * from users")
        for row in result:
            if row[0] == request.form.get("username"):
                count += 1
                break
        if count != 0:
            return erro("Esse nome já existe")
        # Colocar conta na base de dados
        username = request.form.get("username")
        senha = request.form.get("password")
        cursor.execute(f"insert into users (username, senha) values ('{username}', '{senha}')")
        cursor.commit()
        # Redirect para fazer o login
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/meuslembretes")
def meuslemb():
    username = session["name"]
    result = cursor.execute(f"select * from lembretes where username like '{username}'")
    return render_template("meuslembretes.html", result=result, username=username)

if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port=5000)
