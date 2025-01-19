import hashlib
import sqlite3
import json
import os

salt = "library"

### Borra la base de datos
if os.path.exists("datos.db"):
	print("Recreando bd")
	os.remove("../datos.db")

con = sqlite3.connect("../datos.db")
cur = con.cursor()

### Crea la base de datos
cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		user_id integer,
		last_login float,
		FOREIGN KEY(user_id) REFERENCES User(id)
	)
""")

cur.execute("""
	CREATE TABLE Book(
		id integer primary key AUTOINCREMENT,
		title varchar(50),
		author integer,
		cover varchar(50),
		description TEXT,
		FOREIGN KEY(author) REFERENCES Author(id)
	)
""")

cur.execute("""
	CREATE TABLE Theme(
		id integer primary key AUTOINCREMENT,
		name varchar(40)
	)
""")

cur.execute("""
	CREATE TABLE BookTheme(
		book_id integer,
		theme_id integer,
		FOREIGN KEY(book_id) REFERENCES Book(id),
		FOREIGN KEY(theme_id) REFERENCES Theme(id)
	)
""")

cur.execute("""
	CREATE TABLE Copy(
		id integer primary key AUTOINCREMENT,
		book_id integer,
		FOREIGN KEY(book_id) REFERENCES Book(id)
	)
""")

cur.execute("""
	CREATE TABLE Borrow(
    		id INTEGER PRIMARY KEY AUTOINCREMENT,
    		movie_id INTEGER NOT NULL,
    		user_id INTEGER NOT NULL,
    		copy_id INTEGER NOT NULL,
    		borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    		return_date DATETIME,
    		FOREIGN KEY(movie_id) REFERENCES Book(id),
    		FOREIGN KEY(user_id) REFERENCES User(id),
    		FOREIGN KEY(copy_id) REFERENCES Copy(id)
	)
""")

cur.execute("""
	CREATE TABLE Author(
		id integer primary key AUTOINCREMENT,
		name varchar(40)
	)
""")

cur.execute("""
	CREATE TABLE User(
		id integer primary key AUTOINCREMENT,
		name varchar(20),
        last_name varchar(50),
        birth_date DATE,
        email varchar(30) UNIQUE,
		password varchar(32),
		admin integer
	)
""")

cur.execute("""
   CREATE TABLE UserPendientes(
		id integer primary key AUTOINCREMENT,
		name varchar(20),
       		last_name varchar(50),
        	birth_date DATE,
        	email varchar(30) UNIQUE,
		password varchar(32),
		admin integer
	)
""")

cur.execute("""
   CREATE TABLE Friend(
		user_id integer,
		friend_id integer,
		FOREIGN KEY(user_id) REFERENCES User(id),
		FOREIGN KEY(friend_id) REFERENCES User(id)
	)
""")

cur.execute("""
   CREATE TABLE Reviews (
    		id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único de la reseña
    		movie_id INTEGER NOT NULL,            -- ID de la película (clave foránea)
    		user_id INTEGER NOT NULL,             -- ID del usuario que escribió la reseña (clave foránea)
    		comentario TEXT,                      -- Comentario de la reseña
    		puntuacion INTEGER CHECK(puntuacion BETWEEN 1 AND 5), -- Puntuación (entre 1 y 5)
    		fecha DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha en que se hizo la reseña
    		FOREIGN KEY (movie_id) REFERENCES Book(id) ON DELETE CASCADE,
    		FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
	)
""")

cur.execute("""
   CREATE TABLE Donacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único de la donación
        donationAmount INTEGER NOT NULL,       -- Monto de la donación
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP -- Fecha de la donación (por defecto, la fecha actual)
   	)
""")

cur.execute("""
	CREATE TABLE BugReports (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    user_id INTEGER NOT NULL,
	    movie_title TEXT NOT NULL,
	    description TEXT NOT NULL,
	    report_date DATETIME NOT NULL,
	    FOREIGN KEY (user_id) REFERENCES User(id)
	)
""")



### Insert users
with open('../usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

try:

	for user in usuarios:
		dataBase_password = user['password'] + salt
		hashed = hashlib.md5(dataBase_password.encode())
		dataBase_password = hashed.hexdigest()
		cur.execute(
		    "INSERT INTO User VALUES (NULL, ?, ?, ?, ?, ?, ?)", 
		    (user['nombres'], user['apellidos'], user['fecha_nac'], user['email'], dataBase_password, user['admin'])
		)

		con.commit()
		
except:
	print("bd reiniciada")
