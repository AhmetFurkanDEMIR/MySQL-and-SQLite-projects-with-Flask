from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

# Kullanıcı Giriş Decorator'ı
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "logged_in" in session:
            return f(*args, **kwargs)

        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","danger")
            return redirect(url_for("login"))

    return decorated_function

# Kullanıcı Kayıt Formu
class RegisterForm(Form):

    name = StringField("İsim Soyisim",validators=[validators.Length(min = 4,max = 25)])
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min = 5,max = 35)])

    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin...")])
    password = PasswordField("Parola:",validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")

class LoginForm(Form):

    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

# Flask uygulamamız
app = Flask(__name__)

# mysql configarsyonu
app.secret_key= "demirai"
app.config["MYSQL_HOST"] = "demirai.mysql.pythonanywhere-services.com"
app.config["MYSQL_USER"] = "demirai"
app.config["MYSQL_PASSWORD"] = "****"
app.config["MYSQL_DB"] = "demirai$demirai"

# verilerimiz sozluk seklinde gelecek
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

""" 
[
{"id":1, "title":"Deneme"},
{"id":2, "title":"Deneme2"}
]

"""

# mysql db, flask ile iletişimde.
mysql = MySQL(app)

# root, ana sayfa
@app.route("/")
def index():
   return render_template("index.html")

# hakkımda sayfası
@app.route("/about")
def about():
    return render_template("about.html")

# Makale Sayfası
@app.route("/articles")
def articles():

    cursor = mysql.connection.cursor()

    sorgu = "Select * From articles"
    result = cursor.execute(sorgu)

    if result > 0:
        articles = cursor.fetchall()
        return render_template("articles.html",articles = articles)

    else:
        return render_template("articles.html")

@app.route("/dashboard")
@login_required
def dashboard():

    cursor = mysql.connection.cursor()

    sorgu = "Select * From articles where author = %s"
    result = cursor.execute(sorgu,(session["username"],))

    if result > 0:
        articles = cursor.fetchall()
        return render_template("dashboard.html",articles = articles)

    else:
        return render_template("dashboard.html")

#Kayıt Olma
@app.route("/register",methods = ["GET","POST"])
def register():

    #kayit formu
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        # kayit icin bilgiler
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data) # passwordu gizledim.

        # Sql sorgulari icin onerdigim kaynak: https://www.w3schools.com/sql/

        # veritabani uzerinde islem yapmamizi saglayan yapi
        cursor = mysql.connection.cursor()

        # "Insert into users" users tablosuna bir tane deger ekleyecegiz
        # "(name,email,username,password) VALUES(%s,%s,%s,%s)" degerleri sirasiyla atadik
        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"

        # Sql sorgusunu calistiriyoruz.
        cursor.execute(sorgu,(name,email,username,password))

        # degisikligi veritabanina bildiriyoruz.
        # bilgi cekiyorsaniz bu isleme gerek yoktur.
        mysql.connection.commit()

        # kaynaklarin gereksiz yere kullanilmamasi icin close ile kapatiik.
        cursor.close()

        # bilgilendirme
        flash("Başarıyla Kayıt Oldunuz...","success")
        return redirect(url_for("login"))

    else:
        # bilgilendirme
        return render_template("register.html",form = form)

# Login İşlemi
@app.route("/login",methods =["GET","POST"])
def login():

    # login formu
    form = LoginForm(request.form)

    if request.method == "POST":

      # formdaki bilgiler
      username = form.username.data
      password_entered = form.password.data

      # veritabani uzerinde islem yapmamizi saglayan yapi
      cursor = mysql.connection.cursor()

      # "Select * From users" users tablosundan bilgi alaagiz
      # " where username = %s" arayacagimiz username
      sorgu = "Select * From users where username = %s"

      # aranan veri varsa "1" yosa "0"
      result = cursor.execute(sorgu,(username,))

      if result > 0:

          # veriyi almak icin gerekli fonksiyon.
          # verilerimiz sozluk seklindeydi, boylece diger degerlere de ulasabiliriz.
          data = cursor.fetchone()
          # sifre uyusacakmi diye kontrol edecegiz.
          real_password = data["password"]

          # verilerin sifrelenmis hali ayni ise giris yapilir.
          if sha256_crypt.verify(password_entered,real_password):
              flash("Başarıyla Giriş Yaptınız...","success")

              session["logged_in"] = True
              session["username"] = username
              return redirect(url_for("index"))

          else:
              flash("Parolanızı Yanlış Girdiniz...","danger")
              return redirect(url_for("login"))

      else:
          flash("Böyle bir kullanıcı bulunmuyor...","danger")
          return redirect(url_for("login"))


    return render_template("login.html",form = form)


