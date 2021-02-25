# MySQL and SQLite projects with Flask

<p align="center">
  <img src="https://user-images.githubusercontent.com/54184905/109134183-d3e06480-7766-11eb-83b7-f3d44c53ebbd.png" />
</p>

**Flask:** Flask is a micro web framework written in Python. It is classified as a 
microframework because it does not require particular tools or libraries. It has no 
database abstraction layer, form validation, or any other components where 
pre-existing third-party libraries provide common functions. However, Flask supports 
extensions that can add application features as if they were implemented in Flask 
itself. Extensions exist for object-relational mappers, form validation, upload 
handling, various open authentication technologies and several common framework 
related tools.

Applications that use the Flask framework include Pinterest and LinkedIn.

<p align="center">
  <img src="https://user-images.githubusercontent.com/54184905/109134181-d3e06480-7766-11eb-97e8-61ffa4ca040a.png" />
</p>

**MySQL:** MySQL is an open-source relational database management system (RDBMS). Its 
name is a combination of "My", the name of co-founder Michael Widenius's daughter, and
"SQL", the abbreviation for Structured Query Language. A relational database organizes
data into one or more data tables in which data types may be related to each other; 
these relations help structure the data. SQL is a language programmers use to create, 
modify and extract data from the relational database, as well as control user access 
to the database. In addition to relational databases and SQL, an RDBMS like MySQL 
works with an operating system to implement a relational database in a computer's 
storage system, manages users, allows for network access and facilitates testing 
database integrity and creation of backups. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/54184905/109134179-d2af3780-7766-11eb-9b9c-5169fdcea403.png" />
</p>

**SQLite:** SQLite is a relational database management system (RDBMS) contained in a C
library. In contrast to many other database management systems, SQLite is not a client–server database engine. Rather, it is embedded into the end program.

SQLite is ACID-compliant and implements most of the SQL standard, generally following 
PostgreSQL syntax. However, SQLite uses a dynamically and weakly typed SQL syntax that does not guarantee the domain integrity. This means that one can, for example, insert a string into a column defined as an integer. SQLite will attempt to convert data 
between formats where appropriate, the string "123" into an integer in this case, but 
does not guarantee such conversions and will store the data as-is if such a conversion
is not possible.


## Projects

### [**demir.ai blog with MSQL**](/demiraiBlog/)

<p align="center">
  <img src="https://user-images.githubusercontent.com/54184905/109133486-1d7c7f80-7766-11eb-96ba-dc8d81b2f1f4.png" />
</p>

In this application, the user can register and log in to the form, I have stored user transactions in the table named "users".

~~~~sql
create table users(
   id INT NOT NULL AUTO_INCREMENT,
   name TEXT NOT NULL,
   email TEXT NOT NULL,
   username TEXT NOT NULL,
   password TEXT NOT NULL,
   PRIMARY KEY ( id )
);
~~~~

Users can read articles on this blog, if they wish, they can write their own articles after logging in. I have stored the data about the articles in the table named "articles".

~~~~sql
create table articles(
   id INT NOT NULL AUTO_INCREMENT,
   title TEXT NOT NULL,
   author TEXT NOT NULL,
   content TEXT NOT NULL,
   created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY ( id )
);
~~~~

This application was written in Python-Flask and both the database and the site were deployed on [pythonanywhere](https://www.pythonanywhere.com/).

Flask database configuration.

```python
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
```

Deployed version of this application (This site will be disabled on Sunday 23 May 2021): [Link](http://demirai.pythonanywhere.com/)

### [**Todo app with SQLite**](/FlaskTodoApp/)

<p align="center">
  <img src="https://user-images.githubusercontent.com/54184905/109133489-1eadac80-7766-11eb-805e-e2c0958f2a06.png" />
</p>

With this application, you can follow what you need to do regularly. You can add your tasks to the list and mark them when you do, or you can delete these tasks if you wish.

In this application, we created an ORM (Object Relational Mapping) database by combining SQLite and SQLAlchemy, so we performed operations on the objects we created without the need for SQL queries.

```python
# db ye Toodo adinda bir tablo eklemek icin class olusturduk.
class Todo(db.Model):

    # tabloya id adinda sutun ekliyoruz.
    id = db.Column(db.Integer, primary_key=True)

    # tabloya title adinda sutun ekliyoruz.
    title = db.Column(db.String(80))

    # tabloya complate adinda sutun ekliyoruz.
    complete = db.Column(db.Boolean)
```

Flask database configuration.


```python
app = Flask(__name__)

# sqlite db konumu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/EE6A1EE26A1EA6FD/Python/Flask_Todo_App/todo.db'

# SQLAlchemy ile db baglantisi
# Artik ORM db (Nesne-İlişkisel Eşleme)
db = SQLAlchemy(app)
```

Deployed version of this application (This site will be disabled on Sunday 23 May 2021): [Link](http://todoapp.pythonanywhere.com/)

