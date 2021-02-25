from flask import Flask,render_template,redirect,url_for,request

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# sqlite db konumu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/EE6A1EE26A1EA6FD/Python/Flask_Todo_App/todo.db'

# SQLAlchemy ile db baglantisi
# Artik ORM db (Nesne-İlişkisel Eşleme)
db = SQLAlchemy(app)
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

@app.route("/complete/<string:id>")
def completeTodo(id):

    # istenilen id deki verileri (nese) aliyoruz.
    todo = Todo.query.filter_by(id = id).first()

    # istenilen id ye sahip nesnenin complate degiskenini True olarak ayarliyoruz.
    todo.complete = not todo.complete

    # islemi tamamladik.
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add",methods = ["POST"])
def addTodo():

    title = request.form.get("title")

    # Todo classindan bir adet nesene olusturduk. Title ve Complate 'e deger atadik.
    newTodo = Todo(title = title,complete = False)

    # nesneyi db ye aktardik.
    db.session.add(newTodo)

    # ekleme islemini bitirdik.
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def deleteTodo(id):

    # istenilen id deki verileri (nese) aliyoruz.
    todo = Todo.query.filter_by(id = id).first()

    # bu nesneyi siliyorum
    db.session.delete(todo)

    # silme islemi tamam.
    db.session.commit()
    return redirect(url_for("index"))

# db ye Toodo adinda bir tablo eklemek icin class olusturduk.
class Todo(db.Model):

    # tabloya id adinda sutun ekliyoruz.
    id = db.Column(db.Integer, primary_key=True)

    # tabloya title adinda sutun ekliyoruz.
    title = db.Column(db.String(80))

    # tabloya complate adinda sutun ekliyoruz.
    complete = db.Column(db.Boolean)

if __name__ == "__main__":

    # tum classlar tablo olarak db ye aktarilir.
    db.create_all()
    app.run(debug=True)