# Detay Sayfası
@app.route("/article/<string:id>")
def article(id):

    cursor = mysql.connection.cursor()

    sorgu = "Select * from articles where id = %s"
    result = cursor.execute(sorgu,(id,))

    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html",article = article)

    else:
        return render_template("article.html")

# Logout İşlemi
@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("index"))

# Makale Ekleme
@app.route("/addarticle",methods = ["GET","POST"])
def addarticle():

    form = ArticleForm(request.form)

    if request.method == "POST" and form.validate():

        title = form.title.data
        content = form.content.data

        cursor = mysql.connection.cursor()

        sorgu = "Insert into articles(title,author,content) VALUES(%s,%s,%s)"

        cursor.execute(sorgu,(title,session["username"],content))

        mysql.connection.commit()

        cursor.close()

        flash("Makale Başarıyla Eklendi","success")

        return redirect(url_for("dashboard"))

    return render_template("addarticle.html",form = form)

#Makale Silme
@app.route("/delete/<string:id>")
@login_required
def delete(id):

    cursor = mysql.connection.cursor()

    # kendi adimiza makale varmi kontrol ediyoruz.
    sorgu = "Select * from articles where author = %s and id = %s"
    result = cursor.execute(sorgu,(session["username"],id))


    # silinebilecek makale varsa iceri girer
    if result > 0:

        # "Delete from articles" makalelerden veri silecegiz
        # "where id = %s" bu degere sahip olan veri silinecek.
        sorgu2 = "Delete from articles where id = %s"

        cursor.execute(sorgu2,(id,))

        mysql.connection.commit()

        return redirect(url_for("dashboard"))

    else:
        flash("Böyle bir makale yok veya bu işleme yetkiniz yok","danger")
        return redirect(url_for("index"))

#Makale Güncelleme
@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def update(id):

  if request.method == "GET":

    cursor = mysql.connection.cursor()

    # kendi adimiza makale varmi kontrol ediyoruz.
    sorgu = "Select * from articles where id = %s and author = %s"
    result = cursor.execute(sorgu,(id,session["username"]))

    if result == 0:
      flash("Böyle bir makale yok veya bu işleme yetkiniz yok","danger")
      return redirect(url_for("index"))

    else:

      # makaleyi cekip, formu makalemiz ile degistirecegiz
      # boylece makalemiz uzerinde degisiklik yapabilecegiz.
      article = cursor.fetchone()
      form = ArticleForm()

      form.title.data = article["title"]
      form.content.data = article["content"]
      return render_template("update.html",form = form)

  else:
       
    # POST REQUEST
    form = ArticleForm(request.form)

    newTitle = form.title.data
    newContent = form.content.data

    # "Update articles" articles tablosunu guncelleyecegiz.
    # "Set title = %s,content = %s" guncelleme
    # " where id = %s" bu id ye sahip satir guncellenir.
    sorgu2 = "Update articles Set title = %s,content = %s where id = %s "
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu2,(newTitle,newContent,id))

    mysql.connection.commit()

    flash("Makale başarıyla güncellendi","success")

    return redirect(url_for("dashboard"))

    pass

# Makale Form
class ArticleForm(Form):

    title = StringField("Makale Başlığı",validators=[validators.Length(min = 5,max = 100)])
    content = TextAreaField("Makale İçeriği",validators=[validators.Length(min = 10)])

# Arama URL
@app.route("/search",methods = ["GET","POST"])
def search():

  if request.method == "GET":
    return redirect(url_for("index"))

  else:

    keyword = request.form.get("keyword")

    cursor = mysql.connection.cursor()

    # "Select * from articles" articles tablosunda arama yapacagiz.
    # where title like '%" + keyword +"%' icerisinde 'keyword' degiskenindeki gecenleri al.
    sorgu = "Select * from articles where title like '%" + keyword +"%'"

    result = cursor.execute(sorgu)

    if result == 0:
      flash("Aranan kelimeye uygun makale bulunamadı...","warning")
      return redirect(url_for("articles"))

    else:
      articles = cursor.fetchall()
      return render_template("articles.html",articles = articles)

# local de çalışır
if __name__ == "__main__":
    app.run(debug=True)
